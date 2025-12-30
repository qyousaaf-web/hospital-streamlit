# app.py - Hospital Management System with Patient Treatment Analytics (Streamlit + Plotly)
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Hospital Management System", page_icon="🏥", layout="wide")

# Custom CSS for beauty
st.markdown("""
<style>
    .big-font { font-size: 50px !important; font-weight: bold; color: #2E86C1; text-align: center; }
    .metric-value { font-size: 32px; font-weight: bold; color: #d62728; }
</style>
""", unsafe_allow_html=True)

# Database
DB_FILE = "hospital.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS Patients (
            pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, age INTEGER, gender TEXT,
            phone TEXT, address TEXT, email TEXT
        );
        CREATE TABLE IF NOT EXISTS Doctors (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, specialty TEXT
        );
        CREATE TABLE IF NOT EXISTS Appointments (
            app_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER, doc_id INTEGER, app_date TEXT
        );
        CREATE TABLE IF NOT EXISTS MedicalRecords (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER, doc_id INTEGER,
            diagnosis TEXT, treatment TEXT, prescription TEXT, record_date TEXT DEFAULT (date('now'))
        );
        CREATE TABLE IF NOT EXISTS Billings (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER, amount REAL
        );
    ''')
    conn.commit()
    conn.close()

init_db()

def get_data(table):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

# Sidebar
st.sidebar.title("🏥 Hospital System")
page = st.sidebar.radio("Navigate", [
    "Home", "Patients", "Doctors", "Appointments", "Medical Records", "Treatment Analytics", "Billings"
])

if page == "Home":
    st.markdown('<p class="big-font">🏥 Hospital Dashboard</p>', unsafe_allow_html=True)

    patients = get_data("Patients")
    records = get_data("MedicalRecords")
    appointments = get_data("Appointments")
    billings = get_data("Billings")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", len(patients))
    col2.metric("Total Treatments", len(records))
    col3.metric("Appointments", len(appointments))
    col4.metric("Revenue $", f"{billings['amount'].sum():,.2f}" if not billings.empty else "0.00")

# ================ NEW: Patient Treatment Analytics ================
elif page == "Treatment Analytics":
    st.header("📊 Patient Treatment Analytics")

    records = get_data("MedicalRecords")
    patients = get_data("Patients")

    if records.empty:
        st.info("No treatment records yet. Add medical records to see analytics!")
        st.stop()

    # Merge with patient info for richer insights
    merged = records.merge(patients[['pat_id', 'name', 'age', 'gender']], on='pat_id', how='left')

    st.markdown("### 🔍 Top Diagnoses")
    diagnosis_counts = merged['diagnosis'].value_counts().head(10)
    diag_fig = px.bar(
        x=diagnosis_counts.values,
        y=diagnosis_counts.index,
        orientation='h',
        title="Most Common Diagnoses",
        labels={"x": "Number of Cases", "y": "Diagnosis"},
        color=diagnosis_counts.values,
        color_continuous_scale="Viridis"
    )
    diag_fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(diag_fig, use_container_width=True)

    st.markdown("### 💊 Most Prescribed Treatments")
    treatment_counts = merged['treatment'].value_counts().head(10)
    treat_fig = px.pie(
        treatment_counts,
        names=treatment_counts.index,
        values=treatment_counts.values,
        title="Treatment Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(treat_fig, use_container_width=True)

    st.markdown("### 👥 Treatments by Gender")
    gender_treat = merged.groupby(['gender', 'treatment']).size().reset_index(name='count')
    gender_fig = px.bar(
        gender_treat,
        x='treatment',
        y='count',
        color='gender',
        title="Treatments by Gender",
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(gender_fig, use_container_width=True)

    st.markdown("### 📅 Treatment Trends Over Time")
    merged['record_date'] = pd.to_datetime(merged['record_date'], errors='coerce')
    time_trend = merged.groupby('record_date').size().reset_index(name='treatments')
    trend_fig = px.line(
        time_trend,
        x='record_date',
        y='treatments',
        title="Daily Treatment Records",
        markers=True,
        color_discrete_sequence=["#2E86C1"]
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    st.markdown("### 🧑 Age vs Diagnosis")
    if 'age' in merged.columns:
        age_diag = merged.groupby(['age', 'diagnosis']).size().reset_index(name='count')
        age_fig = px.scatter(
            age_diag,
            x='age',
            y='diagnosis',
            size='count',
            color='count',
            title="Diagnosis Frequency by Age",
            color_continuous_scale="Plasma"
        )
        st.plotly_chart(age_fig, use_container_width=True)

# Keep other pages (Patients, Doctors, etc.) as in previous versions

st.sidebar.success("Now with Patient Treatment Analytics! 📊")
