import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# ====== App Theme & Configuration ======
st.set_page_config(
    page_title="FemCare Health",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pastel Feminine Theme
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #fff0f5 0%, #f8f0ff 100%);
        font-family: 'Arial', sans-serif;
    }
    .st-b7 {
        background-color: #ffd6e7 !important;
    }
    [data-testid="stHeader"] {
        background: #ff85a2;
    }
    .css-18e3th9 {
        padding: 2rem 5rem;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        background: white;
        border-left: 5px solid #ff85a2;
    }
    .card-header {
        font-size: 1.3em;
        font-weight: 600;
        color: #ff85a2;
        margin-bottom: 15px;
    }
    .stButton>button {
        background: #ff85a2;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #e76f8c;
        transform: scale(1.02);
    }
    [data-testid="stForm"] {
        background: rgba(255,255,255,0.8);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ====== Machine Learning Model ======
@st.cache_resource
def load_model():
    # Sample training data (replace with real dataset)
    data = {
        'age': [25, 30, 22, 28, 35, 27, 32],
        'bmi': [28, 32, 25, 30, 27, 29, 31],
        'irregular_periods': [1, 1, 0, 1, 1, 1, 0],
        'hair_growth': [1, 1, 0, 1, 0, 1, 0],
        'acne': [1, 1, 0, 1, 1, 1, 0],
        'risk_level': [2, 2, 0, 1, 1, 2, 0]  # 0=Low, 1=Medium, 2=High
    }
    df = pd.DataFrame(data)
    
    X = df.drop('risk_level', axis=1)
    y = df['risk_level']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = load_model()

# ====== App UI ======
def main():
    # Header Section
    st.title("🌸 FemCare Health")
    st.markdown("""
    <div style="background:linear-gradient(90deg, #ffebf3 0%, #f0f8ff 100%);padding:25px;border-radius:15px;margin-bottom:30px">
        <h3 style="color:#ff85a2;text-align:center">PCOS/PCOD Risk Assessment & Wellness Guide</h3>
    </div>
    """, unsafe_allow_html=True)

    # Input Form
    with st.form("health_form"):
        st.subheader("📋 Your Health Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="Enter your name")
            age = st.number_input("Age", 12, 50, 25)
            height = st.number_input("Height (cm)", 120, 200, 165)
            weight = st.number_input("Weight (kg)", 30, 150, 60)
        
        with col2:
            cycle = st.selectbox("Menstrual Cycle", ["Regular (28-35 days)", "Irregular (<28 or >35 days)"])
            flow = st.selectbox("Flow Intensity", ["Light", "Medium", "Heavy"])
            pain = st.selectbox("Menstrual Pain", ["None", "Mild", "Moderate", "Severe"])
        
        st.subheader("🚨 Symptoms Checklist")
        col3, col4 = st.columns(2)
        with col3:
            acne = st.checkbox("Acne/Oily Skin")
            hair_growth = st.checkbox("Excess Facial/Body Hair")
            hair_loss = st.checkbox("Hair Thinning/Loss")
            weight_gain = st.checkbox("Unexplained Weight Gain")
        
        with col4:
            cravings = st.checkbox("Food Cravings")
            fatigue = st.checkbox("Chronic Fatigue")
            mood_swings = st.checkbox("Mood Swings")
            insulin_resistance = st.checkbox("Dark Skin Patches")
        
        submitted = st.form_submit_button("🔍 Assess My Risk", use_container_width=True)

    # Prediction Results
    if submitted:
        # Calculate BMI
        bmi = round(weight / ((height/100) ** 2), 1)
        
        # Prepare features
        features = {
            'age': age,
            'bmi': bmi,
            'irregular_periods': 1 if "Irregular" in cycle else 0,
            'hair_growth': 1 if hair_growth else 0,
            'acne': 1 if acne else 0
        }
        
        # Predict risk
        risk_level = model.predict(pd.DataFrame([features]))[0]
        risk_labels = {0: "Low", 1: "Medium", 2: "High"}
        risk_text = risk_labels[risk_level]
        
        # Show results
        st.success(f"**Hello {name}!** Your assessment is ready.")
        st.markdown(f"""
        <div style="background:white;padding:20px;border-radius:15px;margin:20px 0">
            <h3 style="color:#ff85a2">Your PCOS/PCOD Risk: <span style="color:{'#4CAF50' if risk_level==0 else '#FFC107' if risk_level==1 else '#F44336'}">{risk_text}</span></h3>
            <p>BMI: {bmi} ({'Normal' if 18.5<=bmi<=24.9 else 'Underweight' if bmi<18.5 else 'Overweight'})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Visualization
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.barh([risk_text], [1], color=['#4CAF50' if risk_level==0 else '#FFC107' if risk_level==1 else '#F44336'])
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0, risk_text, ha='center', va='center', color='white', fontsize=24, fontweight='bold')
        st.pyplot(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("💖 Your Personalized Wellness Plan")
        
        with st.expander("🍽️ Dietary Recommendations", expanded=True):
            st.markdown("""
            - **Low Glycemic Index Foods**: Whole grains, legumes, non-starchy vegetables  
            - **Anti-inflammatory Foods**: Fatty fish, berries, turmeric, green tea  
            - **Avoid**: Processed foods, sugary drinks, refined carbs  
            - **Meal Timing**: Eat every 3-4 hours to regulate blood sugar
            """)
        
        with st.expander("💪 Fitness Plan"):
            st.markdown("""
            - **Cardio**: 30-45 mins daily (brisk walking, cycling)  
            - **Strength Training**: 2-3x/week (bodyweight exercises)  
            - **Yoga**: Poses like butterfly, cobra, and cat-cow  
            - **Consistency**: Aim for 150 mins/week minimum
            """)
        
        with st.expander("🧘 Mental Wellness"):
            st.markdown("""
            - **Meditation**: 10 mins daily (try guided apps)  
            - **Sleep Hygiene**: 7-9 hours, consistent schedule  
            - **Stress Management**: Journaling, deep breathing  
            - **Community Support**: Join PCOS support groups
            """)
        
        if risk_level >= 1:
            st.warning("ℹ️ Consider consulting a gynecologist or endocrinologist for further evaluation")

# Run the app
if __name__ == "__main__":
    main()