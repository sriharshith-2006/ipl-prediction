# 🏏 IPL Match Winner & Live Win Probability Predictor

An end-to-end machine learning application that predicts IPL match outcomes two ways — **before the toss** and **ball-by-ball during the chase.** Built with a production-style split between a FastAPI backend and a Streamlit frontend, containerized with Docker, and deployed on Render.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B" />
  <img src="https://img.shields.io/badge/XGBoost-Model-EB5E28" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED" />
  <img src="https://img.shields.io/badge/Deployed-Render-46E3B7" />
</p>

**[🚀 Live App](https://ipl-streamlit.onrender.com/) &nbsp;·&nbsp; [⚡ API Docs](https://ipl-api-9c17.onrender.com/docs)**

> ⚠️ Hosted on Render's free tier — the first request may take 30–60s to wake up the server.

---

## What it does

Cricket fans usually get one of two experiences: pre-match predictions from pundits, or live win% bars on broadcast graphics with no explanation of how they're computed. This project builds both, transparently, from historical IPL data:

| | Match Winner | Live Win Probability |
|---|---|---|
| **When** | Before a ball is bowled | Live, during the 2nd innings |
| **Inputs** | Teams, toss, venue, stage, season | Score, wickets, overs, target, run rates |
| **Output** | Predicted winner | Live win % for both teams, updating over-by-over |

---

## Screenshots

**Dashboard** — a quick snapshot of what the models are trained on and what they cover.

![Home dashboard](images/home.png)

**Pre-match prediction** — feed in the matchup and conditions, get a predicted winner.

![Match winner prediction](images/winner_prediction.png)

**Live chase tracker** — enter the current match state and get a live-updating win probability bar, styled like a broadcast graphic.

![Live win probability](images/live_prediction.png)

---

## How it's built

```
                         Historical IPL Dataset
                                  │
                     Cleaning + Feature Engineering
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                            ▼
          Match Winner Model              Live Win Prob Model
        (pre-match features)          (in-match state features)
                    │                            │
                    └─────────────┬──────────────┘
                                  ▼
                          FastAPI Backend
                       (validation, inference)
                                  │
                                  ▼
                         Streamlit Frontend
                        (interactive UI/UX)
```

Two independently trained XGBoost classifiers power the two use cases — a pre-match model that only sees information available before a ball is bowled, and a live model that consumes evolving match state (runs left, balls left, current/required run rate, wickets in hand) so the probability shifts realistically as the chase unfolds.

---

## Tech Stack

| Layer | Tools |
|---|---|
| **ML** | Scikit-Learn, XGBoost, Pandas, NumPy, Joblib |
| **Backend** | FastAPI, Pydantic, Uvicorn |
| **Frontend** | Streamlit, HTML/CSS |
| **Infra** | Docker, Render, GitHub |

---

## Project Structure

```
ipl/
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── streamlit/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── models/
│   ├── winner_model.pkl
│   ├── winner_preprocessor.pkl
│   ├── winner_label_encoder.pkl
│   ├── live_pred_model.pkl
│   └── live_pred_preprocessor.pkl
├── notebooks/
├── images/
└── README.md
```

---

## Running it locally

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

**Backend**
```bash
cd api
pip install -r requirements.txt
uvicorn app:app --reload
# → http://127.0.0.1:8000  |  Swagger docs: /docs
```

**Frontend**
```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
# → http://localhost:8501
```

**Or with Docker:**
```bash
docker build -t ipl-api -f api/Dockerfile .
docker run -p 8000:8000 ipl-api

docker build -t ipl-streamlit -f streamlit/Dockerfile .
docker run -p 8501:8501 ipl-streamlit
```

---

## API Reference

### `POST /match_winner_predict`
Predicts the winner before the match starts.

```json
{
  "batting_team": "Mumbai Indians",
  "bowling_team": "Chennai Super Kings",
  "toss_winner": "Mumbai Indians",
  "toss_decision": "bat",
  "venue": "Wankhede Stadium",
  "city": "Mumbai",
  "season": "IPL 2025",
  "stage": "group stage",
  "date": "2025-05-10"
}
```

### `POST /live_pred`
Predicts live win probability during the second innings.

```json
{
  "innings": 2,
  "team_runs": 145,
  "team_balls": 96,
  "team_wicket": 4,
  "runs_target": 185,
  "batting_team": "Mumbai Indians",
  "bowling_team": "Chennai Super Kings",
  "venue": "Wankhede Stadium"
}
```

Both endpoints validate input automatically via Pydantic, and full interactive docs are available on the [Swagger UI](https://ipl-api-9c17.onrender.com/docs).

---

## Engineered Features

For the live win probability model, raw match state is transformed into features that actually track how a chase is going:

- Runs left, balls left, wickets left
- Current run rate & required run rate
- Over number, ball number within over

---

## What I'd build next

- Real-time score integration (live data feed instead of manual input)
- Player-level performance and score prediction
- Toss-outcome prediction
- A full match analytics dashboard with historical trends and standings

---

## What I learned

Shipping this end-to-end pushed me past "train a model in a notebook" into the parts that make a project actually usable: structuring an ML pipeline with two independent models, serving predictions through a validated REST API, building a UI that doesn't feel like a form dump, containerizing both services, and getting the whole thing live on Render.

---

## Author

**Janga Sriharshith**
B.Tech in Artificial Intelligence and Data Science, IIIT Sri City

[GitHub](https://github.com/YOUR_GITHUB_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN_USERNAME) · [Email](mailto:YOUR_EMAIL@example.com)

---

⭐ If this project was useful or interesting to you, a star on GitHub goes a long way.
