# app.py - Enhanced Hospital Management System with Colors, Icons & CRUD Buttons
import streamlit as st
import sqlite3
import pandas as pd

# --------------------- Page Config & Custom CSS ---------------------
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colors, buttons, and styling
st.markdown("""
<style>
    .big-title {
        font-size: 3rem !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .module-header {
        font-size: 2rem;
        color: #1976D2;
        padding: 0.5rem;
        border-left: 5px solid #42A5F5;
    }
    .stButton>button {
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .delete-btn { background-color: #E53935; color: white; }
    .update-btn { background-color: #FFB300; color: white; }
    .search-btn { background-color: #43A047; color: white; }
    .add-btn { background-color: #1E88E5; color: white; }
    .card {
        background-color: #f8fdff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --------------------- Database Setup ---------------------
DB_FILE = "hospital.db"

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

# --------------------- Helper Functions ---------------------
def get_data(table_name):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def insert_record(table_name, fields, values):
    conn = sqlite3.connect(DB_FILE)
    placeholders = ', '.join(['?' for _ in values])
    columns = ', '.join(fields)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    conn.execute(sql, values)
    conn.commit()
    conn.close()

def delete_record(table_name, id_column, record_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(f"DELETE FROM {table_name} WHERE {id_column} = ?", (record_id,))
    conn.commit()
    conn.close()

def update_record(table_name, id_column, record_id, fields, values):
    conn = sqlite3.connect(DB_FILE)
    set_clause = ', '.join([f"{f} = ?" for f in fields])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
    values.append(record_id)
    conn.execute(sql, values)
    conn.commit()
    conn.close()

def search_records(table_name, column, query):
    conn = sqlite3.connect(DB_FILE)
    query_sql = f"SELECT * FROM {table_name} WHERE {column} LIKE ?"
    df = pd.read_sql_query(query_sql, conn, params=(f"%{query}%",))
    conn.close()
    return df

def get_record(table_name, id_column, record_id):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute(f"SELECT * FROM {table_name} WHERE {id_column} = ?", (record_id,)).fetchone()
    conn.close()
    return row

# --------------------- Sidebar Navigation ---------------------
st.sidebar.image("https://img.icons8.com/fluency/96/000000/hospital.png", width=100)
st.sidebar.markdown("<h1 style='text-align: center; color: #1976D2;'>🏥 HMS</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

choice = st.sidebar.radio("**Navigation**", 
    ["🏠 Home", "👥 Patients", "👨‍⚕️ Doctors", "🗓️ Appointments", "📋 Medical Records", "💰 Billings"],
    label_visibility="collapsed")

# --------------------- Main Content ---------------------
if choice == "🏠 Home":
    st.markdown('<div class="big-title">🏥 Hospital Management System</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3rem;'>A modern, efficient, and user-friendly healthcare dashboard</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Patients", len(get_data("Patients")), delta="Active")
    with col2:
        st.metric("Doctors Available", len(get_data("Doctors")))
    with col3:
        st.metric("Appointments Today", len(get_data("Appointments")))

    st.markdown("### ✨ Key Features")
    st.success("""
    - Full CRUD operations (Create, Read, Update, Delete)  
    - Search functionality in all modules  
    - Beautiful UI with colors and icons  
    - Persistent SQLite storage  
    - Responsive layout
    """)

elif choice == "👥 Patients":
    st.markdown('<div class="module-header">👥 Patients Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View & Manage", "➕ Add New Patient"])

    with tab1:
        search_query = st.text_input("🔍 Search by Name or Phone", "")
        df = search_records("Patients", "name", search_query) if search_query else get_data("Patients")
        
        if df.empty:
            st.info("😔 No patients found.")
        else:
            st.dataframe(df, use_container_width=True)
            
        # Delete
        st.subheader("🗑️ Delete Patient")
        del_id = st.number_input("Patient ID to Delete", min_value=1, step=1)
        if st.button("Delete Patient", type="primary"):
            delete_record("Patients", "pat_id", del_id)
            st.success("Patient deleted successfully!")
            st.rerun()

        # Update
        st.subheader("✏️ Update Patient")
        update_id = st.number_input("Patient ID to Update", min_value=1, step=1)
        if update_id:
            row = get_record("Patients", "pat_id", update_id)
            if row:
                with st.form("update_patient"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name", value=row[1])
                        age = st.number_input("Age", min_value=0, max_value=120, value=row[2])
                        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(row[3]))
                    with col2:
                        phone = st.text_input("Phone Number", value=row[4])
                        email = st.text_input("Email", value=row[6])
                        address = st.text_area("Address", value=row[5])
                    
                    if st.form_submit_button("Update Patient"):
                        update_record("Patients", "pat_id", update_id,
                                      ["name", "age", "gender", "phone", "address", "email"],
                                      [name, age, gender, phone, address, email])
                        st.success("Patient updated successfully!")
                        st.rerun()
            else:
                st.error("Patient ID not found.")

    with tab2:
        with st.form("add_patient", clear_on_submit=True):
            st.subheader("➕ Register New Patient")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *")
                age = st.number_input("Age", min_value=0, max_value=120)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            with col2:
                phone = st.text_input("Phone Number *")
                email = st.text_input("Email")
                address = st.text_area("Address")
            
            if st.form_submit_button("✅ Add Patient", use_container_width=True):
                if name and phone:
                    insert_record("Patients", ["name", "age", "gender", "phone", "address", "email"],
                                  [name, age, gender, phone, address, email])
                    st.success(f"Patient '{name}' registered successfully! 🎉")
                    st.rerun()
                else:
                    st.error("Name and Phone are required!")

elif choice == "👨‍⚕️ Doctors":
    st.markdown('<div class="module-header">👨‍⚕️ Doctors Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View & Manage", "➕ Add New Doctor"])

    with tab1:
        search_doc = st.text_input("🔍 Search Doctor by Name or Specialty")
        df = search_records("Doctors", "name", search_doc) if search_doc else get_data("Doctors")
        
        if df.empty:
            st.info("No doctors found.")
        else:
            st.dataframe(df, use_container_width=True)
        
        # Delete
        st.subheader("🗑️ Delete Doctor")
        del_id = st.number_input("Doctor ID to Delete", min_value=1, step=1)
        if st.button("Delete Doctor", type="primary"):
            delete_record("Doctors", "doc_id", del_id)
            st.success("Doctor deleted successfully!")
            st.rerun()

        # Update
        st.subheader("✏️ Update Doctor")
        update_id = st.number_input("Doctor ID to Update", min_value=1, step=1)
        if update_id:
            row = get_record("Doctors", "doc_id", update_id)
            if row:
                with st.form("update_doctor"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Doctor Name", value=row[1])
                        specialty = st.text_input("Specialty", value=row[2])
                    with col2:
                        dept_id = st.number_input("Department ID", min_value=1, value=row[3])
                        phone = st.text_input("Phone", value=row[4])
                        email = st.text_input("Email", value=row[5])
                    
                    if st.form_submit_button("Update Doctor"):
                        update_record("Doctors", "doc_id", update_id,
                                      ["name", "specialty", "dept_id", "phone", "email"],
                                      [name, specialty, dept_id, phone, email])
                        st.success("Doctor updated successfully!")
                        st.rerun()
            else:
                st.error("Doctor ID not found.")

    with tab2:
        with st.form("add_doctor"):
            st.subheader("➕ Add New Doctor")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Doctor Name *")
                specialty = st.text_input("Specialty (e.g., Cardiology)")
            with col2:
                dept_id = st.number_input("Department ID", min_value=1)
                phone = st.text_input("Phone")
                email = st.text_input("Email")
            
            if st.form_submit_button("✅ Register Doctor"):
                if name:
                    insert_record("Doctors", ["name", "specialty", "dept_id", "phone", "email"],
                                  [name, specialty, dept_id, phone, email])
                    st.success(f"Dr. {name} added successfully! 👨‍⚕️")
                    st.rerun()
                else:
                    st.error("Doctor Name is required!")

elif choice == "🗓️ Appointments":
    st.markdown('<div class="module-header">🗓️ Appointments Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View & Manage", "➕ Book New Appointment"])

    with tab1:
        search_query = st.text_input("🔍 Search by Date or Status", "")
        df = search_records("Appointments", "app_date", search_query) if search_query else get_data("Appointments")
        
        if df.empty:
            st.info("No appointments found.")
        else:
            st.dataframe(df, use_container_width=True)
        
        # Delete
        st.subheader("🗑️ Delete Appointment")
        del_id = st.number_input("Appointment ID to Delete", min_value=1, step=1)
        if st.button("Delete Appointment", type="primary"):
            delete_record("Appointments", "app_id", del_id)
            st.success("Appointment deleted successfully!")
            st.rerun()

        # Update
        st.subheader("✏️ Update Appointment")
        update_id = st.number_input("Appointment ID to Update", min_value=1, step=1)
        if update_id:
            row = get_record("Appointments", "app_id", update_id)
            if row:
                with st.form("update_appointment"):
                    col1, col2 = st.columns(2)
                    with col1:
                        pat_id = st.number_input("Patient ID", min_value=1, value=row[1])
                        doc_id = st.number_input("Doctor ID", min_value=1, value=row[2])
                    with col2:
                        app_date = st.date_input("Appointment Date", value=pd.to_datetime(row[3]))
                        app_time = st.time_input("Appointment Time", value=pd.to_datetime(row[4]).time())
                        status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"], index=["Scheduled", "Completed", "Cancelled"].index(row[5]))
                    
                    if st.form_submit_button("Update Appointment"):
                        update_record("Appointments", "app_id", update_id,
                                      ["pat_id", "doc_id", "app_date", "app_time", "status"],
                                      [pat_id, doc_id, str(app_date), str(app_time), status])
                        st.success("Appointment updated successfully!")
                        st.rerun()
            else:
                st.error("Appointment ID not found.")

    with tab2:
        with st.form("add_appointment"):
            st.subheader("➕ Book New Appointment")
            col1, col2 = st.columns(2)
            with col1:
                pat_id = st.number_input("Patient ID *", min_value=1)
                doc_id = st.number_input("Doctor ID *", min_value=1)
            with col2:
                app_date = st.date_input("Appointment Date")
                app_time = st.time_input("Appointment Time")
                status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])
            
            if st.form_submit_button("✅ Book Appointment"):
                if pat_id and doc_id:
                    insert_record("Appointments", ["pat_id", "doc_id", "app_date", "app_time", "status"],
                                  [pat_id, doc_id, str(app_date), str(app_time), status])
                    st.success("Appointment booked successfully! 📅")
                    st.rerun()
                else:
                    st.error("Patient ID and Doctor ID are required!")

elif choice == "📋 Medical Records":
    st.markdown('<div class="module-header">📋 Medical Records Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View & Manage", "➕ Add New Record"])

    with tab1:
        search_query = st.text_input("🔍 Search by Diagnosis", "")
        df = search_records("MedicalRecords", "diagnosis", search_query) if search_query else get_data("MedicalRecords")
        
        if df.empty:
            st.info("No records found.")
        else:
            st.dataframe(df, use_container_width=True)
        
        # Delete
        st.subheader("🗑️ Delete Record")
        del_id = st.number_input("Record ID to Delete", min_value=1, step=1)
        if st.button("Delete Record", type="primary"):
            delete_record("MedicalRecords", "record_id", del_id)
            st.success("Record deleted successfully!")
            st.rerun()

        # Update
        st.subheader("✏️ Update Record")
        update_id = st.number_input("Record ID to Update", min_value=1, step=1)
        if update_id:
            row = get_record("MedicalRecords", "record_id", update_id)
            if row:
                with st.form("update_record"):
                    col1, col2 = st.columns(2)
                    with col1:
                        pat_id = st.number_input("Patient ID", min_value=1, value=row[1])
                        doc_id = st.number_input("Doctor ID", min_value=1, value=row[2])
                    with col2:
                        pass  # No additional fields
                    diagnosis = st.text_area("Diagnosis", value=row[3])
                    treatment = st.text_area("Treatment", value=row[4])
                    prescription = st.text_area("Prescription", value=row[5])
                    
                    if st.form_submit_button("Update Record"):
                        update_record("MedicalRecords", "record_id", update_id,
                                      ["pat_id", "doc_id", "diagnosis", "treatment", "prescription"],
                                      [pat_id, doc_id, diagnosis, treatment, prescription])
                        st.success("Record updated successfully!")
                        st.rerun()
            else:
                st.error("Record ID not found.")

    with tab2:
        with st.form("add_record"):
            st.subheader("➕ Add New Medical Record")
            col1, col2 = st.columns(2)
            with col1:
                pat_id = st.number_input("Patient ID *", min_value=1)
                doc_id = st.number_input("Doctor ID *", min_value=1)
            with col2:
                pass
            diagnosis = st.text_area("Diagnosis")
            treatment = st.text_area("Treatment")
            prescription = st.text_area("Prescription")
            
            if st.form_submit_button("✅ Save Record"):
                if pat_id and doc_id:
                    insert_record("MedicalRecords", ["pat_id", "doc_id", "diagnosis", "treatment", "prescription"],
                                  [pat_id, doc_id, diagnosis, treatment, prescription])
                    st.success("Medical record saved successfully! 📋")
                    st.rerun()
                else:
                    st.error("Patient ID and Doctor ID are required!")

elif choice == "💰 Billings":
    st.markdown('<div class="module-header">💰 Billings Management</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View & Manage", "➕ Create New Bill"])

    with tab1:
        search_query = st.text_input("🔍 Search by Details or Status", "")
        df = search_records("Billings", "details", search_query) if search_query else get_data("Billings")
        
        if df.empty:
            st.info("No bills found.")
        else:
            st.dataframe(df, use_container_width=True)
        
        # Delete
        st.subheader("🗑️ Delete Bill")
        del_id = st.number_input("Bill ID to Delete", min_value=1, step=1)
        if st.button("Delete Bill", type="primary"):
            delete_record("Billings", "bill_id", del_id)
            st.success("Bill deleted successfully!")
            st.rerun()

        # Update
        st.subheader("✏️ Update Bill")
        update_id = st.number_input("Bill ID to Update", min_value=1, step=1)
        if update_id:
            row = get_record("Billings", "bill_id", update_id)
            if row:
                with st.form("update_bill"):
                    col1, col2 = st.columns(2)
                    with col1:
                        pat_id = st.number_input("Patient ID", min_value=1, value=row[1])
                        amount = st.number_input("Amount ($)", min_value=0.0, value=float(row[2]), format="%.2f")
                    with col2:
                        payment_status = st.selectbox("Payment Status", ["Pending", "Paid", "Overdue"], index=["Pending", "Paid", "Overdue"].index(row[4]))
                    details = st.text_area("Details", value=row[3])
                    
                    if st.form_submit_button("Update Bill"):
                        update_record("Billings", "bill_id", update_id,
                                      ["pat_id", "amount", "details", "payment_status"],
                                      [pat_id, amount, details, payment_status])
                        st.success("Bill updated successfully!")
                        st.rerun()
            else:
                st.error("Bill ID not found.")

    with tab2:
        with st.form("add_bill"):
            st.subheader("➕ Create New Bill")
            col1, col2 = st.columns(2)
            with col1:
                pat_id = st.number_input("Patient ID *", min_value=1)
                amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
            with col2:
                payment_status = st.selectbox("Payment Status", ["Pending", "Paid", "Overdue"])
            details = st.text_area("Details")
            
            if st.form_submit_button("✅ Create Bill"):
                if pat_id:
                    insert_record("Billings", ["pat_id", "amount", "details", "payment_status"],
                                  [pat_id, amount, details, payment_status])
                    st.success("Bill created successfully! 💰")
                    st.rerun()
                else:
                    st.error("Patient ID is required!")

# --------------------- Footer ---------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    Built with ❤️ using <strong>Streamlit</strong> • Data stored securely in <code>hospital.db</code>
</div>
""", unsafe_allow_html=True)
