"""
Stock Market (NSE) Page
Select Indian company, fetch real-time price, compute value, store snapshot
"""
import streamlit as st
import requests
import pandas as pd
from datetime import date
import sys
sys.path.append('..')

from config.settings import settings
from utils.market_data import market_data_fetcher

st.set_page_config(page_title="Stock Market (NSE)", page_icon="📊", layout="wide")

API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
USER_ID = 1

st.title("📊 Stock Market (NSE)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔎 Select Stock")
    symbol = st.text_input("NSE Symbol (e.g., RELIANCE, TCS, HDFCBANK)", value="RELIANCE")
    company_name = st.text_input("Company Name", value="Reliance Industries Ltd")
    quantity = st.number_input("Quantity", min_value=1, value=10)

with col2:
    st.markdown("### 💵 Price & Value")
    if st.button("⚡ Fetch Real-time Price", use_container_width=True):
        price = market_data_fetcher.get_stock_price(symbol)
        if price:
            st.success(f"Current Price: ₹{price:,.2f}")
            current_value = price * quantity
            st.info(f"Current Value: ₹{current_value:,.2f}")
        else:
            st.error("Unable to fetch price. Please verify symbol.")

st.markdown("---")

with st.form("stock_form"):
    st.markdown("### 💾 Save to Portfolio")
    purchase_price = st.number_input("Purchase Price (₹)", min_value=0.0, value=2500.0, format="%.2f")
    purchase_date = st.date_input("Purchase Date", value=date.today())
    submit = st.form_submit_button("💾 Save Stock")

    if submit:
        try:
            data = {
                "user_id": USER_ID,
                "company_name": company_name,
                "symbol": symbol,
                "quantity": quantity,
                "purchase_price": purchase_price,
                "purchase_date": purchase_date.isoformat()
            }
            resp = requests.post(f"{API_URL}/stock", json=data)
            if resp.status_code == 201:
                st.success("✅ Stock saved!")
                # Update current price
                stock_id = resp.json()['id']
                price = market_data_fetcher.get_stock_price(symbol)
                if price:
                    upd = requests.put(f"{API_URL}/stock/{stock_id}/price", params={"current_price": price})
                    if upd.status_code == 200:
                        st.info("🔄 Current value updated.")
            else:
                st.error(f"❌ Error: {resp.text}")
        except Exception as e:
            st.error(f"❌ API error: {e}")

st.markdown("---")

st.markdown("### 📁 Portfolio")
try:
    resp = requests.get(f"{API_URL}/stock/{USER_ID}")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No stocks yet. Add your first holding above.")
    else:
        st.error("Failed to fetch portfolio.")
except Exception as e:
    st.error(f"Error: {e}")

with st.sidebar:
    if st.button("🏠 Back to Hub"):
        st.switch_page("pages/3_financial_products.py")
