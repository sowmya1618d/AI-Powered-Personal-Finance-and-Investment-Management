#!/usr/bin/env python3
"""
Comprehensive application initialization script
- Creates all database tables automatically
- Adds sample data for demonstration
- Verifies environment configuration
- Ready for immediate use
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from config.settings import settings
from database.connection import engine, init_db, SessionLocal, Base
from database.models import (
    User, Income, Expense, Stock, SIP, MutualFund,
    Loan, Insurance, CreditCard, LumpSum, NetWorthHistory, SWP, RiskLevel
)
from sqlalchemy import text
import hashlib

# Load environment variables
load_dotenv()


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def verify_database_connection():
    """Verify MySQL database connection"""
    print_header("🔍 Verifying Database Connection")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            print_success(f"Connected to MySQL at {settings.DB_HOST}:{settings.DB_PORT}")
            print_success(f"Database: {settings.DB_NAME}")
            print_success(f"User: {settings.DB_USER}")
            return True
    except Exception as e:
        print_error(f"Database connection failed: {str(e)}")
        print_error("Make sure:")
        print_error("  1. MySQL is running: brew services start mysql")
        print_error("  2. Database exists: CREATE DATABASE finance_db;")
        print_error("  3. .env file has correct credentials")
        return False


def create_tables():
    """Create all database tables"""
    print_header("📊 Creating Database Tables")
    
    try:
        init_db()
        print_success("All tables created successfully!")
        return True
    except Exception as e:
        print_error(f"Failed to create tables: {str(e)}")
        return False


def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()


def add_sample_data():
    """Add sample data for demonstration"""
    print_header("📝 Adding Sample Data")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_user = db.query(User).filter(User.email == "demo@finance.com").first()
        if existing_user:
            print_info("Sample data already exists. Skipping...")
            return True
        
        # Create a demo user
        print_info("Creating demo user...")
        demo_user = User(
            email="demo@finance.com",
            name="Demo User",
            password_hash=hash_password("demo123")
        )
        db.add(demo_user)
        db.flush()  # Get the user ID
        
        print_success("Demo user created!")
        
        # Add income data for the last 6 months
        print_info("Adding income data...")
        today = datetime.now().date()
        for i in range(6):
            month = today - timedelta(days=30*i)
            month = month.replace(day=1)
            
            income = Income(
                user_id=demo_user.id,
                month=month,
                salary=75000 + (i * 1000),  # Increasing salary
                other_income=5000,
                other_income_source="Freelance",
                total_income=80000 + (i * 1000)
            )
            db.add(income)
        
        print_success("Added income data for 6 months!")
        
        # Add expense data
        print_info("Adding expense data...")
        expense_categories = [
            ("Food & Dining", 8000),
            ("Transportation", 3000),
            ("Shopping", 5000),
            ("Entertainment", 2000),
            ("Bills & Utilities", 4000),
            ("Healthcare", 1500),
            ("Education", 2000),
            ("Travel", 6000),
            ("EMI", 15000),
            ("Others", 3000)
        ]
        
        for i in range(6):
            month = today - timedelta(days=30*i)
            month = month.replace(day=1)
            
            for category, amount in expense_categories:
                expense = Expense(
                    user_id=demo_user.id,
                    month=month,
                    category=category,
                    amount=amount,
                    description=f"{category} expense",
                    is_anomaly=False
                )
                db.add(expense)
        
        print_success("Added expense data for 6 months with 10 categories!")
        
        # Add stock data
        print_info("Adding stock portfolio...")
        stocks_data = [
            ("RELIANCE", "Reliance Industries", 2500, 2700, 10, 27000),
            ("TCS", "Tata Consultancy Services", 3500, 3650, 5, 18250),
            ("HDFCBANK", "HDFC Bank", 1800, 1950, 15, 29250),
            ("INFY", "Infosys", 1600, 1750, 8, 14000),
            ("WIPRO", "Wipro", 500, 550, 20, 11000),
        ]
        
        for symbol, company, purchase_price, current_price, quantity, current_value in stocks_data:
            stock = Stock(
                user_id=demo_user.id,
                symbol=symbol,
                company_name=company,
                purchase_price=purchase_price,
                purchase_date=today - timedelta(days=180),
                quantity=quantity,
                current_price=current_price,
                current_value=current_value
            )
            db.add(stock)
        
        print_success("Added 5 NSE stocks to portfolio!")
        
        # Add SIP data
        print_info("Adding SIP investments...")
        sips_data = [
            ("HDFC Hybrid Equity Fund", 5000, 0.12),
            ("Axis Bluechip Fund", 10000, 0.11),
            ("ICICI Prudential Growth Fund", 8000, 0.10),
        ]
        
        for fund_name, monthly_amount, expected_return in sips_data:
            sip = SIP(
                user_id=demo_user.id,
                fund_name=fund_name,
                monthly_amount=monthly_amount,
                start_date=today - timedelta(days=90),
                expected_return_rate=expected_return,
                current_value=monthly_amount * 3 * (1 + expected_return/12)
            )
            db.add(sip)
        
        print_success("Added 3 SIP investments!")
        
        # Add Mutual Fund data
        print_info("Adding mutual fund investments...")
        mfs_data = [
            ("Motilal Oswal Large Cap Fund", 100000, 0.14),
            ("DSP Equity Fund", 75000, 0.13),
            ("Parag Parikh Financial Advisory Fund", 50000, 0.15),
        ]
        
        for fund_name, investment_amount, expected_return in mfs_data:
            mf = MutualFund(
                user_id=demo_user.id,
                fund_name=fund_name,
                investment_amount=investment_amount,
                investment_date=today - timedelta(days=120),
                expected_return_rate=expected_return,
                current_value=investment_amount * (1 + (expected_return * 4/12))
            )
            db.add(mf)
        
        print_success("Added 3 mutual fund investments!")
        
        # Add Loan data
        print_info("Adding loan records...")
        loans_data = [
            ("Home Loan", 3500000, 6.5, 240, 15000),
            ("Personal Loan", 500000, 9.5, 60, 10000),
        ]
        
        for loan_type, principal, rate, tenure, emi in loans_data:
            loan = Loan(
                user_id=demo_user.id,
                loan_type=loan_type,
                principal_amount=principal,
                interest_rate=rate,
                tenure_months=tenure,
                start_date=today - timedelta(days=365),
                emi=emi,
                outstanding_amount=principal - (emi * 12)
            )
            db.add(loan)
        
        print_success("Added 2 loans!")
        
        # Add Insurance data
        print_info("Adding insurance policies...")
        insurances_data = [
            ("Term Insurance", "Term Life Policy", "Policy123", 25, 5000, 2000000, "Annual"),
            ("Health Insurance", "Family Health", "Policy456", 35, 15000, 500000, "Annual"),
            ("Life Insurance", "LIC Endowment", "Policy789", 30, 8000, 1000000, "Monthly"),
        ]
        
        for insurance_type, policy_name, policy_num, tenure, premium, coverage, frequency in insurances_data:
            insurance = Insurance(
                user_id=demo_user.id,
                insurance_type=insurance_type,
                policy_name=policy_name,
                policy_number=policy_num,
                tenure_years=tenure,
                premium_amount=premium,
                premium_frequency=frequency,
                coverage_amount=coverage,
                start_date=today - timedelta(days=365),
                maturity_date=today + timedelta(days=tenure*365)
            )
            db.add(insurance)
        
        print_success("Added 3 insurance policies!")
        
        # Add Credit Card data
        print_info("Adding credit cards...")
        credit_cards_data = [
            ("HDFC Credit Card", "1234", 100000, 45000, 20),
            ("ICICI Credit Card", "5678", 150000, 80000, 25),
        ]
        
        for card_name, last4, credit_limit, outstanding, due_day in credit_cards_data:
            cc = CreditCard(
                user_id=demo_user.id,
                card_name=card_name,
                card_number_last4=last4,
                credit_limit=credit_limit,
                outstanding_amount=outstanding,
                due_date=due_day
            )
            db.add(cc)
        
        print_success("Added 2 credit cards!")
        
        # Add Fixed Deposit/Lump Sum data
        print_info("Adding fixed deposits...")
        lumps_data = [
            ("HDFC FD", 500000, 6.5, 24),
            ("ICICI FD", 300000, 6.0, 36),
            ("Axis FD", 200000, 6.2, 12),
        ]
        
        for name, principal, rate, tenure in lumps_data:
            lump = LumpSum(
                user_id=demo_user.id,
                investment_name=name,
                principal=principal,
                interest_rate=rate,
                tenure_months=tenure,
                start_date=today - timedelta(days=60),
                maturity_value=principal * ((1 + rate/100)**(tenure/12)),
                maturity_date=today + timedelta(days=tenure*30)
            )
            db.add(lump)
        
        print_success("Added 3 fixed deposits!")
        
        # Add Net Worth History
        print_info("Adding net worth history...")
        for i in range(6):
            month = today - timedelta(days=30*i)
            month = month.replace(day=1)
            
            total_assets = (
                (27000 + 18250 + 29250 + 14000 + 11000) +  # Stocks
                (5000*3 * 1.01) +  # SIP
                (100000 + 75000 + 50000) * 1.01 +  # MF
                (500000 + 300000 + 200000) +  # FD
                100000  # Savings
            )
            
            total_liabilities = 15000 + 10000 + 45000 + 80000  # Loans + Credit Cards
            
            net_worth = NetWorthHistory(
                user_id=demo_user.id,
                month=month,
                total_assets=total_assets,
                total_liabilities=total_liabilities,
                net_worth=total_assets - total_liabilities
            )
            db.add(net_worth)
        
        print_success("Added net worth history for 6 months!")
        
        # Commit all changes
        db.commit()
        
        print_header("✅ Sample Data Added Successfully!")
        print_info(f"Demo User: demo@finance.com")
        print_info(f"Password: demo123")
        print_info(f"6 months of income data")
        print_info(f"10 expense categories")
        print_info(f"5 stocks (NSE)")
        print_info(f"3 SIPs")
        print_info(f"3 mutual funds")
        print_info(f"2 loans")
        print_info(f"3 insurance policies")
        print_info(f"2 credit cards")
        print_info(f"3 fixed deposits")
        
        return True
        
    except Exception as e:
        db.rollback()
        print_error(f"Failed to add sample data: {str(e)}")
        return False
    finally:
        db.close()


def verify_environment():
    """Verify environment configuration"""
    print_header("🔧 Verifying Environment Configuration")
    
    print_info(f"App Name: {settings.APP_NAME}")
    print_info(f"App Version: {settings.APP_VERSION}")
    print_info(f"Debug Mode: {settings.DEBUG}")
    print_info(f"Currency: {settings.CURRENCY_SYMBOL} {settings.CURRENCY}")
    print_info(f"Stock Market: {settings.STOCK_MARKET}")
    
    if settings.OPENAI_API_KEY:
        api_key_preview = settings.OPENAI_API_KEY[:20] + "***"
        print_success(f"OpenAI API Key configured: {api_key_preview}")
    else:
        print_info("⚠️  OpenAI API Key not configured (agents will use fallback logic)")
    
    return True


def main():
    """Main initialization function"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🚀 AI Personal Finance Application Initialization".ljust(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Step 1: Verify environment
    if not verify_environment():
        return False
    
    # Step 2: Verify database connection
    if not verify_database_connection():
        return False
    
    # Step 3: Create tables
    if not create_tables():
        return False
    
    # Step 4: Add sample data
    if not add_sample_data():
        return False
    
    # Final status
    print_header("🎉 Initialization Complete!")
    print_success("Application is ready to run!")
    print("\n" + "="*60)
    print("  📌 Next Steps:")
    print("="*60)
    print("  1. Start FastAPI Backend (in terminal 1):")
    print("     python -m uvicorn backend.main:app --reload --port 8000")
    print("\n  2. Start Streamlit Frontend (in terminal 2):")
    print("     streamlit run app.py")
    print("\n  3. Access Application:")
    print("     http://localhost:8501")
    print("\n  4. Login with Demo Account:")
    print("     Email: demo@finance.com")
    print("     Password: demo123")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
