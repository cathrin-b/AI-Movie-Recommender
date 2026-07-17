from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from recommender import Recommender

app = FastAPI(title="Hybrid Movie Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = Recommender()


# ---------------------------------------------------------------------- #
# Schemas
# ---------------------------------------------------------------------- #
class RatingIn(BaseModel):
    user_id: int
    movie_id: int
    rating: float = Field(ge=0.5, le=5.0)


class RecommendIn(BaseModel):
    user_id: Optional[int] = None
    liked_movie_ids: list[int] = Field(default_factory=list)
    top_n: int = 12


# ---------------------------------------------------------------------- #
# Routes
# ---------------------------------------------------------------------- #
@app.get("/health")
def health():
    return {"status": "ok", "movies": len(engine.movies), "ratings": len(engine.ratings)}


@app.get("/movies")
def list_movies(search: str = "", genre: str = "", limit: int = 200):
    df = engine.movies
    if search:
        df = df[df["title"].str.contains(search, case=False, na=False)]
    if genre:
        df = df[df["genres"].str.contains(genre, case=False, na=False)]
    df = df.head(limit)
    return [
        {
            "movie_id": int(r.movie_id),
            "title": r.title,
            "year": int(r.year),
            "genres": r.genres.split("|"),
            "overview": r.overview,
        }
        for r in df.itertuples()
    ]


@app.get("/genres")
def list_genres():
    genres = set()
    for g in engine.movies["genres"]:
        genres.update(g.split("|"))
    return sorted(genres)


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = engine.movie_dict(movie_id)
    if movie is None:
        raise HTTPException(404, "Movie not found")
    return movie


@app.get("/movies/{movie_id}/similar")
def similar(movie_id: int, top_n: int = 8):
    if engine.movie_dict(movie_id) is None:
        raise HTTPException(404, "Movie not found")
    sims = engine.similar_movies(movie_id, top_n=top_n)
    return [{**engine.movie_dict(s["movie_id"]), "score": s["score"]} for s in sims]


@app.post("/ratings")
def rate_movie(payload: RatingIn):
    if engine.movie_dict(payload.movie_id) is None:
        raise HTTPException(404, "Movie not found")
    engine.add_rating(payload.user_id, payload.movie_id, payload.rating)
    return {"status": "ok"}


@app.get("/users/{user_id}/ratings")
def user_ratings(user_id: int):
    rows = engine.ratings[engine.ratings["user_id"] == user_id]
    return [
        {**engine.movie_dict(int(r.movie_id)), "rating": r.rating}
        for r in rows.itertuples()
    ]


@app.post("/recommend")
def recommend(payload: RecommendIn):
    results, alpha = engine.recommend(
        user_id=payload.user_id,
        liked_movie_ids=payload.liked_movie_ids,
        top_n=payload.top_n,
    )
    return {
        "alpha_collaborative_weight": alpha,
        "recommendations": [
            {**engine.movie_dict(r["movie_id"]), **r} for r in results
        ],
    }
