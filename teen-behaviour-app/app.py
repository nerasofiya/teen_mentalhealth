import os
import pickle
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

# Set up page config
st.set_page_config(page_title="Teen Behavioral Assistant",
                   layout="wide",
                   page_icon="🧠")

# Get working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load your custom usage habit model 
# (Make sure to save your model as 'usage_habit_model.sav' inside your saved_models folder)
try:
    habit_model = pickle.load(open(f'{working_dir}/saved_models/usage_habit_model.sav', 'rb'))
except FileNotFoundError:
    st.error("Model file not found! Please ensure 'usage_habit_model.sav' exists in the 'saved_models' directory.")
    habit_model = None

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title='Teen Mental Health System',
        options=['Usage Habit Prediction', 'Project Overview'],
        icons=['activity', 'book'],
        menu_icon='brain',
        default_index=0
    )

# --- Prediction Page ---
if selected == 'Usage Habit Prediction':
    st.title('Teen Social Media Usage Habit Predictor')
    st.markdown("Enter the teen's demographic, digital usage, and psychological metrics below:")

    # Form structure divided into columns
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Age of the Teenager', min_value=13, max_value=19, value=15, step=1)
        gender_raw = st.selectbox('Gender', options=['Female', 'Male'])
        daily_hours = st.number_input('Daily Social Media Usage (Hours)', min_value=0.0, max_value=24.0, value=4.0, step=0.5)

    with col2:
        platform_raw = st.selectbox('Primary Platform Usage', options=['Instagram', 'TikTok', 'Both'])
        sleep_hours = st.number_input('Average Sleep Hours', min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        screen_time_before_sleep = st.number_input('Screen Time Before Sleep (Hours)', min_value=0.0, max_value=5.0, value=1.5, step=0.1)

    with col3:
        academic_perf = st.number_input('Academic Performance (GPA/Score)', min_value=0.0, max_value=4.0, value=3.0, step=0.01)
        physical_act = st.number_input('Daily Physical Activity (Hours)', min_value=0.0, max_value=10.0, value=1.0, step=0.1)
        social_level_raw = st.selectbox('In-Person Social Interaction Level', options=['Low', 'Medium', 'High'])

    st.subheader("Psychological Evaluation Scales (1-10)")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        stress_level = st.slider('Stress Level Scale', min_value=1, max_value=10, value=5)
    with col5:
        anxiety_level = st.slider('Anxiety Level Scale', min_value=1, max_value=10, value=5)
    with col6:
        addiction_level = st.slider('Social Media Addiction Scale', min_value=1, max_value=10, value=5)

    # Label Encoding Mapping based on notebook conventions
    # (Update mappings if your LabelEncoder order differed during fitting)
    gender = 0 if gender_raw == 'Female' else 1
    
    platform_map = {'Both': 0, 'Instagram': 1, 'TikTok': 2}
    platform_usage = platform_map[platform_raw]
    
    social_map = {'High': 0, 'Low': 1, 'Medium': 2}
    social_interaction_level = social_map[social_level_raw]

    # Prediction Action
    habit_diagnosis = ''
    
    if st.button('Analyze Behavioral Habits'):
        if habit_model is not None:
            # Structuring inputs in the exact sequence as the trained model features
            user_input = [
                age, gender, daily_hours, platform_usage, sleep_hours, 
                screen_time_before_sleep, academic_perf, physical_act, 
                social_interaction_level, stress_level, anxiety_level, addiction_level
            ]
            
            # Predict
            prediction = habit_model.predict([user_input])
            
            if prediction[0] == 1:
                st.error("⚠️ Diagnosis: The youth shows tendencies toward an Unhealthy Social Media Usage Habit.")
            else:
                st.success("✅ Diagnosis: The youth shows balanced tendencies indicative of a Healthy Usage Habit.")
        else:
            st.warning("Prediction cannot be completed because the machine learning model is missing.")

# --- Overview Page ---
if selected == 'Project Overview':
    st.title("About the System")
    st.write("""
    This intelligent system flags problematic online behaviors among teenagers using machine learning. 
    By assessing digital consumption habits against self-reported mental well-being indexes, 
    the architecture yields predictive analytics to support early intervention strategies.
    """)