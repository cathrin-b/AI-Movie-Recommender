# Reel — Hybrid Movie Recommender

A full-stack movie recommendation system combining **content-based filtering**
(genre/plot similarity via TF-IDF) with **collaborative filtering** (matrix
factorization on a user-item rating matrix), served through a FastAPI backend
and a React frontend.

## How the recommender works

**Content-based** — Every movie is turned into a TF-IDF vector over its
genres + a short synopsis. Cosine similarity between vectors gives a
"movies like this" score. This is what powers cold-start recommendations
for a brand-new user who has rated nothing yet — as soon as they like even
one movie, we can point to similar ones.

**Collaborative filtering** — The full user × movie rating matrix is
factorized with truncated SVD into latent user and item vectors (classic
matrix-factorization recommender, same family of technique behind the
Netflix Prize). A user's predicted rating for something they haven't seen is
the dot product of their latent taste vector and the movie's latent vector.
This captures "people who rate like you also loved this" signal that
content similarity alone can't see.

**Hybrid blend** — The two scores are normalized and combined:

```
final_score = alpha * collaborative_score + (1 - alpha) * content_score
```

`alpha` ramps up automatically with how much rating history a user has —
a new user's recommendations lean almost entirely on content similarity;
an established user's lean mostly on collaborative filtering. The `/recommend`
endpoint returns the actual `alpha` used plus the two component scores, and
the "For You" tab visualizes that split per recommendation.

## Project structure

```
movie-recommender/
├── backend/
│   ├── main.py            FastAPI app + REST endpoints
│   ├── recommender.py     Hybrid recommender engine
│   ├── requirements.txt
│   └── data/
│       ├── movies.csv       107 curated movies (title, genres, synopsis)
│       ├── ratings.csv      ~1,500 synthetic ratings across 60 users
│       ├── build_movies.py  regenerates movies.csv
│       └── build_ratings.py regenerates ratings.csv
└── frontend/
    ├── src/
    │   ├── App.jsx         Browse / My Ratings / For You views
    │   └── index.css       design system
    ├── index.html
    ├── package.json
    └── vite.config.js      dev server + API proxy
```

## Running it locally

**Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API is now live at `http://localhost:8000` (interactive docs at `/docs`).

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api/*` requests
to the backend on port 8000, so both need to be running.

## Trying it out

1. Go to **Browse**, star-rate a handful of movies (try picking a consistent
   taste — e.g. only sci-fi, or only romance — to see clean genre-driven
   recommendations).
2. Switch to **For You**. With few ratings, recommendations lean on content
   similarity; keep rating and the collaborative-filtering weight (shown at
   the top of the tab) climbs.
3. Change the **User ID** field in the top-right — IDs 1–60 already have
   synthetic rating histories baked in from `ratings.csv`, so you can see
   how recommendations differ across existing "taste clusters" without
   rating anything yourself. Any other ID starts as a fresh cold-start user.

## Extending this project

Ideas if you want to keep building:
- Swap the synthetic dataset for the real [MovieLens](https://grouplens.org/datasets/movielens/)
  dataset (25M ratings) for a production-scale demo.
- Add posters via a movie metadata API (e.g. TMDB) to the movie cards.
- Persist ratings to a real database (SQLite/Postgres) instead of the
  in-memory pandas DataFrame — right now ratings reset when the backend
  restarts.
- Try a different CF algorithm (e.g. `scikit-surprise`'s SVD++, or an
  implicit-feedback ALS model) and compare recommendation quality.
- Add an explicit "why this was recommended" explanation using the nearest
  neighbor movies that drove the content score.
