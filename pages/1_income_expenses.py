"""
Page 1: Income & Expenses Management
Track monthly income and categorized expenses
"""
import streamlit as st
import pandas as pd
import requests
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('..')

from config.settings import settings

st.set_page_config(page_title="Income & Expenses", page_icon="💸", layout="wide")

# API base URL
API_URL = f"http://{settings.API_HOST}:{settings.API_PORT}/api"

st.title("💸 Income & Expenses Management")
st.markdown("Track your monthly income and expenses with category-wise breakdown")

# User ID (default)
USER_ID = 1

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Add Data", "📊 View History", "🔍 Anomaly Detection"])

# ===== TAB 1: ADD DATA =====
with tab1:
    col1, col2 = st.columns(2)
    
    # === INCOME SECTION ===
    with col1:
        st.markdown("### 💰 Add Income")
        
        with st.form("income_form"):
            income_month = st.date_input(
                "Month",
                value=date.today().replace(day=1),
                help="Select the first day of the month"
            )
            
            salary = st.number_input(
                "Monthly Salary (₹)",
                min_value=0.0,
                value=0.0,
                step=1000.0,
                format="%.2f"
            )
            
            other_income = st.number_input(
                "Other Income (₹)",
                min_value=0.0,
                value=0.0,
                step=500.0,
                format="%.2f"
            )
            
            other_income_source = st.text_input(
                "Other Income Source",
                placeholder="e.g., Freelance, Rental, Dividends"
            )
            
            total_income = salary + other_income
            st.info(f"**Total Income:** ₹{total_income:,.2f}")
            
            submit_income = st.form_submit_button("💾 Save Income", use_container_width=True)
            
            if submit_income:
                if salary <= 0 and other_income <= 0:
                    st.error("Please enter at least one income source!")
                else:
                    # API call to save income
                    income_data = {
                        "user_id": USER_ID,
                        "month": income_month.isoformat(),
                        "salary": salary,
                        "other_income": other_income,
                        "other_income_source": other_income_source if other_income_source else None
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/income", json=income_data)
                        if response.status_code == 201:
                            st.success("✅ Income saved successfully!")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error connecting to API: {e}")
    
    # === EXPENSE SECTION ===
    with col2:
        st.markdown("### 💳 Add Expense")
        
        with st.form("expense_form"):
            expense_month = st.date_input(
                "Month",
                value=date.today().replace(day=1),
                help="Select the first day of the month",
                key="expense_month"
            )
            
            expense_category = st.selectbox(
                "Category",
                settings.EXPENSE_CATEGORIES
            )
            
            expense_amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f"
            )
            
            expense_description = st.text_area(
                "Description (Optional)",
                placeholder="Add notes about this expense..."
            )
            
            submit_expense = st.form_submit_button("💾 Save Expense", use_container_width=True)
            
            if submit_expense:
                if expense_amount <= 0:
                    st.error("Please enter a valid expense amount!")
                else:
                    # API call to save expense
                    expense_data = {
                        "user_id": USER_ID,
                        "month": expense_month.isoformat(),
                        "category": expense_category,
                        "amount": expense_amount,
                        "description": expense_description if expense_description else None
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/expense", json=expense_data)
                        if response.status_code == 201:
                            st.success("✅ Expense saved successfully!")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error connecting to API: {e}")

# ===== TAB 2: VIEW HISTORY =====
with tab2:
    st.markdown("### 📊 Income & Expense History")
    
    # Fetch data
    try:
        income_response = requests.get(f"{API_URL}/income/{USER_ID}")
        expense_response = requests.get(f"{API_URL}/expense/{USER_ID}")
        
        if income_response.status_code == 200 and expense_response.status_code == 200:
            incomes = income_response.json()
            expenses = expense_response.json()
            
            if incomes or expenses:
                # Convert to DataFrames
                income_df = pd.DataFrame(incomes)
                expense_df = pd.DataFrame(expenses)
                
                if not income_df.empty:
                    income_df['month'] = pd.to_datetime(income_df['month'])
                if not expense_df.empty:
                    expense_df['month'] = pd.to_datetime(expense_df['month'])
                
                # Monthly summary
                st.markdown("#### 📅 Monthly Summary")
                
                if not income_df.empty and not expense_df.empty:
                    # Group by month
                    monthly_income = income_df.groupby('month')['total_income'].sum()
                    monthly_expense = expense_df.groupby('month')['amount'].sum()
                    
                    # Create comparison DataFrame
                    summary_df = pd.DataFrame({
                        'Month': monthly_income.index.strftime('%b %Y'),
                        'Income': monthly_income.values,
                        'Expenses': monthly_expense.reindex(monthly_income.index, fill_value=0).values
                    })
                    summary_df['Savings'] = summary_df['Income'] - summary_df['Expenses']
                    summary_df['Savings Rate (%)'] = (summary_df['Savings'] / summary_df['Income'] * 100).round(2)
                    
                    st.dataframe(summary_df, use_container_width=True)
                    
                    # Visualization
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Line chart: Income vs Expenses
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=summary_df['Month'],
                            y=summary_df['Income'],
                            name='Income',
                            line=dict(color='green', width=3)
                        ))
                        fig.add_trace(go.Scatter(
                            x=summary_df['Month'],
                            y=summary_df['Expenses'],
                            name='Expenses',
                            line=dict(color='red', width=3)
                        ))
                        fig.update_layout(
                            title="Income vs Expenses Trend",
                            xaxis_title="Month",
                            yaxis_title="Amount (₹)",
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Bar chart: Savings
                        fig = px.bar(
                            summary_df,
                            x='Month',
                            y='Savings',
                            title='Monthly Savings',
                            color='Savings',
                            color_continuous_scale='RdYlGn'
                        )
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Category-wise expense breakdown
                if not expense_df.empty:
                    st.markdown("#### 📊 Expense Breakdown by Category")
                    
                    category_expenses = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Pie chart
                        fig = px.pie(
                            values=category_expenses.values,
                            names=category_expenses.index,
                            title='Expense Distribution',
                            hole=0.4
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Bar chart
                        fig = px.bar(
                            x=category_expenses.values,
                            y=category_expenses.index,
                            orientation='h',
                            title='Expense by Category',
                            labels={'x': 'Amount (₹)', 'y': 'Category'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📝 No data available. Start by adding your income and expenses!")
        else:
            st.error("❌ Error fetching data from API")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ===== TAB 3: ANOMALY DETECTION =====
with tab3:
    st.markdown("### 🔍 Expense Anomaly Detection")
    st.info("🤖 Using AI to detect unusual spending patterns...")
    
    try:
        expense_response = requests.get(f"{API_URL}/expense/{USER_ID}")
        
        if expense_response.status_code == 200:
            expenses = expense_response.json()
            
            if expenses:
                expense_df = pd.DataFrame(expenses)
                expense_df['month'] = pd.to_datetime(expense_df['month'])
                
                # Simple rule-based anomaly detection
                monthly_totals = expense_df.groupby('month')['amount'].sum()
                
                if len(monthly_totals) >= 3:
                    mean_expense = monthly_totals.mean()
                    std_expense = monthly_totals.std()
                    threshold = mean_expense + 2 * std_expense
                    
                    anomalies = monthly_totals[monthly_totals > threshold]
                    
                    if len(anomalies) > 0:
                        st.warning(f"⚠️ {len(anomalies)} anomalous month(s) detected!")
                        
                        for month, amount in anomalies.items():
                            with st.expander(f"📅 {month.strftime('%B %Y')} - ₹{amount:,.2f}"):
                                deviation = ((amount - mean_expense) / std_expense)
                                st.metric(
                                    "Deviation from Average",
                                    f"{deviation:.1f}σ",
                                    f"₹{amount - mean_expense:,.2f}"
                                )
                                
                                # Show category breakdown for that month
                                month_expenses = expense_df[expense_df['month'] == month]
                                category_breakdown = month_expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
                                
                                st.markdown("**Top Expense Categories:**")
                                for cat, amt in category_breakdown.head(5).items():
                                    st.markdown(f"- {cat}: ₹{amt:,.2f}")
                    else:
                        st.success("✅ No anomalies detected. Your spending is consistent!")
                else:
                    st.info("📊 Need at least 3 months of data for anomaly detection")
            else:
                st.info("📝 No expense data available")
        else:
            st.error("❌ Error fetching expense data")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    try:
        income_response = requests.get(f"{API_URL}/income/{USER_ID}")
        expense_response = requests.get(f"{API_URL}/expense/{USER_ID}")
        
        if income_response.status_code == 200 and expense_response.status_code == 200:
            incomes = income_response.json()
            expenses = expense_response.json()
            
            total_income = sum(inc['total_income'] for inc in incomes)
            total_expenses = sum(exp['amount'] for exp in expenses)
            total_savings = total_income - total_expenses
            
            st.metric("Total Income", f"₹{total_income:,.2f}")
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
            st.metric("Total Savings", f"₹{total_savings:,.2f}")
    except:
        pass
    
    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")
