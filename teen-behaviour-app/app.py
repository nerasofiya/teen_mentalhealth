import os
import pickle
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

# Set up page config
st.set_page_config(page_title="Teen Behavioral Assistant",
                   layout="wide",
                   page_icon="")

# Get working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load your custom usage habit model 
try:
    habit_model = pickle.load(open(f'{working_dir}/saved_models/usage_habit_model.sav', 'rb'))
except FileNotFoundError:
    st.error("Model file not found! Please ensure 'usage_habit_model.sav' exists in the 'saved_models' directory.")
    habit_model = None

# Sidebar Navigation with custom colorful styling
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4F46E5;'>Navigation Menu</h2>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title='Mental Health Portal',
        options=['Habit Predictor', 'System Overview'],
        icons=['activity', 'info-circle'],
        menu_icon='heart-pulse',
        default_index=0,
        styles={
            "container": {"padding": "5px!", "background-color": "#f8fafc"},
            "icon": {"color": "#6366f1", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#e2e8f0"},
            "nav-link-selected": {"background-color": "#4f46e5", "color": "white"},
        }
    )

# --- Prediction Page ---
if selected == 'Habit Predictor':
    st.markdown("<h1 style='color: #4F46E5;'>Teen Social Media Habit Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("##### Please complete the profile details below to evaluate digital well-being patterns:")
    
    st.markdown("---")

    # Group 1: Demographics & Usage
    st.markdown("### Step 1: Core Metrics & Routine")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Age of Teenager', min_value=13, max_value=19, value=15, step=1)
        gender_raw = st.selectbox('Gender', options=['Female', 'Male'])
        daily_hours = st.number_input('Daily Social Media Use (Hours)', min_value=0.0, max_value=24.0, value=4.0, step=0.5)

    with col2:
        platform_raw = st.selectbox('Primary Platform', options=['Instagram', 'TikTok', 'Both'])
        sleep_hours = st.number_input('Average Nightly Sleep (Hours)', min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        screen_time_before_sleep = st.number_input('Pre-Bed Screen Time (Hours)', min_value=0.0, max_value=5.0, value=1.5, step=0.1)

    with col3:
        academic_perf = st.number_input('Academic Performance (GPA)', min_value=0.0, max_value=4.0, value=3.0, step=0.01)
        physical_act = st.number_input('Daily Exercise/Activity (Hours)', min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        social_level_raw = st.selectbox('In-Person Socializing Level', options=['Low', 'Medium', 'High'])

    st.markdown("---")

    # Group 2: Psychological Evaluation
    st.markdown("### Step 2: Psychological Self-Evaluation")
    st.caption("Rate the following indicators on a slider scale from 1 (Lowest) to 10 (Highest):")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        stress_level = st.slider('Current Stress Level', min_value=1, max_value=10, value=5)
    with col5:
        box = st.slider('Current Anxiety Level', min_value=1, max_value=10, value=5)
    with col6:
        addiction_level = st.slider('Social Media Fixation / Urge', min_value=1, max_value=10, value=5)

    # Encode raw user metrics to operational feature values
    gender = 0 if gender_raw == 'Female' else 1
    platform_usage = {'Both': 0, 'Instagram': 1, 'TikTok': 2}[platform_raw]
    social_interaction_level = {'High': 0, 'Low': 1, 'Medium': 2}[social_level_raw]

    st.markdown("<br>", unsafe_allow_html=True)

    # Prediction Action Layout
    if st.button('Run Analysis Report', use_container_width=True):
        if habit_model is not None:
            user_input = [
                age, gender, daily_hours, platform_usage, sleep_hours, 
                screen_time_before_sleep, academic_perf, physical_act, 
                social_interaction_level, stress_level, box, addiction_level
            ]
            
            prediction = habit_model.predict([user_input])
            
            st.markdown("### Evaluation Result")
            if prediction[0] == 1:
                st.markdown(
                    """
                    <div style="background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 20px; border-radius: 8px;">
                        <h4 style="color: #991b1b; margin: 0 0 10px 0;">Risk Flags Detected</h4>
                        <p style="color: #7f1d1d; margin: 0; font-size: 16px;">
                            The current profile suggests screen habits that lean toward an <strong>Unhealthy Social Media Balance</strong>. 
                            Taking structured breaks and setting tech-free boundaries could benefit overall routine dynamics.
                        </p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style="background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 20px; border-radius: 8px;">
                        <h4 style="color: #166534; margin: 0 0 10px 0;">Balanced Profile</h4>
                        <p style="color: #14532d; margin: 0; font-size: 16px;">
                            The current profile metrics reflect a <strong>Healthy & Balanced Digital Usage Pattern</strong>. 
                            Online activities and daily wellness metrics appear to look stable and well-proportioned!
                        </p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.warning("Prediction cannot be completed because the machine learning model is missing.")

# --- Overview Page ---
if selected == 'System Overview':
    st.markdown("<h1 style='color: #4F46E5;'>System and Project Info</h1>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background-color: #f0fdfa; border-left: 5px solid #0d9488; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #115e59; margin: 0 0 8px 0;">Project Objective</h4>
            <p style="color: #134e4a; margin: 0;">
                This assistant is designed to identify screens and routine patterns that might negatively affect well-being. 
                By correlating personal usage stats alongside self-reported mental wellness markers, the predictive model 
                promotes healthy reflection and assists caregivers in determining when to offer positive guidance.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info("Engine: Powered by an optimized Random Forest Classification pipeline.")
    with col_info2:
        st.success("Privacy First: Data entered into this dashboard is handled instantly in-memory and never cached.")
