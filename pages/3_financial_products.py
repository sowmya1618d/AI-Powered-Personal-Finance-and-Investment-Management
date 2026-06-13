"""
Page 3: Financial Products Hub
Central page with redirects to all financial product pages
"""
import streamlit as st

st.set_page_config(page_title="Financial Products", page_icon="🏦", layout="wide")

st.title("🏦 Financial Products Hub")
st.markdown("Manage all your financial products in one place")

# Create grid of product categories
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Investments")
    
    if st.button("📊 Stock Market (NSE)", use_container_width=True):
        st.switch_page("pages/stock_market.py")
    
    if st.button("💼 SIP & Mutual Funds", use_container_width=True):
        st.switch_page("pages/sip_mutual_fund.py")
    
    if st.button("💰 Lump Sum / Fixed Deposits", use_container_width=True):
        st.switch_page("pages/lump_sum.py")

with col2:
    st.markdown("### 💳 Liabilities")
    
    if st.button("🏠 Loans", use_container_width=True):
        st.switch_page("pages/loans.py")
    
    if st.button("💳 Credit Cards", use_container_width=True):
        st.switch_page("pages/credit_card.py")
    
    if st.button("📤 SWP (Systematic Withdrawal)", use_container_width=True):
        st.switch_page("pages/swp.py")

with col3:
    st.markdown("### 🛡️ Protection")
    
    if st.button("🛡️ Insurance Policies", use_container_width=True):
        st.switch_page("pages/insurance.py")
    
    st.markdown("### 📊 Analysis")
    
    if st.button("📈 Portfolio Analysis", use_container_width=True):
        st.switch_page("pages/4_summary_report.py")

# Quick overview section
st.markdown("---")
st.markdown("## 📊 Product Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Assets", "₹0.00", "0%", help="Sum of all investments")

with col2:
    st.metric("Total Liabilities", "₹0.00", "0%", help="Sum of all loans & debts")

with col3:
    st.metric("Net Worth", "₹0.00", "0%", help="Assets - Liabilities")

with col4:
    st.metric("Monthly EMI", "₹0.00", help="Total monthly loan obligations")

# Information boxes
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **💡 Investment Tips:**
    - Diversify across asset classes
    - Review portfolio quarterly
    - Align investments with goals
    - Consider tax implications
    """)

with col2:
    st.warning("""
    **⚠️ Liability Management:**
    - Pay high-interest debts first
    - Maintain good credit score
    - Consider prepayment options
    - Track all due dates
    """)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    st.markdown("**Investment:**")
    st.markdown("• Add new stock")
    st.markdown("• Start new SIP")
    st.markdown("• Create FD")
    
    st.markdown("**Liability:**")
    st.markdown("• Add new loan")
    st.markdown("• Update credit card")
    
    st.markdown("**Protection:**")
    st.markdown("• Add insurance policy")
    
    st.markdown("---")
    st.markdown("### 📱 Coming Soon")
    st.markdown("• Gold/Silver investments")
    st.markdown("• Real estate tracking")
    st.markdown("• Cryptocurrency portfolio")
    st.markdown("• Alternative investments")
    
    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")

# Note about implementation
st.markdown("---")
st.info("""
**📝 Note:** This is the financial products hub. Each button represents a separate page that would handle:
- **Stock Market:** Real-time NSE stock tracking with yfinance
- **SIP/Mutual Funds:** Monthly SIP tracking and lump sum investments
- **Loans:** EMI calculations, amortization schedules, prepayment options
- **Insurance:** Policy management for all insurance types
- **Credit Cards:** Outstanding tracking and payment reminders
- **SWP:** Systematic withdrawal planning with optional loan linking
- **Lump Sum/FD:** Fixed deposit maturity calculations

Each page follows the same pattern as Income & Expenses page with forms, tables, and visualizations.
""")
