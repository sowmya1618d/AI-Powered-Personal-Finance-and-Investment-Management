"""
SWP → Loan Connector Page
Use SWP amount to reduce EMI or principal on selected loan
"""
import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="SWP → Loan Connector", page_icon="🔗", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("🔗 SWP → Loan Connector")

# Fetch loans and SWPs
loans = []
swps = []

try:
    loan_resp = requests.get(f"{API_URL}/loan/{USER_ID}")
    swp_resp = requests.get(f"{API_URL}/swp/{USER_ID}")
    if loan_resp.status_code == 200:
        loans = loan_resp.json()
    if swp_resp.status_code == 200:
        swps = swp_resp.json()
except Exception as e:
    st.error(f"Error fetching data: {e}")

loan_options = {f"#{l['id']} - {l['loan_type']} (Outstanding ₹{l['outstanding_amount']:.2f})": l for l in loans}
swp_options = {f"#{s['id']} - {s['source_investment_type']} (₹{s['monthly_withdrawal']:.2f})": s for s in swps}

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏠 Select Loan")
    selected_loan_key = st.selectbox("Loan", list(loan_options.keys())) if loan_options else None

with col2:
    st.markdown("### 📤 Select SWP")
    selected_swp_key = st.selectbox("SWP", list(swp_options.keys())) if swp_options else None

st.markdown("---")

if selected_loan_key and selected_swp_key:
    loan = loan_options[selected_loan_key]
    swp = swp_options[selected_swp_key]

    st.info(
        f"Applying SWP ₹{swp['monthly_withdrawal']:.2f} to loan outstanding ₹{loan['outstanding_amount']:.2f}"
    )

    apply_mode = st.radio("Apply SWP to:", ["Reduce EMI", "Reduce Principal"], index=1)

    if st.button("✅ Apply This Month", use_container_width=True):
        try:
            new_outstanding = loan['outstanding_amount'] - swp['monthly_withdrawal']
            if new_outstanding < 0:
                new_outstanding = 0.0
            upd = requests.put(
                f"{API_URL}/loan/{loan['id']}/outstanding",
                params={"new_outstanding": new_outstanding}
            )
            if upd.status_code == 200:
                st.success("✅ Loan outstanding updated!")
            else:
                st.error(f"❌ Error: {upd.text}")
        except Exception as e:
            st.error(f"API error: {e}")

with st.sidebar:
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
}