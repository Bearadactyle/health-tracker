import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Set up page config
st.set_page_config(page_title="Health Baseline Tracker", layout="wide")
st.title("Physical Health Baseline Tracker (Cloud Version)")
st.write("Log your metrics from anywhere. Data syncs instantly to Google Sheets.")

# Establish connection to Google Sheets
# (The spreadsheet URL will be securely stored in the cloud settings)
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. METADATA & CONTEXT
st.header("1. Log Details & Context")
col_meta1, col_meta2 = st.columns(2)

with col_meta1:
    date = st.date_input("Date", datetime.today())
    sleep_hours = st.number_input("Sleep Duration (Hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)

with col_meta2:
    sleep_quality = st.selectbox(
        "Sleep Quality", 
        ["Great sleep", "Normal/Good sleep", "Groggy / Melatonin hangover", "Rough sleep", "Woke up from pain dream"]
    )
    appetite = st.selectbox("Appetite / Hunger Level", ["Normal", "Super hungry (Steroid effect)", "Poor / Nauseous"])

# 2. CORE PHYSICAL SLIDERS (0-10)
st.header("2. Core Physical Symptoms (0 = None, 10 = Severe)")
col1, col2 = st.columns(2)

with col1:
    lymph_nodes = st.slider("Swollen Lymph Nodes (Hardness/Sensitivity)", 0, 10, 0)
    tissue_swelling = st.slider("Surrounding Tissue Swelling (Around Nodes)", 0, 10, 0)
    torso_band = st.slider("Torso / Midsection Banding Swelling", 0, 10, 0)
    overall_swelling = st.slider("Overall Internal Swelling / Heat Sensation", 0, 10, 0)

with col2:
    spinal_pain = st.slider("Right-Side Spinal Pain (Dull/Constant)", 0, 10, 0)
    lower_back = st.slider("Lower Back Pain / Stiffness", 0, 10, 0)
    nerve_tightness = st.slider("Nerve Tightness / Leg Fatigue ('Rubber Bands')", 0, 10, 0)
    hand_arm_pain = st.slider("Hand & Arm Nerve Pain/Tightness", 0, 10, 0)

# 3. SYSTEMIC & EMOTIONAL SLIDERS (0-10)
st.header("3. Systemic & Nervous System Impact")
col3, col4 = st.columns(2)

with col3:
    numbness = st.slider("Numbness Severity (Toes/Feet/Legs)", 0, 10, 0)
    fatigue = st.slider("Extreme Fatigue / Sudden Shutdowns", 0, 10, 0)

with col4:
    anxiety_mood = st.slider("Anxiety / Irritability / Emotional Sensitivity", 0, 10, 0)
    sweating = st.slider("Heavy Sweating (Hands/Feet/Inflammation Spikes)", 0, 10, 0)

# 4. DYNAMIC CHECKBOXES (TRIGGERS)
st.header("4. Daily Triggers & Variables")
c1, c2, c3 = st.columns(3)
with c1:
    drive_short = st.checkbox("Short Drive (15-30 mins)")
    drive_long = st.checkbox("Long Drive (1+ hours)")
with c2:
    steroid_taper = st.checkbox("Steroid Taper Step-Down Day")
    med_issue = st.checkbox("Missed / Delayed Medication Window")
with c3:
    heavy_activity = st.checkbox("Physical Activity (Lifting, Walking, Tasks)")
    diet_flare = st.checkbox("Dietary Trigger (Sushi, High Sodium, etc.)")
    extreme_heat = st.checkbox("Extreme Weather / Heat (100°F+)")

# 5. ADDITIONAL TEXT NOTES
st.header("5. Additional Notes")
notes = st.text_area("Specific anomalies:")

# SAVE DATA BUTTON
st.markdown("---")
if st.button("Log Daily Data", type="primary"):
    data_row = {
        "Date": str(date), "Sleep Hours": sleep_hours, "Sleep Quality": sleep_quality, "Appetite": appetite,
        "Lymph Nodes": lymph_nodes, "Tissue Swelling": tissue_swelling, "Torso Banding": torso_band,
        "Overall Swelling": overall_swelling, "Right Spinal Pain": spinal_pain, "Lower Back Pain": lower_back,
        "Leg Nerve Tightness": nerve_tightness, "Hand Arm Pain": hand_arm_pain, "Numbness Severity": numbness,
        "Fatigue": fatigue, "Anxiety/Irritability": anxiety_mood, "Sweating": sweating,
        "Trigger_ShortDrive": drive_short, "Trigger_LongDrive": drive_long, "Trigger_SteroidTaper": steroid_taper,
        "Trigger_MedIssue": med_issue, "Trigger_HeavyActivity": heavy_activity, "Trigger_Diet": diet_flare, "Trigger_Heat": extreme_heat,
        "Notes": notes
    }
    
    try:
        # Read current data from Google Sheet
        existing_data = conn.read()
        new_df = pd.DataFrame([data_row])
        updated_df = pd.concat([existing_data, new_df], ignore_index=True)
        
        # Update the live Google Sheet
        conn.update(data=updated_df)
        st.success("Successfully logged data directly to your online Google Sheet!")
        st.rerun()
    except Exception as e:
        st.error(f"Error saving to cloud storage: {e}")

# 6. HISTORY VIEWER SECTION
st.markdown("---")
st.header("📊 Past Logs History")
try:
    df_history = conn.read()
    if not df_history.empty:
        st.dataframe(df_history.iloc[::-1], use_container_width=True)
    else:
        st.info("No records found in the Google Sheet yet.")
except Exception as e:
    st.info("Awaiting live database link connection...")