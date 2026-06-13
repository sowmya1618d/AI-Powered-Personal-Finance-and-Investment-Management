"""
Credit Card Page
Track card limit, outstanding, due date and impact on liabilities
"""
import streamlit as st
import requests
import pandas as pd
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="Credit Cards", page_icon="💳", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("💳 Credit Cards")

st.markdown("### ➕ Add Card")
with st.form("card_form"):
    card_name = st.text_input("Card Name", value="Premium Credit Card")
    card_number_last4 = st.text_input("Last 4 digits", value="1234", max_chars=4)
    credit_limit = st.number_input("Credit Limit (₹)", min_value=10000.0, value=200000.0)
    outstanding_amount = st.number_input("Outstanding (₹)", min_value=0.0, value=0.0)
    due_date = st.number_input("Due Day of Month", min_value=1, max_value=31, value=15)
    submit = st.form_submit_button("💾 Save Card")

    if submit:
        data = {
            "user_id": USER_ID,
            "card_name": card_name,
            "card_number_last4": card_number_last4,
            "credit_limit": credit_limit,
            "outstanding_amount": outstanding_amount,
            "due_date": int(due_date)
        }
        try:
            resp = requests.post(f"{API_URL}/credit-card", json=data)
            if resp.status_code == 201:
                st.success("✅ Card saved!")
            else:
                st.error(f"❌ Error: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")

st.markdown("### 📁 Cards")
try:
    resp = requests.get(f"{API_URL}/credit-card/{USER_ID}")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No cards found.")
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("### 🔄 Update Outstanding")
card_id = st.number_input("Card ID", min_value=0, value=0)
new_outstanding = st.number_input("New Outstanding (₹)", min_value=0.0, value=0.0)
if st.button("🔄 Update", use_container_width=True):
    try:
        resp = requests.put(f"{API_URL}/credit-card/{int(card_id)}/outstanding", params={"new_outstanding": new_outstanding})
        if resp.status_code == 200:
            st.success("✅ Outstanding updated!")
        else:
            st.error(f"❌ Error: {resp.text}")
    except Exception as e:
        st.error(f"API error: {e}")

with st.sidebar:
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
