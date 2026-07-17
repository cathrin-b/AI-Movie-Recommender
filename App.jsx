import { useEffect, useMemo, useState, useCallback } from 'react'

const API = '/api'

function SprocketStrip() {
  const holes = Array.from({ length: 40 })
  return (
    <div className="sprocket-strip">
      {holes.map((_, i) => <span key={i} />)}
    </div>
  )
}

function Stars({ value, onRate }) {
  const rounded = Math.round(value || 0)
  return (
    <div className="stars">
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          key={n}
          className={`star-btn ${n <= rounded ? 'filled' : ''}`}
          onClick={() => onRate(n)}
          title={`Rate ${n} star${n > 1 ? 's' : ''}`}
        >
          ★
        </button>
      ))}
    </div>
  )
}

function MatchDial({ contentScore, cfScore }) {
  const total = contentScore + cfScore || 1
  const contentPct = (contentScore / total) * 100
  const cfPct = (cfScore / total) * 100
  return (
    <div className="match-dial">
      <div className="match-track">
        <div className="match-fill-content" style={{ width: `${contentPct}%` }} />
        <div className="match-fill-cf" style={{ width: `${cfPct}%` }} />
      </div>
      <span className="match-label">match breakdown</span>
    </div>
  )
}

function MovieCard({ movie, rating, onRate, showMatch }) {
  return (
    <div className="card">
      <div className="card-title-row">
        <div className="card-title">{movie.title}</div>
        <div className="card-year">{movie.year}</div>
      </div>
      <div className="genre-row">
        {movie.genres.map((g) => <span className="genre-pill" key={g}>{g}</span>)}
      </div>
      <div className="overview">{movie.overview}</div>
      {showMatch && <MatchDial contentScore={movie.content_score} cfScore={movie.cf_score} />}
      <div className="card-actions">
        <Stars value={rating} onRate={(n) => onRate(movie.movie_id, n)} />
      </div>
    </div>
  )
}

