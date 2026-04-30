import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="AI Movie Recommender", layout="wide")

# -------------------------------
# 🔥 MODERN NETFLIX UI
# -------------------------------
st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0b0f1a;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* HERO SECTION */
.hero {
    background: linear-gradient(to right, #141e30, #243b55);
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 50px;
    font-weight: bold;
    color: #ff4b4b;
}

.hero-sub {
    font-size: 18px;
    color: #ccc;
}

/* MOVIE CARD */
.card {
    background-color: #141a2e;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    transition: 0.3s;
    cursor: pointer;
}

.card:hover {
    transform: scale(1.05);
    background-color: #1f2a48;
}

/* BUTTON */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 6px 12px;
}

.stButton>button:hover {
    background-color: #ff1f1f;
}

/* SECTION TITLE */
.section-title {
    font-size: 28px;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #ffffff;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 40px;
    color: #aaa;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🎬 HERO BANNER
# -------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">🎬 AI Movie Recommender</div>
    <div class="hero-sub">Discover movies you’ll love with AI-powered recommendations</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df.fillna('', inplace=True)
    return df

df = load_data()

# -------------------------------
# FAVORITES
# -------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------------
# 🔥 TRENDING
# -------------------------------
st.markdown('<div class="section-title">🔥 Trending Now</div>', unsafe_allow_html=True)

trending = df.sort_values(by='release_year', ascending=False).head(5)
cols = st.columns(5)

for col, (_, row) in zip(cols, trending.iterrows()):
    with col:
        st.markdown(f"<div class='card'>🎬 {row['title']}<br>📅 {row['release_year']}</div>", unsafe_allow_html=True)

# -------------------------------
# 🔍 SEARCH
# -------------------------------
st.markdown('<div class="section-title">🔍 Search Movie</div>', unsafe_allow_html=True)

search = st.text_input("Search your favorite movie")

if search:
    suggestions = df[df['title'].str.contains(search, case=False)]
    for title in suggestions['title'].head(5):
        st.write(f"👉 {title}")

# -------------------------------
# 🎯 FILTER
# -------------------------------
st.markdown('<div class="section-title">🎯 Browse by Category</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    type_option = st.selectbox("Type", df['type'].unique())

filtered_df = df[df['type'] == type_option]

genres = set()
for g in filtered_df['listed_in']:
    for item in g.split(','):
        genres.add(item.strip())

with col2:
    genre_option = st.selectbox("Genre", sorted(genres))

genre_filtered = filtered_df[
    filtered_df['listed_in'].str.contains(genre_option)
]

st.write(f"### {genre_option} {type_option}s")

cols = st.columns(5)

for col, (_, row) in zip(cols, genre_filtered.head(5).iterrows()):
    with col:
        st.markdown(f"<div class='card'>🎬 {row['title']}</div>", unsafe_allow_html=True)
        if st.button("❤️", key=row['title']):
            st.session_state.favorites.append(row['title'])

# -------------------------------
# 🤖 AI RECOMMENDATION
# -------------------------------
st.markdown('<div class="section-title">🤖 AI Recommendation</div>', unsafe_allow_html=True)

df['tags'] = df['listed_in'] + " " + df['description']

cv = CountVectorizer(max_features=3000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
similarity = cosine_similarity(vectors)

selected_movie = st.selectbox("Choose a movie", df['title'].values)

def recommend(title):
    index = df[df['title'] == title].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True)[1:6]
    return [df.iloc[i[0]].title for i in movie_list]

if st.button("Recommend 🎬"):
    results = recommend(selected_movie)

    cols = st.columns(5)
    for col, movie in zip(cols, results):
        with col:
            st.markdown(f"<div class='card'>🎬 {movie}</div>", unsafe_allow_html=True)
            if st.button("❤️", key=movie):
                st.session_state.favorites.append(movie)

# -------------------------------
# ❤️ FAVORITES
# -------------------------------
st.markdown('<div class="section-title">❤️ Your Favorites</div>', unsafe_allow_html=True)

if st.session_state.favorites:
    cols = st.columns(5)
    for col, fav in zip(cols, st.session_state.favorites):
        with col:
            st.markdown(f"<div class='card'>🎬 {fav}</div>", unsafe_allow_html=True)
else:
    st.write("No favorites yet")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
<div class="footer">
© 2026 | AI Movie Recommender | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)