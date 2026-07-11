# 🏏 IPL Match Outcome Prediction

An end-to-end Machine Learning application that predicts the **winner of an IPL match before it begins** and estimates the **live winning probability during the second innings**. The project exposes trained machine learning models through **FastAPI** and provides an interactive **Streamlit** web interface.

---

## 📌 Features

### 🏆 Match Winner Prediction
Predict the winning team before the match starts using:

- Batting Team
- Bowling Team
- Toss Winner
- Toss Decision
- Venue
- City
- Match Stage
- Match Date

### 📈 Live Win Probability
Predict the winning probability during the chase using:

- Current Score
- Target Score
- Wickets Fallen
- Balls Bowled
- Current Run Rate
- Required Run Rate

The application returns:

- Predicted Winner
- Batting Team Win Probability
- Bowling Team Win Probability

---

## 🛠 Tech Stack

- **Python**
- **Scikit-learn**
- **Pandas**
- **NumPy**
- **FastAPI**
- **Pydantic**
- **Streamlit**
- **Docker**
- **Joblib**

---

## 📂 Project Structure

```
IPL-Prediction/
│
├── api/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── models/
│   ├── winner_model.pkl
│   ├── winner_preprocessor.pkl
│   ├── winner_label_encoder.pkl
│   ├── live_pred_model.pkl
│   └── live_pred_preprocessor.pkl
│
├── streamlit/
│   └── app.py
│
├── notebooks/
│
├── data/
│
├── images/
│
├── README.md
│
└── .gitignore
```

---

## ⚙️ Machine Learning Pipeline

### Match Winner Prediction

**Feature Engineering**

- Batting Team
- Bowling Team
- Toss Winner
- Toss Decision
- Venue
- City
- Season
- Match Stage
- Home Advantage
- Toss Advantage
- Knockout Match Indicator
- Match Date Features

**Preprocessing**

- One-Hot Encoding
- ColumnTransformer
- Scikit-learn Pipeline

**Model**

- Random Forest Classifier

---

### Live Win Probability Prediction

**Engineered Features**

- Runs Left
- Balls Left
- Wickets Left
- Current Run Rate
- Required Run Rate
- Over
- Ball

**Model**

- Random Forest Classifier

---

## 🚀 API Endpoints

### Match Winner Prediction

**POST** `/match_winner_predict`

Example Request

```json
{
  "batting_team": "Chennai Super Kings",
  "bowling_team": "Mumbai Indians",
  "toss_winner": "Mumbai Indians",
  "toss_decision": "field",
  "venue": "Wankhede Stadium",
  "city": "Mumbai",
  "season": 2025,
  "stage": "group stage",
  "date": "2025-04-20"
}
```

Example Response

```json
{
  "Predicted Winner": "Mumbai Indians"
}
```

---

### Live Win Prediction

**POST** `/live_pred`

Example Request

```json
{
  "innings": 2,
  "team_runs": 140,
  "team_balls": 96,
  "team_wicket": 4,
  "runs_target": 186,
  "venue": "Wankhede Stadium",
  "batting_team": "Chennai Super Kings",
  "bowling_team": "Mumbai Indians"
}
```

Example Response

```json
{
  "Predicted Winner": "Mumbai Indians",
  "Chennai Super Kings Win Probability": 37.84,
  "Mumbai Indians Win Probability": 62.16
}
```

---

## ▶️ Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/IPL-Prediction.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run FastAPI

```bash
uvicorn app:app --reload
```

API Documentation will be available at:

```
http://127.0.0.1:8000/docs
```

### Run Streamlit

```bash
streamlit run app.py
```

---

## 🐳 Docker

Build the Docker image

```bash
docker build -t ipl-prediction .
```

Run the container

```bash
docker run -p 8000:8000 ipl-prediction
```

---

## 📊 Workflow

```
User Input
      │
      ▼
Feature Engineering
      │
      ▼
Preprocessing Pipeline
      │
      ▼
Machine Learning Model
      │
      ▼
FastAPI
      │
      ▼
Streamlit Dashboard
```

---

## 📈 Future Improvements

- Player statistics integration
- Team form analysis
- Weather information
- Head-to-head statistics
- XGBoost and LightGBM models
- Cloud deployment
- CI/CD pipeline

---

## 👨‍💻 Author

**Sriharshith**

B.Tech – Artificial Intelligence & Data Science  
IIIT Sri City

GitHub: https://github.com/sriharshith-2006

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.