export default function App() {
  const [tab, setTab] = useState('browse')
  const [movies, setMovies] = useState([])
  const [genres, setGenres] = useState([])
  const [search, setSearch] = useState('')
  const [genreFilter, setGenreFilter] = useState('')
  const [userId, setUserId] = useState(1)
  const [myRatings, setMyRatings] = useState({}) // movie_id -> rating
  const [recs, setRecs] = useState([])
  const [alpha, setAlpha] = useState(0)
  const [loadingRecs, setLoadingRecs] = useState(false)

  // load full movie catalog + genre list once
  useEffect(() => {
    fetch(`${API}/genres`).then(r => r.json()).then(setGenres)
  }, [])

  useEffect(() => {
    const params = new URLSearchParams()
    if (search) params.set('search', search)
    if (genreFilter) params.set('genre', genreFilter)
    fetch(`${API}/movies?${params.toString()}`).then(r => r.json()).then(setMovies)
  }, [search, genreFilter])

  const loadMyRatings = useCallback(() => {
    fetch(`${API}/users/${userId}/ratings`)
      .then(r => r.json())
      .then(rows => {
        const map = {}
        rows.forEach(row => { map[row.movie_id] = row.rating })
        setMyRatings(map)
      })
  }, [userId])

  useEffect(() => { loadMyRatings() }, [loadMyRatings])

  const handleRate = useCallback((movieId, rating) => {
    setMyRatings(prev => ({ ...prev, [movieId]: rating }))
    fetch(`${API}/ratings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, movie_id: movieId, rating }),
    })
  }, [userId])

  const fetchRecommendations = useCallback(() => {
    setLoadingRecs(true)
    const likedIds = Object.entries(myRatings)
      .filter(([, r]) => r >= 4)
      .map(([id]) => Number(id))
    fetch(`${API}/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, liked_movie_ids: likedIds, top_n: 12 }),
    })
      .then(r => r.json())
      .then(data => {
        setRecs(data.recommendations)
        setAlpha(data.alpha_collaborative_weight)
      })
      .finally(() => setLoadingRecs(false))
  }, [userId, myRatings])

  useEffect(() => {
    if (tab === 'foryou') fetchRecommendations()
  }, [tab, fetchRecommendations])

  const ratedCount = Object.keys(myRatings).length
  const myRatedMovies = useMemo(
    () => movies.filter(m => myRatings[m.movie_id] !== undefined),
    [movies, myRatings]
  )

  return (
    <div className="app">
      <SprocketStrip />
      <header className="header">
        <div className="logo">reel<span className="dot">.</span></div>
        <div className="tagline">Hybrid recommender · content similarity + collaborative filtering</div>
      </header>

      <nav className="tabs">
        <button className={`tab ${tab === 'browse' ? 'active' : ''}`} onClick={() => setTab('browse')}>
          Browse
        </button>
        <button className={`tab ${tab === 'myratings' ? 'active' : ''}`} onClick={() => setTab('myratings')}>
          My Ratings <span className="count">{ratedCount}</span>
        </button>
        <button className={`tab ${tab === 'foryou' ? 'active' : ''}`} onClick={() => setTab('foryou')}>
          For You
        </button>
        <div style={{ marginLeft: 'auto' }} className="user-switcher">
          <label>User ID</label>
          <input
            type="number"
            value={userId}
            onChange={(e) => setUserId(Number(e.target.value) || 1)}
          />
        </div>
      </nav>

      <main className="main">
        {tab === 'browse' && (
          <>
            <h2 className="section-title">Browse the catalog</h2>
            <p className="section-sub">{movies.length} films · rate a few to sharpen your recommendations</p>
            <div className="controls">
              <input
                className="search-input"
                placeholder="Search by title…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <select className="select" value={genreFilter} onChange={(e) => setGenreFilter(e.target.value)}>
                <option value="">All genres</option>
                {genres.map(g => <option key={g} value={g}>{g}</option>)}
              </select>
            </div>
            <div className="grid">
              {movies.map(m => (
                <MovieCard key={m.movie_id} movie={m} rating={myRatings[m.movie_id]} onRate={handleRate} />
              ))}
            </div>
          </>
        )}

        {tab === 'myratings' && (
          <>
            <h2 className="section-title">Your ratings</h2>
            <p className="section-sub">User #{userId} · {ratedCount} movies rated</p>
            {myRatedMovies.length === 0 ? (
              <div className="empty">
                <strong>No ratings yet</strong>
                Head to Browse and star a few movies you like — the more you rate, the more the
                collaborative side of the recommender kicks in.
              </div>
            ) : (
              <div className="grid">
                {myRatedMovies.map(m => (
                  <MovieCard key={m.movie_id} movie={m} rating={myRatings[m.movie_id]} onRate={handleRate} />
                ))}
              </div>
            )}
          </>
        )}

        {tab === 'foryou' && (
          <>
            <h2 className="section-title">Recommended for you</h2>
            <p className="section-sub">User #{userId} · blended from content similarity and rating patterns</p>
            <div className="alpha-banner">
              collaborative filtering weight: <strong style={{ color: 'var(--ink)' }}>{Math.round(alpha * 100)}%</strong>
              &nbsp;·&nbsp; content-based weight: <strong style={{ color: 'var(--ink)' }}>{Math.round((1 - alpha) * 100)}%</strong>
            </div>
            <div className="legend">
              <div className="legend-item"><span className="legend-dot" style={{ background: 'var(--teal)' }} /> content match</div>
              <div className="legend-item"><span className="legend-dot" style={{ background: 'var(--amber)' }} /> collaborative match</div>
            </div>
            {loadingRecs ? (
              <div className="spinner-text">Scoring the catalog…</div>
            ) : recs.length === 0 ? (
              <div className="empty">
                <strong>Nothing to recommend yet</strong>
                Rate a handful of movies first — even 3 or 4 is enough to get started.
              </div>
            ) : (
              <div className="grid">
                {recs.map(m => (
                  <MovieCard key={m.movie_id} movie={m} rating={myRatings[m.movie_id]} onRate={handleRate} showMatch />
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}
