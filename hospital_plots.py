# Enhanced Medical Records Form - Beautiful & Professional
elif page == "Medical Records":
    st.header("📋 Medical Records Management")

    tab1, tab2 = st.tabs(["📋 View All Records", "🩺 Add New Record"])

    with tab1:
        st.subheader("Registered Medical Records")
        records_df = get_data("MedicalRecords")
        if records_df.empty:
            st.info("No medical records added yet. Start by adding one! 👇")
        else:
            st.dataframe(records_df, use_container_width=True)

    with tab2:
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 15px; border-left: 6px solid #4CAF50; margin-bottom: 20px;">
            <h3 style="color: #2E86C1; margin:0;">🩺 Add New Medical Record</h3>
            <p style="color: #555; margin:5px 0 0 0;">Fill in the details below to document patient treatment</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("medical_record_form", clear_on_submit=True):
            # Patient & Doctor Section
            st.markdown("### 👤 Patient & Doctor Information")
            col1, col2 = st.columns(2)
            with col1:
                pat_id = st.number_input("**Patient ID**", min_value=1, step=1, help="Enter registered Patient ID")
            with col2:
                doc_id = st.number_input("**Doctor ID**", min_value=1, step=1, help="Enter attending Doctor ID")

            st.markdown("---")

            # Diagnosis Section
            st.markdown("### 🩺 Diagnosis")
            diagnosis = st.text_area(
                "",
                height=120,
                placeholder="Describe symptoms, findings, and confirmed diagnosis...",
                help="Be detailed and specific"
            )

            # Treatment Section
            st.markdown("### 💉 Treatment Plan")
            treatment = st.text_area(
                "",
                height=120,
                placeholder="Outline procedures, therapies, or interventions performed...",
                help="Include duration and follow-up if applicable"
            )

            # Prescription Section
            st.markdown("### 💊 Prescription & Medications")
            prescription = st.text_area(
                "",
                height=120,
                placeholder="List medications, dosage, frequency, and duration (e.g., Amoxicillin 500mg - 3 times daily for 7 days)...",
                help="Include any special instructions"
            )

            st.markdown("---")

            # Submit Button - Big, Green, Centered
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button(
                    "💾 Save Medical Record",
                    type="primary",
                    use_container_width=True
                )

            if submitted:
                if pat_id and doc_id and diagnosis.strip():
                    add_medical_record(pat_id, doc_id, diagnosis, treatment, prescription)
                    st.success("✅ Medical record saved successfully!")
                    st.balloons()  # Fun celebration animation
                    st.rerun()
                else:
                    st.error("⚠️ Patient ID, Doctor ID, and Diagnosis are required fields!")
