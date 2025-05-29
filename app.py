import streamlit as st

# --- Age-based BP reference logic ---
st.title("Pediatric Blood Pressure Reference Centile Tool")
st.markdown("Get reference systolic/diastolic blood pressure values for pediatric patients aged 26 weeks PMA to 17 years.")

age_unit = st.selectbox("Select age unit", ["Postmenstrual Weeks", "Months", "Years"])
sex = st.selectbox("Sex", ["Male", "Female"])

if age_unit == "Postmenstrual Weeks":
    pma = st.number_input("Postmenstrual Age (weeks)", min_value=26, max_value=44, value=30)
    if st.button("Get Centiles"):
        # Example static data (replace with real neonatal data if needed)
        sbp_95 = 70 + (pma - 26) * 1.2
        dbp_95 = 40 + (pma - 26) * 1.0
        sbp_99 = sbp_95 + 5
        dbp_99 = dbp_95 + 5
        sbp_50 = sbp_95 - 15
        dbp_50 = dbp_95 - 10

        st.subheader("Reference BP Values:")
        st.markdown(f"- **50th percentile:** {round(sbp_50)}/{round(dbp_50)} mmHg")
        st.markdown(f"- **90th percentile:** —")
        st.markdown(f"- **95th percentile:** {round(sbp_95)}/{round(dbp_95)} mmHg")
        st.markdown(f"- **99th percentile:** {round(sbp_99)}/{round(dbp_99)} mmHg")

elif age_unit == "Months":
    age_months = st.number_input("Age (months)", min_value=0, max_value=23, value=12)
    if age_months == 12:
        weight = st.number_input("Weight (kg)", min_value=2.0, max_value=20.0, value=9.0)
        if st.button("Get Centiles"):
            # Use static representative data (you may expand with real chart data)
            if sex == "Male":
                sbp_50, dbp_50 = 90, 55
                sbp_90, dbp_90 = 100, 65
                sbp_95, dbp_95 = 105, 67
            else:
                sbp_50, dbp_50 = 88, 52
                sbp_90, dbp_90 = 98, 62
                sbp_95, dbp_95 = 103, 64

            sbp_stage2 = sbp_95 + 12
            dbp_stage2 = dbp_95 + 12

            st.subheader("Reference BP Values:")
            st.markdown(f"- **50th percentile:** {sbp_50}/{dbp_50} mmHg")
            st.markdown(f"- **90th percentile:** {sbp_90}/{dbp_90} mmHg")
            st.markdown(f"- **95th percentile:** {sbp_95}/{dbp_95} mmHg")
            st.markdown(f"- **95th + 12 mmHg (Stage 2):** {sbp_stage2}/{dbp_stage2} mmHg")

    elif age_months < 12:
        height = st.number_input("Height (cm)", min_value=30.0, max_value=100.0, value=70.0)
        if st.button("Get Centiles"):
            sbp_50 = 85
            dbp_50 = 50
            sbp_90 = 95
            dbp_90 = 60
            sbp_95 = 98
            dbp_95 = 65
            sbp_stage2 = sbp_95 + 12
            dbp_stage2 = dbp_95 + 12

            st.subheader("Reference BP Values:")
            st.markdown(f"- **50th percentile:** {sbp_50}/{dbp_50} mmHg")
            st.markdown(f"- **90th percentile:** {sbp_90}/{dbp_90} mmHg")
            st.markdown(f"- **95th percentile:** {sbp_95}/{dbp_95} mmHg")
            st.markdown(f"- **95th + 12 mmHg (Stage 2):** {sbp_stage2}/{dbp_stage2} mmHg")

else:
    age_years = st.number_input("Age (years)", min_value=1, max_value=17, value=5)
    height = st.number_input("Height (cm)", min_value=60.0, max_value=180.0, value=100.0)
    if st.button("Get Centiles"):
        # Static logic for demonstration; should be replaced with AAP 2017 interpolation
        sbp_50 = 95 + age_years
        dbp_50 = 60 + int(age_years / 2)
        sbp_90 = sbp_50 + 5
        dbp_90 = dbp_50 + 5
        sbp_95 = sbp_50 + 8
        dbp_95 = dbp_50 + 7
        sbp_stage2 = sbp_95 + 12
        dbp_stage2 = dbp_95 + 12

        st.subheader("Reference BP Values:")
        st.markdown(f"- **50th percentile:** {sbp_50}/{dbp_50} mmHg")
        st.markdown(f"- **90th percentile:** {sbp_90}/{dbp_90} mmHg")
        st.markdown(f"- **95th percentile:** {sbp_95}/{dbp_95} mmHg")
        st.markdown(f"- **95th + 12 mmHg (Stage 2):** {sbp_stage2}/{dbp_stage2} mmHg")
