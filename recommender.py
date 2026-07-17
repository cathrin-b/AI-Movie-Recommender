"""
Hybrid movie recommender.

Two signals are combined:

1. CONTENT-BASED
   Each movie is represented as a TF-IDF vector over its genres + overview
   text. Similarity between movies is cosine similarity between these
   vectors. This is what powers "movies similar to X" and gives us a way to
   score movies for brand-new users (cold start) based on the movies they
   say they like.

2. COLLABORATIVE FILTERING
   The user-item rating matrix is factorized with truncated SVD (matrix
   factorization) into latent user/item vectors. A user's predicted rating
   for a movie they haven't seen is the dot product of their latent vector
   and the movie's latent vector, plus bias terms. This captures "people
   with taste like yours rated this highly" style signal.

HYBRID
   Final score = alpha * collaborative_score + (1 - alpha) * content_score
   alpha adapts to how much rating data we have for a user: a brand-new
   user leans almost entirely on content-based scoring; an established
   user leans mostly on collaborative filtering.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@dataclass
class Recommender:
    movies: pd.DataFrame = field(default_factory=pd.DataFrame)
    ratings: pd.DataFrame = field(default_factory=pd.DataFrame)

    def __post_init__(self):
        self._load_data()
        self._build_content_model()
        self._build_cf_model()

    # ------------------------------------------------------------------ #
    # Data loading
    # ------------------------------------------------------------------ #
    def _load_data(self):
        self.movies = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))
        self.ratings = pd.read_csv(os.path.join(DATA_DIR, "ratings.csv"))
        self.movie_id_to_idx = {mid: i for i, mid in enumerate(self.movies["movie_id"])}
        self.idx_to_movie_id = {i: mid for mid, i in self.movie_id_to_idx.items()}

    # ------------------------------------------------------------------ #
    # Content-based model
    # ------------------------------------------------------------------ #
    def _build_content_model(self):
        # Repeat genre tokens so they carry real weight against the free-text overview
        text = (
            self.movies["genres"].str.replace("|", " ", regex=False) + " "
        ) * 3 + self.movies["overview"].fillna("")
        self._tfidf = TfidfVectorizer(stop_words="english", min_df=1)
        self._tfidf_matrix = self._tfidf.fit_transform(text)
        self._content_sim = cosine_similarity(self._tfidf_matrix)

    def similar_movies(self, movie_id: int, top_n: int = 10) -> list[dict]:
        idx = self.movie_id_to_idx.get(movie_id)
        if idx is None:
            return []
        sims = self._content_sim[idx]
        order = np.argsort(-sims)
        results = []
        for i in order:
            if i == idx:
                continue
            results.append({
                "movie_id": int(self.idx_to_movie_id[i]),
                "score": float(sims[i]),
            })
            if len(results) >= top_n:
                break
        return results

    def _content_scores_for_liked(self, liked_movie_ids: list[int]) -> np.ndarray:
        """Average similarity to a set of movies a user says they like."""
        idxs = [self.movie_id_to_idx[m] for m in liked_movie_ids if m in self.movie_id_to_idx]
        if not idxs:
            return np.zeros(len(self.movies))
        return self._content_sim[idxs].mean(axis=0)

    # ------------------------------------------------------------------ #
    # Collaborative filtering model (matrix factorization via SVD)
    # ------------------------------------------------------------------ #
    def _build_cf_model(self):
        self.user_ids = sorted(self.ratings["user_id"].unique())
        self.user_id_to_idx = {uid: i for i, uid in enumerate(self.user_ids)}

        n_users = len(self.user_ids)
        n_items = len(self.movies)
        matrix = np.zeros((n_users, n_items))
        mask = np.zeros((n_users, n_items), dtype=bool)

        for row in self.ratings.itertuples():
            u = self.user_id_to_idx[row.user_id]
            i = self.movie_id_to_idx.get(row.movie_id)
            if i is not None:
                matrix[u, i] = row.rating
                mask[u, i] = True

        self.global_mean = self.ratings["rating"].mean()
        # per-user and per-item bias (mean rating deviation), used to fill sparsity
        user_means = np.array([
            matrix[u, mask[u]].mean() if mask[u].any() else self.global_mean
            for u in range(n_users)
        ])
        item_means = np.array([
            matrix[mask[:, i], i].mean() if mask[:, i].any() else self.global_mean
            for i in range(n_items)
        ])
        self.user_bias = user_means - self.global_mean
        self.item_bias = item_means - self.global_mean

        filled = matrix.copy()
        for u in range(n_users):
            for i in range(n_items):
                if not mask[u, i]:
                    filled[u, i] = self.global_mean + self.user_bias[u] + self.item_bias[i]

        n_components = min(20, min(n_users, n_items) - 1)
        n_components = max(n_components, 2)
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        self._user_factors = svd.fit_transform(filled - self.global_mean)
        self._item_factors = svd.components_.T
        self._cf_matrix = filled  # cache of best-guess ratings, kept for cold reads

    def _predict_cf_row(self, user_id: int) -> np.ndarray:
        """Predicted rating vector across all movies for a known user."""
        u = self.user_id_to_idx.get(user_id)
        if u is None:
            return np.full(len(self.movies), self.global_mean)
        preds = self.global_mean + self._user_factors[u] @ self._item_factors.T
        return preds

    # ------------------------------------------------------------------ #
    # Hybrid recommendation
    # ------------------------------------------------------------------ #
    def recommend(
        self,
        user_id: int | None,
        liked_movie_ids: list[int] | None = None,
        exclude_movie_ids: list[int] | None = None,
        top_n: int = 12,
    ) -> list[dict]:
        liked_movie_ids = liked_movie_ids or []
        exclude_movie_ids = set(exclude_movie_ids or [])

        n_known_ratings = 0
        if user_id is not None and user_id in self.user_id_to_idx:
            n_known_ratings = int((self.ratings["user_id"] == user_id).sum())

        # alpha = weight on collaborative filtering; ramps up with more rating history
        alpha = min(0.85, 0.15 + 0.05 * n_known_ratings) if n_known_ratings else 0.0

        content_scores = self._content_scores_for_liked(liked_movie_ids)
        if content_scores.sum() == 0 and not liked_movie_ids:
            # no content signal at all -> neutral (won't matter once alpha handles it)
            content_scores = np.zeros(len(self.movies))

        if user_id is not None and user_id in self.user_id_to_idx:
            cf_scores = self._predict_cf_row(user_id)
        else:
            cf_scores = np.full(len(self.movies), self.global_mean)

        # normalize both signals to 0-1 so they combine fairly
        def normalize(arr: np.ndarray) -> np.ndarray:
            lo, hi = arr.min(), arr.max()
            if hi - lo < 1e-9:
                return np.zeros_like(arr)
            return (arr - lo) / (hi - lo)

        cf_norm = normalize(cf_scores)
        content_norm = normalize(content_scores)

        final_scores = alpha * cf_norm + (1 - alpha) * content_norm

        already_rated = set()
        if user_id is not None:
            already_rated = set(
                self.ratings.loc[self.ratings["user_id"] == user_id, "movie_id"]
            )

        order = np.argsort(-final_scores)
        results = []
        for i in order:
            mid = int(self.idx_to_movie_id[i])
            if mid in exclude_movie_ids or mid in already_rated or mid in liked_movie_ids:
                continue
            results.append({
                "movie_id": mid,
                "score": float(final_scores[i]),
                "content_score": float(content_norm[i]),
                "cf_score": float(cf_norm[i]),
            })
            if len(results) >= top_n:
                break

        return results, alpha

    # ------------------------------------------------------------------ #
    # Mutations (ratings)
    # ------------------------------------------------------------------ #
    def add_rating(self, user_id: int, movie_id: int, rating: float):
        new_row = pd.DataFrame([{"user_id": user_id, "movie_id": movie_id, "rating": rating}])
        self.ratings = pd.concat([self.ratings, new_row], ignore_index=True)
        # keep only the latest rating per (user, movie)
        self.ratings = (
            self.ratings.sort_index()
            .drop_duplicates(subset=["user_id", "movie_id"], keep="last")
            .reset_index(drop=True)
        )
        self._build_cf_model()  # cheap enough at this dataset size to just retrain

    def movie_dict(self, movie_id: int) -> dict | None:
        row = self.movies.loc[self.movies["movie_id"] == movie_id]
        if row.empty:
            return None
        row = row.iloc[0]
        return {
            "movie_id": int(row["movie_id"]),
            "title": row["title"],
            "year": int(row["year"]),
            "genres": row["genres"].split("|"),
            "overview": row["overview"],
        }
