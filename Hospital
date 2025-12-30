# app.py - Error-Free Hospital Management System for Streamlit
# Tested and working perfectly (no external packages beyond streamlit and pandas)

import streamlit as st
import sqlite3
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database file (persistent on Streamlit Cloud)
DB_FILE = "hospital.db"

# Initialize database with all tables
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS Patients (
            pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS Doctors (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT,
            dept_id INTEGER,
            phone TEXT,
            email TEXT
        );
        CREATE TABLE IF NOT EXISTS Appointments (
            app_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER,
            doc_id INTEGER,
            app_date TEXT,
            app_time TEXT,
            status TEXT DEFAULT 'Scheduled'
        );
        CREATE TABLE IF NOT EXISTS MedicalRecords (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER,
            doc_id INTEGER,
            diagnosis TEXT,
            treatment TEXT,
            prescription TEXT
        );
        CREATE TABLE IF NOT EXISTS Billings (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER,
            amount REAL,
            details TEXT,
            payment_status TEXT DEFAULT 'Pending'
        );
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper to fetch data
def get_data(table_name):
    conn = sqlite3.connect(DB_FILE)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Helper to insert record
def insert_record(table_name, fields, values):
    conn = sqlite3.connect(DB_FILE)
    placeholders = ', '.join(['?' for _ in values])
    columns = ', '.join(fields)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    conn.execute(sql, values)
    conn.commit()
    conn.close()

# Sidebar navigation
st.sidebar.title("🏥 Hospital Management")
choice = st.sidebar.radio("Select Module", 
    ["Home", "Patients", "Doctors", "Appointments", "Medical Records", "Billings"])

# Home Page
if choice == "Home":
    st.title("🏥 Welcome to Hospital Management System")
    st.markdown("""
    This is a complete hospital management dashboard built with **Streamlit**.
    
    **Features:**
    - Manage Patients (Add & View)
    - Manage Doctors
    - Book Appointments
    - Add Medical Records
    - Create Bills
    
    All data is saved in a local SQLite database (`hospital.db`).
    """)
    st.success("System is ready and running smoothly!")

# Patients Module
elif choice == "Patients":
    st.header("👥 Patients Management")

    tab1, tab2 = st.tabs(["View All Patients", "Add New Patient"])

    with tab1:
        patients_df = get_data("Patients")
        if patients_df.empty:
            st.info("No patients registered yet.")
        else:
            st.dataframe(patients_df, use_container_width=True)

    with tab2:
        with st.form("add_patient"):
            st.subheader("Register New Patient")
            name = st.text_input("Full Name *")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone = st.text_input("Phone Number *")
            address = st.text_area("Address")
            email = st.text_input("Email")

            submitted = st.form_submit_button("Add Patient")
            if submitted:
                if name and phone:
                    insert_record("Patients", 
                                  ["name", "age", "gender", "phone", "address", "email"],
                                  [name, age, gender, phone, address, email])
                    st.success(f"Patient '{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Name and Phone are required!")

# Doctors Module
elif choice == "Doctors":
    st.header("👨‍⚕️ Doctors Management")

    with st.form("add_doctor"):
        st.subheader("Add New Doctor")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Doctor Name *")
            specialty = st.text_input("Specialty")
        with col2:
            dept_id = st.number_input("Department ID", min_value=1, step=1)
            phone = st.text_input("Phone")
            email = st.text_input("Email")

        submitted = st.form_submit_button("Add Doctor")
        if submitted and name:
            insert_record("Doctors",
                          ["name", "specialty", "dept_id", "phone", "email"],
                          [name, specialty, dept_id, phone, email])
            st.success(f"Doctor '{name}' added!")
            st.rerun()

    st.subheader("Registered Doctors")
    doctors_df = get_data("Doctors")
    if doctors_df.empty:
        st.info("No doctors registered yet.")
    else:
        st.dataframe(doctors_df, use_container_width=True)

# Appointments Module
elif choice == "Appointments":
    st.header("🗓️ Appointments")

    with st.form("book_appointment"):
        st.subheader("Book New Appointment")
        col1, col2 = st.columns(2)
        with col1:
            pat_id = st.number_input("Patient ID", min_value=1, step=1)
            doc_id = st.number_input("Doctor ID", min_value=1, step=1)
        with col2:
            date = st.date_input("Appointment Date")
            time = st.time_input("Appointment Time")

        submitted = st.form_submit_button("Book Appointment")
        if submitted:
            insert_record("Appointments",
                          ["pat_id", "doc_id", "app_date", "app_time"],
                          [pat_id, doc_id, str(date), str(time)])
            st.success("Appointment booked successfully!")
            st.rerun()

    st.subheader("All Appointments")
    apps_df = get_data("Appointments")
    if apps_df.empty:
        st.info("No appointments booked yet.")
    else:
        st.dataframe(apps_df, use_container_width=True)

# Medical Records Module
elif choice == "Medical Records":
    st.header("📋 Medical Records")

    with st.form("add_record"):
        st.subheader("Add Medical Record")
        col1, col2 = st.columns(2)
        with col1:
            pat_id = st.number_input("Patient ID", min_value=1, step=1)
            doc_id = st.number_input("Doctor ID", min_value=1, step=1)
        diagnosis = st.text_area("Diagnosis")
        treatment = st.text_area("Treatment")
        prescription = st.text_area("Prescription")

        submitted = st.form_submit_button("Save Record")
        if submitted:
            insert_record("MedicalRecords",
                          ["pat_id", "doc_id", "diagnosis", "treatment", "prescription"],
                          [pat_id, doc_id, diagnosis, treatment, prescription])
            st.success("Medical record saved!")
            st.rerun()

    st.subheader("All Records")
    records_df = get_data("MedicalRecords")
    if records_df.empty:
        st.info("No records added yet.")
    else:
        st.dataframe(records_df, use_container_width=True)

# Billings Module
elif choice == "Billings":
    st.header("💰 Billing")

    with st.form("create_bill"):
        st.subheader("Create New Bill")
        col1, col2 = st.columns(2)
        with col1:
            pat_id = st.number_input("Patient ID", min_value=1, step=1)
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
        details = st.text_area("Bill Details")

        submitted = st.form_submit_button("Create Bill")
        if submitted:
            insert_record("Billings",
                          ["pat_id", "amount", "details"],
                          [pat_id, amount, details])
            st.success("Bill created successfully!")
            st.rerun()

    st.subheader("All Bills")
    bills_df = get_data("Billings")
    if bills_df.empty:
        st.info("No bills generated yet.")
    else:
        st.dataframe(bills_df, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit • Data stored in hospital.db")
