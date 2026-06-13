"""
Loans Page
Home, Personal, Mortgage loans with EMI auto-calculation and monthly outstanding tracking
"""
import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="Loans", page_icon="🏠", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("🏠 Loans")

st.markdown("### ➕ Add Loan")
with st.form("loan_form"):
    loan_type = st.selectbox("Loan Type", settings.LOAN_TYPES)
    principal_amount = st.number_input("Principal (₹)", min_value=10000.0, value=500000.0)
    interest_rate = st.number_input("Interest Rate (% p.a.)", min_value=0.0, value=8.5)
    tenure_months = st.number_input("Tenure (months)", min_value=6, value=240)
    start_date = st.date_input("Start Date", value=date.today())
    submit = st.form_submit_button("💾 Save Loan")

    if submit:
        data = {
            "user_id": USER_ID,
            "loan_type": loan_type,
            "principal_amount": principal_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure_months,
            "start_date": start_date.isoformat()
        }
        try:
            resp = requests.post(f"{API_URL}/loan", json=data)
            if resp.status_code == 201:
                st.success("✅ Loan saved! EMI auto-calculated.")
                st.info(f"EMI: ₹{resp.json()['emi']:.2f}")
            else:
                st.error(f"❌ Error: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")

st.markdown("### 📁 Loans")
try:
    resp = requests.get(f"{API_URL}/loan/{USER_ID}")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No loans found.")
except Exception as e:
    st.error(f"Error: {e}")

with st.sidebar:
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
