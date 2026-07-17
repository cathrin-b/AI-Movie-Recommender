"""
Generates synthetic ratings.csv. Users are drawn from a handful of "taste
clusters" (e.g. sci-fi/action fans, drama/romance fans, horror fans, animation
fans, prestige/crime drama fans) so that collaborative filtering has genuine
structure to learn from, plus noise so it isn't trivial.
"""
import csv
import random

random.seed(42)

with open("/home/claude/movie-recommender/backend/data/movies.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    movies = list(reader)

for m in movies:
    m["genres"] = m["genres"].split("|")

CLUSTERS = {
    "scifi_action":   {"Sci-Fi": 2.0, "Action": 1.8, "Adventure": 1.2, "Thriller": 1.0},
    "drama_romance":  {"Drama": 2.0, "Romance": 1.8, "Biography": 1.0},
    "horror_thriller":{"Horror": 2.2, "Thriller": 1.6, "Mystery": 1.2},
    "animation_family":{"Animation": 2.2, "Family": 1.8, "Comedy": 1.0},
    "crime_drama":    {"Crime": 2.0, "Drama": 1.4, "Thriller": 1.2, "Mystery": 1.0},
    "comedy_fan":     {"Comedy": 2.2, "Romance": 1.0, "Adventure": 0.8},
    "prestige_mixed": {"Drama": 1.5, "History": 1.3, "War": 1.2, "Mystery": 1.0, "Sci-Fi": 0.8},
}

N_USERS = 60
rows = []
user_id = 1
cluster_names = list(CLUSTERS.keys())

for _ in range(N_USERS):
    # each user leans toward 1-2 clusters (blended taste), so CF finds real neighbors
    primary = random.choice(cluster_names)
    secondary = random.choice(cluster_names)
    weights = {}
    for g, w in CLUSTERS[primary].items():
        weights[g] = weights.get(g, 0) + w
    for g, w in CLUSTERS[secondary].items():
        weights[g] = weights.get(g, 0) + 0.5 * w

    # how many movies this user has rated
    n_rated = random.randint(15, 35)
    sample = random.sample(movies, n_rated)

    for m in sample:
        base = 3.0  # neutral baseline
        affinity = sum(weights.get(g, 0) for g in m["genres"])
        score = base + 0.35 * affinity + random.gauss(0, 0.6)
        rating = max(1, min(5, round(score * 2) / 2))  # clamp to [1,5], half-star steps
        rows.append((user_id, int(m["movie_id"]), rating))

    user_id += 1

with open("/home/claude/movie-recommender/backend/data/ratings.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["user_id", "movie_id", "rating"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} ratings across {N_USERS} users")
