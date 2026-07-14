import streamlit as st
import requests
from datetime import date
st.set_page_config(
    page_title="IPL Prediction System",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
:root{
    --navy: #16213E;
    --navy-deep: #0B1224;
    --blue: #1E88E5;
    --blue-light: #64B5F6;
    --ink: #1F2937;
    --muted: #6B7280;
    --card-border: #E4E9F5;
}

/* Hide Streamlit default chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* App background */
.stApp{
    background:
        radial-gradient(circle at 10% 0%, rgba(30,136,229,0.07), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(100,181,246,0.10), transparent 35%),
        linear-gradient(180deg, #F7F9FC 0%, #EEF2F9 100%);
    color: var(--ink);
}

/* Force readable text color in main content (overrides inherited
   dark-theme white text so it isn't invisible on the light bg) */
.stApp p, .stApp li, .stApp span, .stApp label,
.stApp div[data-testid="stMarkdownContainer"],
.stApp h1, .stApp h2, .stApp h3, .stApp h4{
    color: var(--ink) !important;
}
.stApp .stCaption, .stApp [data-testid="stCaptionContainer"]{
    color: var(--muted) !important;
}

/* Main title gets a gradient treatment */
.stApp h1{
    background: linear-gradient(90deg, var(--navy) 0%, var(--blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
    padding-bottom: 4px;
}

/* Section subheaders get a small left accent bar */
.stApp h3{
    border-left: 4px solid var(--blue);
    padding-left: 10px;
    font-weight: 700 !important;
}

/* Divider styling */
hr{
    border: none;
    height: 2px;
    background: linear-gradient(90deg, var(--blue) 0%, transparent 80%);
    opacity: 0.35;
}

/* Sidebar keeps white text regardless of the rule above */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div{
    color:white !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-deep) 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
}
section[data-testid="stSidebar"] h2{
    color: var(--blue-light) !important;
    font-weight:800;
    letter-spacing: 0.3px;
}

/* Radio options in sidebar look like nav items */
section[data-testid="stSidebar"] div[role="radiogroup"] label{
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background-color: rgba(30,136,229,0.25);
    border-color: var(--blue);
    transform: translateX(3px);
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:10px;
    background: linear-gradient(90deg, var(--blue) 0%, #1565C0 100%);
    color:white;
    font-weight:bold;
    border: none;
    padding: 0.6em 0;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton>button:hover{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(30,136,229,0.35);
}

/* ------------------------------------------------------------------
   Card containers created with st.container(border=True, key=...).
   Streamlit auto-generates a .st-key-<key> class on containers that
   are given a `key`, which is the most reliable way to target a
   specific container — the internal data-testid names have changed
   across Streamlit versions, so that's targeted too as a fallback.
   ------------------------------------------------------------------ */
.st-key-card-match-winner,
.st-key-card-live-probability,
.st-key-card-fastapi-backend,
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stContainer"]{
    border: 1.5px solid var(--card-border) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 14px rgba(16,24,64,0.06);
    background-color: white !important;
    padding: 14px 6px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.st-key-card-match-winner:hover,
.st-key-card-live-probability:hover,
.st-key-card-fastapi-backend:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:hover{
    transform: translateY(-5px);
    box-shadow: 0 14px 28px rgba(16,24,64,0.14);
    border-color: var(--blue) !important;
}

/* Metric cards */
div[data-testid="stMetric"]{
    background: white;
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 18px 10px;
    box-shadow: 0 4px 14px rgba(16,24,64,0.06);
    text-align: center;
    border-bottom: 3px solid var(--blue);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover{
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(16,24,64,0.12);
}
div[data-testid="stMetricValue"]{
    color: var(--blue);
    font-weight:800;
}
div[data-testid="stMetricLabel"]{
    color: var(--muted) !important;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.78rem;
    letter-spacing: 0.5px;
}

/* Info boxes */
div[data-testid="stAlert"]{
    border-radius: 12px;
    border-left: 4px solid var(--blue);
}

/* Titles */
h1, h2, h3 {
    color: var(--navy);
}

/* Custom scrollbar */
::-webkit-scrollbar{ width: 10px; }
::-webkit-scrollbar-track{ background: transparent; }
::-webkit-scrollbar-thumb{ background: #C7D2E8; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover{ background: var(--blue); }

</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 🏏 Navigation")
    page = st.radio(
        "Navigation",
        ["Home", "Match Winner Prediction", "Live Win Probability Prediction"],
        label_visibility="collapsed"
    )

if page == "Home":
    col1,col2,col3=st.columns([5,6,3])
    with col2:
        st.image("ipl banner.png",width=250)
    st.title("IPL Match Analytics & Prediction")
    st.caption(
        "Machine Learning powered Match Winner and Live Win Probability Prediction"
    )
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True, key="card-match-winner"):
            st.markdown("### Match Winner")
            st.write("Predict the winning team before the match starts.")
            st.markdown(
                "**Features**\n"
                "- Toss Information\n"
                "- Venue\n"
                "- Team Strength\n"
                "- Historical Data"
            )

    with col2:
        with st.container(border=True, key="card-live-probability"):
            st.markdown("### Live Probability")
            st.write("Predict winning probability during the chase.")
            st.markdown(
                "**Features**\n"
                "- Current Score\n"
                "- Wickets Left\n"
                "- Required Run Rate\n"
                "- Balls Remaining"
            )

    with col3:
        with st.container(border=True, key="card-fastapi-backend"):
            st.markdown("### FastAPI Backend")
            st.write("Predictions are served using REST APIs.")
            st.markdown(
                "**Built with**\n"
                "- FastAPI\n"
                "- Pydantic\n"
                "- Joblib\n"
                "- Scikit-Learn"
            )

    st.divider()
    st.subheader("Built Using")
    st.write(
        """
        - Python
        - Scikit-learn
        - FastAPI
        - Streamlit
        - Pandas
        - NumPy
        """
    )
    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Teams", 10)
    m2.metric("Models", 2)
    m3.metric("Features", "15")
    m4.metric("League", "IPL")
    st.markdown(
        """
        <div style='text-align:center; margin-top:2em; color:#6B7280;'>
        Developed by <b>Sriharshith</b>
        </div>
        """,
        unsafe_allow_html=True
    )
elif page == "Match Winner Prediction":
    st.title(" Match Winner Prediction")
    st.caption("Predict Match Winner based on the toss status")
    st.subheader("Enter Match Details")
    st.divider()
    col1,col2=st.columns(2)
    with col1:
        batting_team = st.selectbox(
        "Batting Team",
        [   "Select Team",
            "Chennai Super Kings",
            "Mumbai Indians",
            "Royal Challengers Bengaluru",
            "Kolkata Knight Riders",
            "Sunrisers Hyderabad",
            "Delhi Capitals",
            "Punjab Kings",
            "Rajasthan Royals",
            "Lucknow Super Giants",
            "Gujarat Titans"
        ]
    )
        bowling_team = st.selectbox(
        "Bowling Team",
        [   "Select Team",
            "Chennai Super Kings",
            "Mumbai Indians",
            "Royal Challengers Bengaluru",
            "Kolkata Knight Riders",
            "Sunrisers Hyderabad",
            "Delhi Capitals",
            "Punjab Kings",
            "Rajasthan Royals",
            "Lucknow Super Giants",
            "Gujarat Titans"
        ]
    )
        toss_winner = st.selectbox(
        "Toss Winner",
        [   "Select Team",
            "Chennai Super Kings",
            "Mumbai Indians",
            "Royal Challengers Bengaluru",
            "Kolkata Knight Riders",
            "Sunrisers Hyderabad",
            "Delhi Capitals",
            "Punjab Kings",
            "Rajasthan Royals",
            "Lucknow Super Giants",
            "Gujarat Titans"
        ]
    )
        toss_decision=st.selectbox("Toss Decision",["Select","bat","field"])
        stage=st.selectbox(
            "Stage",[
                "group stage","Qualifier 1","Qualifier 2","Eliminator","Final"
            ]
    )
    with col2:
        venue=st.selectbox("Venue",["Select Venue",
            "MA Chidambaram Stadium",
            "Wankhede Stadium",
            "M Chinnaswamy Stadium",
            "Eden Gardens",
            "Rajiv Gandhi International Stadium",
            "Sawai Mansingh Stadium",
            "Arun Jaitley Stadium",
            "Punjab Cricket Association Stadium",
            "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
            "Narendra Modi Stadium"
        ])
        city = st.selectbox(
            "City",
            [
                "Ahmedabad",
                "Abu Dhabi",
                "Bangalore",
                "Chandigarh",
                "Chennai",
                "Delhi",
                "Dubai",
                "Dharamsala",
                "Hyderabad",
                "Kolkata",
                "Lucknow",
                "Mumbai",
                "Pune",
                "Jaipur",
                "Sharjah",
                "Visakhapatnam"
            ],
            index=None,
            placeholder="Select City"
        )

        season = st.text_input(
        "Season")
        match_date = st.date_input(
        "Match Date",
        value=None,
        min_value=date(2008, 1, 1),
        max_value=date(2030, 12, 31),
        format="YYYY-MM-DD"
    )  
    predict=st.button("Predict Match Winner",use_container_width=True)
    payload={
        "batting_team": batting_team,
        "bowling_team": bowling_team,
        "toss_winner": toss_winner,
        "toss_decision":toss_decision,
        "venue": venue,
        "city": city,
        "season": season,
        "stage": stage,
        "date":str(match_date)
        }
    response=requests.post("https://ipl-api-9c17.onrender.com/match_winner_predict",json=payload)
    team_colors = {
    "Chennai Super Kings": "#F9CD05",
    "Mumbai Indians": "#004BA0",
    "Royal Challengers Bengaluru": "#D71920",
    "Sunrisers Hyderabad": "#F26522",
    "Kolkata Knight Riders": "#3A225D",
    "Delhi Capitals": "#17449B",
    "Rajasthan Royals": "#EA1A85",
    "Punjab Kings": "#D71920",
    "Lucknow Super Giants": "#00A651",
    "Gujarat Titans": "#1C2957"
}
    if predict:
        result = response.json()
        Winner = result["predicted_winner"]
        st.divider()
        color = team_colors.get(Winner, "#1565C0")
        def darken(hex_color, factor=0.55):
            hex_color = hex_color.lstrip("#")
            r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            r, g, b = int(r*factor), int(g*factor), int(b*factor)
            return f"#{r:02x}{g:02x}{b:02x}"
        dark_shade = darken(color)
        st.markdown(
            f"""
            <style>
            @keyframes floatTrophy {{
                0%   {{ transform: translateY(0px) rotate(0deg); }}
                50%  {{ transform: translateY(-8px) rotate(-4deg); }}
                100% {{ transform: translateY(0px) rotate(0deg); }}
            }}
            @keyframes shimmer {{
                0%   {{ background-position: -300px 0; }}
                100% {{ background-position: 300px 0; }}
            }}
            @keyframes fadeInUp {{
                0%   {{ opacity: 0; transform: translateY(20px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}

            .winner-card {{
                position: relative;
                background: linear-gradient(135deg, {color} 0%, {dark_shade} 100%);
                padding: 40px 30px;
                border-radius: 22px;
                text-align: center;
                color: #ffffff;
                box-shadow: 0 12px 30px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.08) inset;
                overflow: hidden;
                animation: fadeInUp 0.6s ease-out;
                border: 1px solid rgba(255,255,255,0.15);
            }}

            .winner-card::before {{
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: linear-gradient(
                    120deg,
                    rgba(255,255,255,0) 30%,
                    rgba(255,255,255,0.15) 50%,
                    rgba(255,255,255,0) 70%
                );
                background-size: 200% 100%;
                animation: shimmer 3.5s infinite linear;
                pointer-events: none;
            }}

            .winner-label {{
                display: inline-block;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
                color: rgba(255,255,255,0.85);
                margin-bottom: 6px;
            }}

            .winner-trophy {{
                font-size: 46px;
                display: block;
                animation: floatTrophy 2.4s ease-in-out infinite;
                filter: drop-shadow(0 4px 6px rgba(0,0,0,0.35));
                margin-bottom: 4px;
            }}

            .winner-name {{
                font-size: 40px;
                font-weight: 800;
                margin: 8px 0 0 0;
                color: #ffffff;
                text-shadow: 0 3px 10px rgba(0,0,0,0.5);
                letter-spacing: 0.5px;
                line-height: 1.2;
            }}

            .winner-sub {{
                margin-top: 14px;
                font-size: 13px;
                color: rgba(255,255,255,0.75);
                letter-spacing: 1px;
            }}
            </style>

            <div class="winner-card">
                <span class="winner-trophy">🏆</span>
                <span class="winner-label">Predicted Winner</span>
                <h1 class="winner-name">{Winner}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
elif page == "Live Win Probability Prediction":
    st.title("Live Win Probability")
    st.caption("Predict the probability of winning based on current match status")
    st.subheader("Enter Match Details")
    st.divider()
    col1,col2=st.columns(2)
    with col1:
        innings=st.number_input(
            "Innings",
            value=2,
            format="%d"
        )
        Batting_team = st.selectbox(
        "Batting Team",
        [   "Select Team",
            "Chennai Super Kings",
            "Mumbai Indians",
            "Royal Challengers Bengaluru",
            "Kolkata Knight Riders",
            "Sunrisers Hyderabad",
            "Delhi Capitals",
            "Punjab Kings",
            "Rajasthan Royals",
            "Lucknow Super Giants",
            "Gujarat Titans"
        ]
    )
        Bowling_team = st.selectbox(
        "Bowling Team",
        [   "Select Team",
            "Chennai Super Kings",
            "Mumbai Indians",
            "Royal Challengers Bengaluru",
            "Kolkata Knight Riders",
            "Sunrisers Hyderabad",
            "Delhi Capitals",
            "Punjab Kings",
            "Rajasthan Royals",
            "Lucknow Super Giants",
            "Gujarat Titans"
        ]
    )
        Venue=st.selectbox("Venue",["Select Venue",
            "MA Chidambaram Stadium",
            "Wankhede Stadium",
            "M Chinnaswamy Stadium",
            "Eden Gardens",
            "Rajiv Gandhi International Stadium",
            "Sawai Mansingh Stadium",
            "Arun Jaitley Stadium",
            "Punjab Cricket Association Stadium",
            "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
            "Narendra Modi Stadium"
        ])
    with col2:
        team_runs=st.number_input(
            "Current Team Runs",
            min_value=0,
            value=0,
            step=1,
            format="%d"
        )
        team_wicket=st.number_input(
            "Current Team Wickets",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            format="%d"
        )
        team_balls=st.number_input(
            "Number of Balls Till Now",
            min_value=0,
            max_value=120,
            value=0,
            step=1,
            format="%d"
        )
        runs_target = st.number_input(
            "Target",
            min_value=1,
            value=1,
            step=1,
            format="%d"
        )
    predict=st.button("Predict Live win probability",use_container_width=True)
    payload={
        "innings":innings,
        "team_runs":team_runs,
        "team_balls":team_balls,
        "team_wicket":team_wicket,
        "venue":Venue,
        "runs_target":runs_target,
        "batting_team":Batting_team,
        "bowling_team":Bowling_team
    }
    response=requests.post("https://ipl-api-9c17.onrender.com/live_pred",json=payload)
    team_colors = {
    "Chennai Super Kings": "#F9CD05",
    "Mumbai Indians": "#004BA0",
    "Royal Challengers Bengaluru": "#D71920",
    "Sunrisers Hyderabad": "#F26522",
    "Kolkata Knight Riders": "#3A225D",
    "Delhi Capitals": "#17449B",
    "Rajasthan Royals": "#EA1A85",
    "Punjab Kings": "#D71920",
    "Lucknow Super Giants": "#00A651",
    "Gujarat Titans": "#1C2957"
}
    team_short = {
        "Chennai Super Kings":"CSK",
        "Mumbai Indians":"MI",
        "Royal Challengers Bengaluru":"RCB",
        "Kolkata Knight Riders":"KKR",
        "Sunrisers Hyderabad":"SRH",
        "Delhi Capitals":"DC",
        "Punjab Kings":"PBKS",
        "Rajasthan Royals":"RR",
        "Lucknow Super Giants":"LSG",
        "Gujarat Titans":"GT"
    }
    if predict:
        result = response.json()
        batting_team = result["batting_team"]
        bowling_team = result["bowling_team"]
        batting_prob = int(round(result["batting_probability"]))
        bowling_prob = int(round(result["bowling_probability"]))
        winner = result["predicted_winner"]
        winner_prob = batting_prob if winner == batting_team else bowling_prob
        team_runs = result["team_runs"]
        team_wicket = result["team_wicket"]
        over = result["over"]
        ball = result["ball"]
        runs_target = result["runs_target"]
        crr = result["current_rr"]
        req_rr = result["required_rr"]
        short_a = "".join(w[0] for w in batting_team.split()) 
        short_b = "".join(w[0] for w in bowling_team.split())   
        color_a = team_colors.get(batting_team, "#8ecbff")
        color_b = team_colors.get(bowling_team, "#ffb3a7")
        winner_color = team_colors.get(winner, "#1565C0")
        st.divider()
        html = f"""<div style="max-width:700px;margin:auto;background:white;padding:30px;border-radius:20px;box-shadow:0px 5px 18px rgba(0,0,0,0.15);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
        <div style="text-align:left;">
        <div style="font-size:13px;color:#888;font-weight:600;">{short_a}</div>
        <div style="font-size:26px;font-weight:700;color:#222;">{team_runs}/{team_wicket} <span style="font-size:14px;color:#888;">({over}.{ball} ov)</span></div>
        </div>
        <div style="text-align:right;">
        <div style="font-size:13px;color:#888;font-weight:600;">TARGET</div>
        <div style="font-size:26px;font-weight:700;color:#222;">{runs_target}</div>
        </div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:22px;padding-top:10px;border-top:1px dashed #e5e5e5;">
        <div style="font-size:18px;color:#555;">Current RR: <b style="color:#1565C0;">{crr}</b></div>
        <div style="font-size:18px;color:#555;">Required RR: <b style="color:#D71920;">{req_rr}</b></div>
        </div>
        <h3 style="text-align:center;color:#1565C0;margin-bottom:25px;">🏏 Live Win Probability</h3>
        <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-weight:bold;font-size:18px;">
        <span style="color:{color_a};">{short_a} ({batting_prob}%)</span>
        <span style="color:{color_b};">{short_b} ({bowling_prob}%)</span>
        </div>
        <div style="display:flex;width:100%;height:20px;border-radius:10px;overflow:hidden;background:#EEEEEE;">
        <div style="width:{batting_prob}%;background:{color_a};"></div>
        <div style="width:{bowling_prob}%;background:{color_b};"></div>
        </div>
        <div style="margin-top:35px;background:{winner_color};border-radius:18px;padding:25px;text-align:center;color:white;">
        <div style="font-size:45px;">🏆</div>
        <div style="font-size:14px;letter-spacing:2px;font-weight:bold;">PREDICTED WINNER</div>
        <div style="font-size:32px;font-weight:800;margin-top:10px;">{winner}</div>
        <div style="margin-top:10px;font-size:18px;">Winning Chance : <b>{winner_prob}%</b></div>
        </div>
        </div>"""

        st.markdown(html, unsafe_allow_html=True)
