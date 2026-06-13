"""
Lump Sum Page
Principal, interest rate, time and final value calculation
"""
import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="Lump Sum / FD", page_icon="💰", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("💰 Lump Sum / Fixed Deposits")

st.markdown("### ➕ Add Investment")
with st.form("lump_form"):
    investment_name = st.text_input("Investment Name", value="Fixed Deposit")
    principal = st.number_input("Principal (₹)", min_value=1000.0, value=100000.0)
    interest_rate = st.number_input("Interest Rate (% p.a.)", min_value=0.0, value=6.5)
    tenure_months = st.number_input("Tenure (months)", min_value=1, value=12)
    start_date = st.date_input("Start Date", value=date.today())
    submit = st.form_submit_button("💾 Save Investment")

    if submit:
        data = {
            "user_id": USER_ID,
            "investment_name": investment_name,
            "principal": principal,
            "interest_rate": interest_rate,
            "tenure_months": int(tenure_months),
            "start_date": start_date.isoformat()
        }
        try:
            resp = requests.post(f"{API_URL}/lump-sum", json=data)
            if resp.status_code == 201:
                st.success("✅ Investment saved!")
                st.info(f"Estimated Maturity Value: ₹{resp.json()['maturity_value']:.2f}")
            else:
                st.error(f"❌ Error: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")

st.markdown("### 📁 Investments")
try:
    resp = requests.get(f"{API_URL}/lump-sum/{USER_ID}")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No investments found.")
except Exception as e:
    st.error(f"Error: {e}")

with st.sidebar:
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
