# 🎬 AI Movie Recommendation System

## 📌 Project Overview

The AI Movie Recommendation System is a smart web application built using Python, Machine Learning, and Streamlit that helps users discover movies based on their interests and preferences.

This project uses content-based filtering with cosine similarity to recommend similar movies based on genres and descriptions. Users can search movies, browse by category, explore trending content, and save favorite movies.

The application is designed with a modern Netflix-style UI to provide a clean and interactive user experience.

---

## 🚀 Features

* 🔥 Trending Movies Section
* 🔍 Smart Movie Search
* 🎯 Browse by Type and Genre
* 🤖 AI-Based Movie Recommendations
* ❤️ Add to Favorites Feature
* 🎬 Movie Posters Display
* 🌙 Modern Dark UI (Netflix Style)
* 📱 Responsive Streamlit Layout

---

## 🛠 Technologies Used

* Python
* Streamlit
* Pandas
* Scikit-learn
* CountVectorizer
* Cosine Similarity
* HTML + CSS (for UI customization)

---

## 📂 Dataset Used

Dataset Name: `netflix_titles.csv`

The dataset contains:

* Movie Title
* Type (Movie / TV Show)
* Genre
* Description
* Release Year
* Additional metadata

---

## ⚙️ How It Works

### Step 1: Load Dataset

The system loads the Netflix dataset and handles missing values.

### Step 2: Create Tags

Genres and descriptions are combined into a single feature called `tags`.

### Step 3: Vectorization

Using CountVectorizer, text data is converted into numerical vectors.

### Step 4: Similarity Calculation

Cosine similarity is used to calculate how similar one movie is to another.

### Step 5: Recommendation

When a user selects a movie, the system recommends the top 5 most similar movies.

---

## ▶️ How to Run the Project

### Install Required Libraries

```bash
pip install streamlit pandas scikit-learn
```

### Run the Application

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```bash
AI-Movie-Recommendation-System/
│
├── app.py
├── netflix_titles.csv
├── posters/
│   ├── default.jpg
│   ├── movie1.jpg
│   ├── movie2.jpg
│
└── README.md
```

---

## 💼 Resume Description

Built an AI-powered Movie Recommendation System using Machine Learning with content-based filtering, cosine similarity, and Streamlit. Designed a modern Netflix-style user interface with trending movies, search, filters, favorites, and poster display.

---

## 🌐 Future Improvements

* Add movie trailers
* Add ratings and reviews
* Add OTT platform filters
* User login system
* Personalized recommendations
* Cloud deployment

---

## 👩‍💻 Developed By

Cathrin Prasalya

Final Year B.Com (Computer Applications) Student
Aspiring Data Analyst | Python | Power BI | Machine Learning

---

## ❤️ Conclusion

This project demonstrates practical implementation of machine learning in recommendation systems while combining strong UI/UX design for real-world usability.

It is a portfolio-ready project suitable for internships, placements, and LinkedIn showcase.
