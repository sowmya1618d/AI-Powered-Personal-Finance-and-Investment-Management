"""
SWP Page
Set up systematic withdrawals from investments and optionally link to a loan
"""
import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="SWP", page_icon="📤", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("📤 Systematic Withdrawal Plan (SWP)")

st.markdown("### ➕ Create SWP")
with st.form("swp_form"):
    source_type = st.selectbox("Investment Type", ["SIP", "MutualFund", "Stocks", "LumpSum"])
    source_id = st.number_input("Investment ID", min_value=1, value=1, help="Enter the ID from the respective investment table")
    monthly_withdrawal = st.number_input("Monthly Withdrawal (₹)", min_value=100.0, value=2000.0)
    start_date = st.date_input("Start Date", value=date.today())
    link_to_loan = st.checkbox("Link to Loan (reduce EMI/principal)")
    linked_loan_id = st.number_input("Loan ID (optional)", min_value=0, value=0) if link_to_loan else None
    submit = st.form_submit_button("💾 Save SWP")

    if submit:
        data = {
            "user_id": USER_ID,
            "source_investment_type": source_type,
            "source_investment_id": int(source_id),
            "monthly_withdrawal": monthly_withdrawal,
            "start_date": start_date.isoformat(),
            "linked_loan_id": int(linked_loan_id) if linked_loan_id else None
        }
        try:
            resp = requests.post(f"{API_URL}/swp", json=data)
            if resp.status_code == 201:
                st.success("✅ SWP saved!")
            else:
                st.error(f"❌ Error: {resp.text}")
        except Exception as e:
            st.error(f"❌ API error: {e}")

st.markdown("### 📁 Active SWPs")
try:
    resp = requests.get(f"{API_URL}/swp/{USER_ID}")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No SWPs found.")
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

st.info("To connect SWP to a loan and apply withdrawals to EMI/principal, go to the 'SWP → Loan Connector' page.")

with st.sidebar:
    if st.button("🔗 SWP → Loan Connector"):
        st.switch_page("pages/swp_loan_connector.py")
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
