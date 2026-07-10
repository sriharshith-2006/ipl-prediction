from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Annotated,Literal
from typing import Literal
import joblib
import pandas as pd
Team = Literal[
    "Chennai Super Kings",
    "Mumbai Indians",
    "Royal Challengers Bengaluru",
    "Kolkata Knight Riders",
    "Sunrisers Hyderabad",
    "Rajasthan Royals",
    "Delhi Capitals",
    "Punjab Kings",
    "Lucknow Super Giants",
    "Gujarat Titans"
]
TEAM_HOME_VENUE = {
    "Chennai Super Kings": "MA Chidambaram Stadium",
    "Mumbai Indians": "Wankhede Stadium",
    "Royal Challengers Bengaluru": "M Chinnaswamy Stadium",
    "Kolkata Knight Riders": "Eden Gardens",
    "Sunrisers Hyderabad": "Rajiv Gandhi International Stadium",
    "Rajasthan Royals": "Sawai Mansingh Stadium",
    "Delhi Capitals": "Arun Jaitley Stadium",
    "Punjab Kings": "Punjab Cricket Association Stadium",
    "Lucknow Super Giants": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    "Gujarat Titans": "Narendra Modi Stadium"
}

class MatchWinner(BaseModel):
    batting_team: Team
    bowling_team: Team
    toss_winner: Team
    toss_decision:Literal["bat","field"]
    venue: Annotated[str,Field(...,min_length=3)]
    city:Annotated[str,Field(...,min_length=3)]
    season: Annotated[str,Field(...)]
    stage: Literal["group stage","Qualifier 1","Qualifier 2","Eliminator","Final"]
    date:date
winner_model=joblib.load("../models/winner_model.pkl")
winner_preprocessor=joblib.load("../models/winner_preprocessor.pkl")
winner_label_encoder=joblib.load("../models/winner_label-encoder.pkl")
live_model=joblib.load("../models/live_pred_model.pkl")
live_preprocessor=joblib.load("../models/live_pred_preprocessor.pkl")
app=FastAPI(title="IPL_prediction_API",version="1.0.0")
@app.post('/match_winner_predict')
def predict_match_winner(request:MatchWinner):
    year=request.date.year
    month=request.date.month
    day=request.date.day
    batting_team_won_toss=int(request.batting_team==request.toss_winner)
    is_knockout=int(request.stage!='group stage')
    batting_team_home = int(
        TEAM_HOME_VENUE.get(request.batting_team) == request.venue
    )
    bowling_team_home = int(
    TEAM_HOME_VENUE.get(request.bowling_team) == request.venue
    )
    new_match = pd.DataFrame({
    'batting_team': [request.batting_team],
    'bowling_team': [request.bowling_team],
    'toss_winner': [request.toss_winner],
    'toss_decision':[request.toss_decision], 
    'venue':[request.venue],
    'city':[request.city],
    'season':[request.season],
    'stage_clean':[request.stage],
    'year':[year],
    'month': [month],
    'day':[day],
    'batting_team_home':[batting_team_home],
    'bowling_team_home':[bowling_team_home],
    'batting_team_won_toss':[batting_team_won_toss],
    'is_knockout':[is_knockout]
    })
    X=winner_preprocessor.transform(new_match)
    prediction=winner_model.predict(X)
    winner=winner_label_encoder.inverse_transform(prediction)[0]
    return{
        "Predicted Winner":winner
    }
class Live_pred(BaseModel):
    innings:Literal[2]
    team_runs:Annotated[int,Field(...,ge=0,le=720)]
    team_balls:Annotated[int,Field(...,ge=0,le=120)]
    team_wicket:Annotated[int,Field(...,ge=0,le=10)]
    venue:Annotated[str,Field(...,min_length=3)]
    runs_target:Annotated[int,Field(...,gt=0)]
    batting_team:Team
    bowling_team:Team
@app.post('/live_pred')
def live_pred(request:Live_pred):
    over=request.team_balls//6
    ball=request.team_balls%6
    balls_left=120-request.team_balls
    runs_left=request.runs_target-request.team_runs
    wickets_left=10-request.team_wicket
    current_rr=(request.team_runs*6)/request.team_balls if request.team_balls>0 else 0
    required_rr=(runs_left*6)/balls_left if balls_left>0 else 0
    new_data=pd.DataFrame({
    "innings": [request.innings],
    "team_runs": [request.team_runs],
    "team_balls": [request.team_balls],
    "team_wicket": [request.team_wicket],
    "runs_target": [request.runs_target],
    "batting_team": [request.batting_team],
    "bowling_team": [request.bowling_team],
    "venue": [request.venue],
    "over": [over],
    "ball": [ball],
    "runs_left": [runs_left],
    "balls_left": [balls_left],
    "wickets_left": [wickets_left],
    "current_rr": [current_rr],
    "required_rr": [required_rr]
    })
    Y=live_preprocessor.transform(new_data)
    prediction=live_model.predict(Y)
    probability=live_model.predict_proba(Y)
    if prediction[0]== 1:
        predicted_winner = request.batting_team
    else:
        predicted_winner = request.bowling_team
    return {
        "Predicted Winner": predicted_winner,
        f"{request.batting_team} Win Probability": round(probability[0][1] * 100, 2),
        f"{request.bowling_team} Win Probability": round(probability[0][0] * 100, 2)
    }
