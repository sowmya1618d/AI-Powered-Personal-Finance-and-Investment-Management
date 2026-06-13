"""
Insurance Page
Manage Term, Life, Health, Child, Retirement insurance policies
"""
import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="Insurance", page_icon="🛡️", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("🛡️ Insurance Policies")

st.markdown("### ➕ Add Policy")
with st.form("insurance_form"):
    insurance_type = st.selectbox("Type", settings.INSURANCE_TYPES)
    policy_name = st.text_input("Policy Name", value="Term Plan")
    policy_number = st.text_input("Policy Number", value="ABC123456")
    premium_amount = st.number_input("Premium (₹)", min_value=1000.0, value=15000.0)
    premium_frequency = st.selectbox("Frequency", ["Monthly", "Quarterly", "Annual"])
    coverage_amount = st.number_input("Coverage (₹)", min_value=100000.0, value=5000000.0)
    tenure_years = st.number_input("Tenure (years)", min_value=1, value=30)
    start_date = st.date_input("Start Date", value=date.today())
    submit = st.form_submit_button("💾 Save Policy")

    if submit:
        data = {
            "user_id": USER_ID,
            "insurance_type": insurance_type,
            "policy_name": policy_name,
            "policy_number": policy_number,
            "premium_amount": premium_amount,
            "premium_frequency": premium_frequency,
            "coverage_amount": coverage_amount,
            "tenure_years": tenure_years,
            "start_date": start_date.isoformat()
        }
        try:
            resp = requests.post(f"{API_URL}/insurance", json=data)
            if resp.status_code == 201:
                st.success("✅ Policy saved!")
            else:
                st.error(f"❌ Error: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")

st.markdown("### 📁 Policies")
try:
    resp = requests.get(f"{API_URL}/insurance/{USER_ID}")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No policies found.")
except Exception as e:
    st.error(f"Error: {e}")

with st.sidebar:
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
