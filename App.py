# app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Europa League Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #ffde59;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .match-card {
        background-color: rgba(12, 46, 78, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #ffde59;
    }
    .stButton>button {
        background-color: #ffde59;
        color: #0c2e4e;
        font-weight: bold;
        border-radius: 20px;
        padding: 10px 24px;
    }
    .points-display {
        background-color: rgba(12, 46, 78, 0.7);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for points and predictions
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}

# Europa League data - 2023-24 season (example data)
def get_europa_league_data():
    matchdays = {
        1: [
            {"date": "2023-09-21", "home": "Arsenal", "away": "PSV Eindhoven", "group": "B"},
            {"date": "2023-09-21", "home": "Manchester United", "away": "Real Sociedad", "group": "E"},
            {"date": "2023-09-21", "home": "Roma", "away": "Young Boys", "group": "G"},
            {"date": "2023-09-21", "home": "Napoli", "away": "Leicester City", "group": "C"},
            {"date": "2023-09-21", "home": "Lyon", "away": "Rangers", "group": "A"},
            {"date": "2023-09-21", "home": "Monaco", "away": "PSV", "group": "B"}
        ],
        2: [
            {"date": "2023-10-05", "home": "Lazio", "away": "Marseille", "group": "D"},
            {"date": "2023-10-05", "home": "Barcelona", "away": "Benfica", "group": "E"},
            {"date": "2023-10-05", "home": "Celtic", "away": "Bayer Leverkusen", "group": "G"},
            {"date": "2023-10-05", "home": "West Ham", "away": "Genk", "group": "H"},
            {"date": "2023-10-05", "home": "Leicester", "away": "Spartak Moscow", "group": "C"},
            {"date": "2023-10-05", "home": "Rangers", "away": "Brondby", "group": "A"}
        ],
        3: [
            {"date": "2023-10-26", "home": "Real Sociedad", "away": "Sturm Graz", "group": "B"},
            {"date": "2023-10-26", "home": "PSV", "away": "Bodo/Glimt", "group": "C"},
            {"date": "2023-10-26", "home": "Braga", "away": "Ludogorets", "group": "D"},
            {"date": "2023-10-26", "home": "Fenerbahce", "away": "Antwerp", "group": "E"},
            {"date": "2023-10-26", "home": "Dinamo Zagreb", "away": "Rapid Wien", "group": "F"},
            {"date": "2023-10-26", "home": "Galatasaray", "away": "Olympiakos", "group": "G"}
        ],
        4: [
            {"date": "2023-11-09", "home": "Sturm Graz", "away": "Real Sociedad", "group": "B"},
            {"date": "2023-11-09", "home": "Bodo/Glimt", "away": "PSV", "group": "C"},
            {"date": "2023-11-09", "home": "Ludogorets", "away": "Braga", "group": "D"},
            {"date": "2023-11-09", "home": "Antwerp", "away": "Fenerbahce", "group": "E"},
            {"date": "2023-11-09", "home": "Rapid Wien", "away": "Dinamo Zagreb", "group": "F"},
            {"date": "2023-11-09", "home": "Olympiakos", "away": "Galatasaray", "group": "G"}
        ],
        5: [
            {"date": "2023-11-30", "home": "Real Sociedad", "away": "PSV", "group": "B"},
            {"date": "2023-11-30", "home": "Sturm Graz", "away": "Monaco", "group": "B"},
            {"date": "2023-11-30", "home": "Spartak Moscow", "away": "Napoli", "group": "C"},
            {"date": "2023-11-30", "home": "Leicester", "away": "Legia Warsaw", "group": "C"},
            {"date": "2023-11-30", "home": "Lazio", "away": "Lokomotiv Moscow", "group": "D"},
            {"date": "2023-11-30", "home": "Marseille", "away": "Galatasaray", "group": "D"}
        ],
        6: [
            {"date": "2023-12-09", "home": "PSV", "away": "Real Sociedad", "group": "B"},
            {"date": "2023-12-09", "home": "Monaco", "away": "Sturm Graz", "group": "B"},
            {"date": "2023-12-09", "home": "Napoli", "away": "Leicester", "group": "C"},
            {"date": "2023-12-09", "home": "Legia Warsaw", "away": "Spartak Moscow", "group": "C"},
            {"date": "2023-12-09", "home": "Lokomotiv Moscow", "away": "Lazio", "group": "D"},
            {"date": "2023-12-09", "home": "Galatasaray", "away": "Marseille", "group": "D"}
        ]
    }
    return matchdays

# Header
st.markdown('<h1 class="main-header">Europa League Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Predict scores for all matchdays and earn points for correct predictions")

# Points display
st.markdown(f"""
<div class="points-display">
    <h2>Total Points: {st.session_state.points}</h2>
</div>
""", unsafe_allow_html=True)

# Competition selector
matchdays_data = get_europa_league_data()

# Matchday selector
matchday = st.selectbox("Select Matchday", options=list(matchdays_data.keys()), format_func=lambda x: f"Matchday {x}")

# Display matches for selected matchday
st.markdown(f'<div class="subheader">Matchday {matchday} Fixtures</div>', unsafe_allow_html=True)

for i, match in enumerate(matchdays_data[matchday]):
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        
        with col1:
            st.markdown(f"**{match['home']}**")
        with col2:
            home_score = st.number_input("", min_value=0, max_value=10, value=0, key=f"home_{matchday}_{i}")
        with col3:
            st.markdown("**vs**", help="Enter your score prediction")
        with col4:
            away_score = st.number_input("", min_value=0, max_value=10, value=0, key=f"away_{matchday}_{i}")
        with col5:
            st.markdown(f"**{match['away']}**")
        
        # Store prediction
        match_key = f"{match['home']}_{match['away']}_{matchday}"
        st.session_state.predictions[match_key] = (home_score, away_score)
        
        st.markdown(f"*Group {match['group']} - {match['date']}*")
        st.markdown("---")

# Submit button
if st.button("Submit Predictions", use_container_width=True):
    # Calculate points (simplified for demo)
    points_earned = 0
    for match_key, prediction in st.session_state.predictions.items():
        # Simulate some correct predictions
        if sum(prediction) % 3 == 0:  # Just a simple example condition
            points_earned += 3
        elif sum(prediction) % 2 == 0:
            points_earned += 1
    
    st.session_state.points += points_earned
    st.success(f"You earned {points_earned} points! Total points: {st.session_state.points}")
    st.balloons()

# Rules section
st.markdown("---")
st.markdown("### Scoring Rules")
rules_col1, rules_col2 = st.columns(2)

with rules_col1:
    st.markdown("""
    - **3 points** for correctly predicting the exact scoreline
    - **1 point** for correctly predicting the outcome (win, lose, or draw)
    - **0 points** for incorrect outcome prediction
    """)

with rules_col2:
    st.markdown("""
    - **+1 bonus point** for predicting a correct draw with correct goals (e.g. 1-1, 2-2)
    - **+2 bonus points** for predicting a correct high-scoring game (4+ goals)
    """)

# Footer
st.markdown("---")
st.markdown("*This is a demo application. Actual Europa League fixtures may vary.*")
