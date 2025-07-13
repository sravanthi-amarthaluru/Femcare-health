import streamlit as st
import pandas as pd
import numpy as np

# ====== App Configuration ======
st.set_page_config(
    page_title="FemCare Health",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== Custom CSS ======
def load_css():
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

load_css()

# ====== Risk Calculation ======
def calculate_risk(age, bmi, symptoms):
    """Simple risk calculation without ML dependencies"""
    risk_score = 0
    
    # Weighting factors
    if bmi > 25: risk_score += 1.5
    if age < 25: risk_score += 0.5
    if symptoms['irregular']: risk_score += 1.5
    if symptoms['hair_growth']: risk_score += 1
    if symptoms['acne']: risk_score += 1
    if symptoms['weight_gain']: risk_score += 1
    if symptoms['fatigue']: risk_score += 0.5
    
    if risk_score >= 4: return 2  # High
    elif risk_score >= 2: return 1  # Medium
    else: return 0  # Low

# ====== App UI ======
def main():
    # Header Section
    st.title("🌸 FemCare Health")
    st.markdown("""
    <div style="background:linear-gradient(90deg, #ffebf3 0%, #f0f8ff 100%);
                padding:25px;
                border-radius:15px;
                margin-bottom:30px">
        <h3 style="color:#ff85a2;text-align:center">
            PCOS/PCOD Risk Assessment & Wellness Guide
        </h3>
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
            cycle = st.selectbox("Menstrual Cycle", 
                               ["Regular (28-35 days)", 
                                "Irregular (<28 or >35 days)"])
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
        
        submitted = st.form_submit_button("🔍 Assess My Risk", 
                                        use_container_width=True)

    # Results Section
    if submitted:
        # Calculate BMI
        bmi = round(weight / ((height/100) ** 2), 1)
        
        # Prepare symptoms
        symptoms = {
            'irregular': "Irregular" in cycle,
            'hair_growth': hair_growth,
            'acne': acne,
            'weight_gain': weight_gain,
            'fatigue': fatigue
        }
        
        # Calculate risk
        risk_level = calculate_risk(age, bmi, symptoms)
        risk_labels = ["Low", "Medium", "High"]
        risk_colors = ["#4CAF50", "#FFC107", "#F44336"]
        risk_text = risk_labels[risk_level]
        
        # Display results
        st.success(f"**Hello {name}!** Your assessment is ready.")
        st.markdown(f"""
        <div style="background:white;
                    padding:20px;
                    border-radius:15px;
                    margin:20px 0">
            <h3 style="color:#ff85a2">
                Your PCOS/PCOD Risk: 
                <span style="color:{risk_colors[risk_level]}">
                    {risk_text}
                </span>
            </h3>
            <p>BMI: {bmi} ({'Normal' if 18.5<=bmi<=24.9 else 'Underweight' if bmi<18.5 else 'Overweight'})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual indicator
        st.markdown(f"""
        <div style="background:{risk_colors[risk_level]};
                    color:white;
                    padding:30px;
                    border-radius:10px;
                    text-align:center;
                    font-size:28px;
                    font-weight:bold;
                    margin:20px 0">
            {risk_text} Risk Level
        </div>
        """, unsafe_allow_html=True)
        
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