import streamlit as st
import pandas as pd
import pickle

# Load trained Random Forest model
model = pickle.load(open("best_model_compressed.pkl", "rb"))

st.set_page_config(page_title="Loan Approval Predictor", page_icon="🏦")
st.title("🏦 Smart Loan Approval Prediction App")
st.write("Enter applicant details below to check loan eligibility.")

# ---------------- INPUT SECTION ----------------
credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650)
person_income = st.number_input("Annual Income (₹)", min_value=0, value=40000, step=1000)
loan_amnt = st.number_input("Requested Loan Amount (₹)", min_value=0, value=10000, step=1000)
loan_percent_income = st.number_input("Loan Amount as % of Income", min_value=0.0, value=0.25, step=0.01)
loan_int_rate = st.number_input("Loan Interest Rate (%)", min_value=0.0, value=12.0, step=0.1)
person_emp_exp = st.number_input("Years of Employment Experience", min_value=0, value=3)
previous_loan_defaults_on_file = st.selectbox("Any Previous Loan Default?", ["No", "Yes"])

# Convert categorical input to numeric
prev_default = 1 if previous_loan_defaults_on_file == "Yes" else 0

# ---------------- PREDICTION SECTION ----------------
if st.button("Predict Loan Approval"):
    input_data = pd.DataFrame({
        "credit_score": [credit_score],
        "person_income": [person_income],
        "loan_amnt": [loan_amnt],
        "loan_percent_income": [loan_percent_income],
        "loan_int_rate": [loan_int_rate],
        "person_emp_exp": [person_emp_exp],
        "previous_loan_defaults_on_file": [prev_default]
    })

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("✅ Loan Approved! The applicant meets the financial criteria.")
    else:
        st.error("❌ Loan Not Approved.")
        st.subheader("🔍 Possible Reasons:")
        
        reasons = []
        if credit_score < 600:
            reasons.append("Low credit score (below 600)")
        if person_income < 25000:
            reasons.append("Low annual income")
        if loan_percent_income > 0.5:
            reasons.append("Loan amount is more than 50% of income")
        if prev_default == 1:
            reasons.append("Previous loan default on record")
        if loan_int_rate > 15:
            reasons.append("High interest rate increases risk")
        if person_emp_exp < 1:
            reasons.append("Insufficient employment experience")

        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.write("Applicant does not meet model criteria for approval.")
