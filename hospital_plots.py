# app.py - Hospital Management System with More Responsive Form Layout
import streamlit as st
import sqlite3
import pandas as pd

# Page config
st.set_page_config(page_title="Hospital Management System", page_icon="🏥", layout="wide")

# Custom CSS for responsive & beautiful forms
st.markdown("""
<style>
    /* Responsive form container */
    .form-container {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 0 auto;
    }

    /* Responsive columns */
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column !important;
        }
    }

    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 10px;
        font-size: 16px;
    }

    /* Button styling */
    .stButton > button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        width: 100%;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #218838;
    }

    /* Labels */
    label {
        font-weight: bold;
        color: #495057;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
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
            pat_id INTEGER, doc_id INTEGER,
            app_date TEXT, app_time TEXT, status TEXT DEFAULT 'Scheduled'
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

def add_appointment(pat_id, doc_id, app_date, app_time, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO Appointments (pat_id, doc_id, app_date, app_time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (pat_id, doc_id, str(app_date), str(app_time), status))
    conn.commit()
    conn.close()

# Sidebar
st.sidebar.title("🏥 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Appointments"])

if page == "Appointments":
    st.header("🗓️ Appointment Scheduling")

    tab1, tab2 = st.tabs(["📅 View Appointments", "➕ Schedule New"])

    with tab1:
        st.subheader("All Appointments")
        df = get_data("Appointments")
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #1E88E5;">🗓️ Schedule Appointment</h3>', unsafe_allow_html=True)

        with st.form("appointment_form", clear_on_submit=True):
            # Responsive columns for inputs
            col1, col2 = st.columns([1, 1])
            with col1:
                pat_id = st.number_input("**Patient ID**", min_value=1, step=1)
            with col2:
                doc_id = st.number_input("**Doctor ID**", min_value=1, step=1)

            col3, col4 = st.columns([1, 1])
            with col3:
                app_date = st.date_input("**Date**", value=None)
            with col4:
                app_time = st.time_input("**Time**", value=None)

            status = st.selectbox("**Status**", ["Scheduled", "Confirmed", "Completed", "Cancelled"])

            submitted = st.form_submit_button("📅 Schedule Appointment")

            if submitted:
                if pat_id and doc_id and app_date and app_time:
                    add_appointment(pat_id, doc_id, app_date, app_time, status)
                    st.markdown('<div class="success-box">✅ Appointment scheduled successfully!</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("⚠️ All fields are required!")

        st.markdown('</div>', unsafe_allow_html=True)

# Other pages (Home, etc.) can be added similarly

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit")
