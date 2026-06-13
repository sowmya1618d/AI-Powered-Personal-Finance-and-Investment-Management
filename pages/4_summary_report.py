"""
Page 4: Summary & Monthly Report
Net worth tracking, visualizations, and PDF report generation
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import date, datetime
import sys
sys.path.append('..')

from config.settings import settings
from ml_models.lstm_forecasting import forecast_net_worth
from utils.pdf_generator import report_generator

st.set_page_config(page_title="Summary & Reports", page_icon="📊", layout="wide")

st.title("📊 Financial Summary & Reports")
st.markdown("Comprehensive overview of your financial health with AI-powered insights")

USER_ID = 1
API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Net Worth", "📊 Visualizations", "🤖 AI Forecast", "📄 PDF Report"])

# ===== TAB 1: NET WORTH =====
with tab1:
    st.markdown("### 💎 Net Worth Summary")
    
    # Calculate current net worth
    col1, col2, col3 = st.columns(3)
    
    # Mock data for demo (in production, fetch from API)
    total_assets = 500000.0
    total_liabilities = 150000.0
    net_worth = total_assets - total_liabilities
    
    with col1:
        st.metric(
            "Total Assets",
            f"₹{total_assets:,.0f}",
            "+12.5%",
            help="Sum of all investments and savings"
        )
    
    with col2:
        st.metric(
            "Total Liabilities",
            f"₹{total_liabilities:,.0f}",
            "-5.2%",
            help="Sum of all loans and debts"
        )
    
    with col3:
        st.metric(
            "Net Worth",
            f"₹{net_worth:,.0f}",
            "+18.3%",
            help="Assets - Liabilities"
        )
    
    st.markdown("---")
    
    # Asset breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Assets Breakdown")
        
        assets_data = {
            "Category": ["Stocks", "SIP", "Mutual Funds", "Fixed Deposits", "Savings"],
            "Amount": [150000, 120000, 100000, 80000, 50000]
        }
        assets_df = pd.DataFrame(assets_data)
        
        fig = px.pie(
            assets_df,
            values='Amount',
            names='Category',
            title='Asset Allocation',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            assets_df.style.format({'Amount': '₹{:,.0f}'}),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("#### 📉 Liabilities Breakdown")
        
        liabilities_data = {
            "Category": ["Home Loan", "Personal Loan", "Credit Card"],
            "Amount": [120000, 25000, 5000]
        }
        liabilities_df = pd.DataFrame(liabilities_data)
        
        fig = px.pie(
            liabilities_df,
            values='Amount',
            names='Category',
            title='Liability Distribution',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            liabilities_df.style.format({'Amount': '₹{:,.0f}'}),
            use_container_width=True,
            hide_index=True
        )

# ===== TAB 2: VISUALIZATIONS =====
with tab2:
    st.markdown("### 📊 Financial Visualizations")
    
    # Net worth history (mock data)
    months = pd.date_range(start='2023-06-01', end='2024-06-01', freq='MS')
    net_worth_history = [320000, 335000, 348000, 362000, 378000, 395000, 410000, 
                         425000, 442000, 458000, 475000, 492000, 510000]
    
    history_df = pd.DataFrame({
        'Month': months,
        'Net Worth': net_worth_history
    })
    
    # Line chart: Net worth growth
    st.markdown("#### 📈 Net Worth Growth Over Time")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history_df['Month'],
        y=history_df['Net Worth'],
        mode='lines+markers',
        name='Net Worth',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))
    
    fig.update_layout(
        title='Net Worth Progression',
        xaxis_title='Month',
        yaxis_title='Net Worth (₹)',
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly investment increase
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Monthly Investment Trend")
        
        investment_data = {
            'Month': ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
            'Investment': [15000, 18000, 16000, 20000, 22000, 25000]
        }
        inv_df = pd.DataFrame(investment_data)
        
        fig = px.bar(
            inv_df,
            x='Month',
            y='Investment',
            title='Monthly Investment Amount',
            color='Investment',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Savings Rate")
        
        savings_data = {
            'Month': ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
            'Savings Rate': [25, 28, 26, 32, 35, 38]
        }
        sav_df = pd.DataFrame(savings_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sav_df['Month'],
            y=sav_df['Savings Rate'],
            mode='lines+markers',
            line=dict(color='green', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title='Savings Rate (%)',
            yaxis_title='Percentage (%)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparison charts
    st.markdown("#### 📊 Asset vs Liability Trend")
    
    comparison_data = {
        'Month': ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
        'Assets': [450000, 465000, 478000, 490000, 502000, 515000],
        'Liabilities': [155000, 152000, 150000, 148000, 145000, 142000]
    }
    comp_df = pd.DataFrame(comparison_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Assets', x=comp_df['Month'], y=comp_df['Assets'], marker_color='lightgreen'))
    fig.add_trace(go.Bar(name='Liabilities', x=comp_df['Month'], y=comp_df['Liabilities'], marker_color='lightcoral'))
    
    fig.update_layout(
        title='Assets vs Liabilities',
        barmode='group',
        yaxis_title='Amount (₹)',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# ===== TAB 3: AI FORECAST =====
with tab3:
    st.markdown("### 🤖 AI-Powered Net Worth Forecast")
    st.info("Using LSTM neural networks to predict your future net worth")
    
    if st.button("🔮 Generate Forecast", use_container_width=True):
        with st.spinner("🤖 Training LSTM model and generating predictions..."):
            # Create sample historical data
            history_df = pd.DataFrame({
                'month': pd.date_range(start='2023-01-01', periods=13, freq='MS'),
                'net_worth': [320000, 335000, 348000, 362000, 378000, 395000, 410000, 
                             425000, 442000, 458000, 475000, 492000, 510000]
            })
            
            # Get forecast
            forecast_result = forecast_net_worth(history_df, months=6)
            
            st.success("✅ Forecast generated successfully!")
            
            # Display predictions
            st.markdown("#### 📈 Next 6 Months Prediction")
            
            future_months = pd.date_range(start='2024-07-01', periods=6, freq='MS')
            predictions = forecast_result['predictions']
            
            forecast_df = pd.DataFrame({
                'Month': future_months.strftime('%b %Y'),
                'Predicted Net Worth': predictions,
                'Growth': [f"+{((p - 510000) / 510000 * 100):.1f}%" for p in predictions]
            })
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Combine historical and forecast
                combined_months = list(history_df['month']) + list(future_months)
                combined_values = list(history_df['net_worth']) + predictions
                
                fig = go.Figure()
                
                # Historical
                fig.add_trace(go.Scatter(
                    x=history_df['month'],
                    y=history_df['net_worth'],
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='blue', width=3)
                ))
                
                # Forecast
                fig.add_trace(go.Scatter(
                    x=future_months,
                    y=predictions,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='orange', width=3, dash='dash')
                ))
                
                fig.update_layout(
                    title='Net Worth Forecast (LSTM)',
                    xaxis_title='Month',
                    yaxis_title='Net Worth (₹)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(
                    forecast_df.style.format({'Predicted Net Worth': '₹{:,.0f}'}),
                    use_container_width=True,
                    hide_index=True
                )
                
                avg_growth = (predictions[-1] - predictions[0]) / predictions[0] * 100
                st.metric(
                    "Projected Growth (6 months)",
                    f"₹{predictions[-1] - 510000:,.0f}",
                    f"+{avg_growth:.1f}%"
                )
            
            st.markdown(f"**Model:** {forecast_result['method']}")
            st.info("📝 **Note:** Predictions are based on historical trends and may vary based on market conditions and your financial decisions.")

# ===== TAB 4: PDF REPORT =====
with tab4:
    st.markdown("### 📄 Generate Monthly PDF Report")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        report_month = st.date_input(
            "Select Report Month",
            value=date.today().replace(day=1)
        )
        
        user_name = st.text_input("Your Name", value="User")
        
        if st.button("📥 Generate PDF Report", use_container_width=True):
            with st.spinner("📄 Generating comprehensive PDF report..."):
                # Prepare data for report
                income_data = {
                    'salary': 50000,
                    'other_income': 5000,
                    'total': 55000
                }
                
                expense_data = {
                    'categories': {
                        'Food & Dining': 8000,
                        'Transportation': 5000,
                        'Bills & Utilities': 4000,
                        'Shopping': 3000,
                        'Others': 2000
                    },
                    'total': 22000
                }
                
                assets_data = {
                    'stocks': 150000,
                    'sip': 120000,
                    'mutual_funds': 100000,
                    'fd': 80000,
                    'savings': 50000,
                    'total': 500000
                }
                
                liabilities_data = {
                    'home_loan': 120000,
                    'personal_loan': 25000,
                    'credit_card': 5000,
                    'total': 150000
                }
                
                net_worth_data = {
                    'net_worth': 350000,
                    'previous_month': 340000
                }
                
                predictions = {
                    'next_month': 360000,
                    'expected_return': 12.5,
                    'risk_score': 'Medium'
                }
                
                # Generate PDF
                pdf_path = report_generator.generate_report(
                    user_name,
                    report_month,
                    income_data,
                    expense_data,
                    assets_data,
                    liabilities_data,
                    net_worth_data,
                    predictions
                )
                
                st.success(f"✅ PDF report generated successfully!")
                st.info(f"📁 Report saved to: `{pdf_path}`")
                
                # Download button
                try:
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_file,
                            file_name=f"financial_report_{report_month.strftime('%Y-%m')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except:
                    st.warning("Download will be available once report is generated")
    
    with col2:
        st.markdown("#### 📋 Report Contents")
        st.markdown("""
        Your monthly financial report includes:
        
        **📊 Income Summary**
        - Salary breakdown
        - Other income sources
        - Total monthly income
        
        **💸 Expense Analysis**
        - Category-wise expenses
        - Spending patterns
        - Savings calculation
        
        **📈 Assets Overview**
        - Stock portfolio value
        - SIP and mutual fund holdings
        - Fixed deposits
        - Savings accounts
        
        **📉 Liabilities Summary**
        - Outstanding loans
        - Credit card dues
        - EMI obligations
        
        **💎 Net Worth Calculation**
        - Current net worth
        - Month-over-month change
        - Growth percentage
        
        **🤖 AI Predictions**
        - Next month net worth forecast
        - Expected returns
        - Risk assessment
        
        All values in Indian Rupees (₹) with detailed tables and charts.
        """)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    st.metric("Current Net Worth", "₹3,50,000")
    st.metric("Monthly Savings", "₹33,000", "+15%")
    st.metric("Investment Returns", "12.5%", "+2.3%")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Financial Goals")
    progress_1 = 65
    st.markdown("**Emergency Fund**")
    st.progress(progress_1 / 100)
    st.caption(f"{progress_1}% Complete")
    
    progress_2 = 40
    st.markdown("**Home Purchase**")
    st.progress(progress_2 / 100)
    st.caption(f"{progress_2}% Complete")
    
    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")
