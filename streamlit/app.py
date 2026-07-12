import streamlit as st
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
        city=st.text_input("City")
        season = st.number_input(
        "Season",
        min_value=2008,
        max_value=2035,
    )
        match_date = st.date_input(
        "Match Date",
        value=None,
        format="YYYY-MM-DD"
    )
       
    predict=st.button("Predict Match Winner",use_container_width=True)
    if predict:
        st.success("Succesfully entered details")
elif page == "Live Win Probability Prediction":
    st.title("Live Win Probability")
    st.caption("Predict the probability of winning based on current match status")
    st.subheader("Enter Match Details")
    st.divider()
    col1,col2=st.columns(2)
    with col1:
        innings=st.number_input("Innings")
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
    with col2:
        team_runs = st.number_input(
            "Current Team Runs",
            min_value=0,
            value=0,
            step=1,
            format="%d"
        )

        team_wicket = st.number_input(
            "Current Team Wicket",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            format="%d"
        )
        team_balls = st.number_input(
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
    if predict:
            st.success("Ok")
    
