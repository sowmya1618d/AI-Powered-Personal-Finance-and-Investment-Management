"""
Main Streamlit Application
AI-Based Personal Finance & Investment Manager (India)
"""
import streamlit as st
import sys
sys.path.append('.')

# Page configuration
st.set_page_config(
    page_title="AI Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 3rem;
    }
    .option-card {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: transform 0.3s;
    }
    .option-card:hover {
        transform: translateY(-5px);
    }
    .option-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .option-desc {
        font-size: 1.1rem;
    }
    .feature-list {
        text-align: left;
        margin: 1rem 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">💰 AI Personal Finance Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">🇮🇳 India-Specific Financial Planning & Investment Platform</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.info("📊 **Welcome!** Choose an option below to manage your finances intelligently.")
    
    # Create 4 main option columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1️⃣ Income & Expenses")
        st.markdown("""
        - Track monthly salary and income
        - Category-wise expense management
        - Historical data entry
        - Expense anomaly detection
        """)
        if st.button("📝 Manage Income & Expenses", key="btn1", use_container_width=True):
            st.switch_page("pages/1_income_expenses.py")
        
        st.markdown("---")
        
        st.markdown("### 3️⃣ Financial Products")
        st.markdown("""
        - 📈 Stock Market (NSE)
        - 💼 SIP & Mutual Funds
        - 💳 Loans & Credit Cards
        - 🛡️ Insurance Policies
        - 💰 FD & Investments
        """)
        if st.button("🏦 Explore Financial Products", key="btn3", use_container_width=True):
            st.switch_page("pages/3_financial_products.py")
    
    with col2:
        st.markdown("### 2️⃣ AI Investment Suggestions")
        st.markdown("""
        - Risk-based portfolio allocation
        - ML-powered recommendations
        - Real-time market insights
        - AI agent advisory
        """)
        if st.button("🤖 Get AI Investment Advice", key="btn2", use_container_width=True):
            st.switch_page("pages/2_ai_investment.py")
        
        st.markdown("---")
        
        st.markdown("### 4️⃣ Summary & Reports")
        st.markdown("""
        - Net worth calculation
        - Growth visualization
        - Monthly PDF reports
        - LSTM forecasting
        """)
        if st.button("📊 View Summary & Reports", key="btn4", use_container_width=True):
            st.switch_page("pages/4_summary_report.py")
    
    # Features section
    st.markdown("---")
    st.markdown("## 🚀 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤖 AI-Powered**
        - LSTM Net Worth Forecasting
        - XGBoost Return Prediction
        - Autoencoder Anomaly Detection
        - RL Portfolio Optimization
        """)
    
    with col2:
        st.markdown("""
        **🇮🇳 India-Specific**
        - NSE Stock Market
        - Indian Rupee (₹)
        - Indian Financial Products
        - Local Market Data
        """)
    
    with col3:
        st.markdown("""
        **📊 Comprehensive**
        - Real-time Data Fetching
        - Interactive Dashboards
        - PDF Report Generation
        - Multi-page Navigation
        """)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 User Info")
        st.info("**User ID:** 1\n\n**Default User Mode**")
        
        st.markdown("---")
        
        st.markdown("### 🔧 Settings")
        st.markdown("- Currency: **₹ INR**")
        st.markdown("- Market: **NSE India**")
        st.markdown("- Timezone: **IST**")
        
        st.markdown("---")
        
        st.markdown("### 📖 Quick Links")
        st.markdown("[📚 Documentation](https://github.com)")
        st.markdown("[🐛 Report Issue](https://github.com)")
        st.markdown("[💡 Suggest Feature](https://github.com)")
        
        st.markdown("---")
        
        st.markdown("### ℹ️ About")
        st.markdown("""
        **AI Personal Finance Manager**
        
        Version: 1.0.0
        
        Built with:
        - FastAPI
        - Streamlit
        - TensorFlow
        - XGBoost
        - LangChain
        """)
        
        st.markdown("---")
        st.success("✅ Backend API: Connected")


if __name__ == "__main__":
    main()
