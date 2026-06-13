"""
FastAPI main application
RESTful API for personal finance management
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from datetime import datetime

from database.connection import get_db, init_db
from backend import crud, schemas
from config.settings import settings
from utils.calculations import financial_calculator
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal finance and investment management API for India"
)

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def setup_database_on_startup():
    """Ensure database tables are created on application startup"""
    try:
        init_db()
        print("✅ Database initialized on startup")
    except Exception as e:
        print(f"❌ Failed to initialize database on startup: {e}")


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# ============= INCOME ENDPOINTS =============
@app.post("/api/income", response_model=schemas.IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    """Create new income record"""
    return crud.create_income(db, income)


@app.get("/api/income/{user_id}", response_model=List[schemas.IncomeResponse])
def get_incomes(user_id: int, db: Session = Depends(get_db)):
    """Get all incomes for a user"""
    return crud.get_incomes_by_user(db, user_id)


@app.get("/api/income/{user_id}/{month}", response_model=schemas.IncomeResponse)
def get_income_by_month(user_id: int, month: date, db: Session = Depends(get_db)):
    """Get income for specific month"""
    income = crud.get_income_by_month(db, user_id, month)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found for this month")
    return income


# ============= EXPENSE ENDPOINTS =============
@app.post("/api/expense", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """Create new expense record"""
    return crud.create_expense(db, expense)


@app.get("/api/expense/{user_id}", response_model=List[schemas.ExpenseResponse])
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    """Get all expenses for a user"""
    return crud.get_expenses_by_user(db, user_id)


@app.get("/api/expense/{user_id}/{month}", response_model=List[schemas.ExpenseResponse])
def get_expenses_by_month(user_id: int, month: date, db: Session = Depends(get_db)):
    """Get expenses for specific month"""
    return crud.get_expenses_by_month(db, user_id, month)


# ============= STOCK ENDPOINTS =============
@app.post("/api/stock", response_model=schemas.StockResponse, status_code=status.HTTP_201_CREATED)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    """Create new stock investment"""
    return crud.create_stock(db, stock)


@app.get("/api/stock/{user_id}", response_model=List[schemas.StockResponse])
def get_stocks(user_id: int, db: Session = Depends(get_db)):
    """Get all stocks for a user"""
    return crud.get_stocks_by_user(db, user_id)


@app.put("/api/stock/{stock_id}/price")
def update_stock_price(stock_id: int, current_price: float, db: Session = Depends(get_db)):
    """Update stock current price"""
    stock = crud.update_stock_price(db, stock_id, current_price)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


# ============= SIP ENDPOINTS =============
@app.post("/api/sip", response_model=schemas.SIPResponse, status_code=status.HTTP_201_CREATED)
def create_sip(sip: schemas.SIPCreate, db: Session = Depends(get_db)):
    """Create new SIP"""
    return crud.create_sip(db, sip)


@app.get("/api/sip/{user_id}", response_model=List[schemas.SIPResponse])
def get_sips(user_id: int, db: Session = Depends(get_db)):
    """Get all SIPs for a user"""
    return crud.get_sips_by_user(db, user_id)


@app.put("/api/sip/{sip_id}/values")
def update_sip_values(sip_id: int, total_invested: float, current_value: float, db: Session = Depends(get_db)):
    """Update SIP values"""
    sip = crud.update_sip_values(db, sip_id, total_invested, current_value)
    if not sip:
        raise HTTPException(status_code=404, detail="SIP not found")
    return sip


# ============= MUTUAL FUND ENDPOINTS =============
@app.post("/api/mutual-fund", response_model=schemas.MutualFundResponse, status_code=status.HTTP_201_CREATED)
def create_mutual_fund(mf: schemas.MutualFundCreate, db: Session = Depends(get_db)):
    """Create new mutual fund investment"""
    return crud.create_mutual_fund(db, mf)


@app.get("/api/mutual-fund/{user_id}", response_model=List[schemas.MutualFundResponse])
def get_mutual_funds(user_id: int, db: Session = Depends(get_db)):
    """Get all mutual funds for a user"""
    return crud.get_mutual_funds_by_user(db, user_id)


# ============= SWP ENDPOINTS =============
@app.post("/api/swp", response_model=schemas.SWPResponse, status_code=status.HTTP_201_CREATED)
def create_swp(swp: schemas.SWPCreate, db: Session = Depends(get_db)):
    """Create new SWP"""
    return crud.create_swp(db, swp)


@app.get("/api/swp/{user_id}", response_model=List[schemas.SWPResponse])
def get_swps(user_id: int, db: Session = Depends(get_db)):
    """Get all SWPs for a user"""
    return crud.get_swps_by_user(db, user_id)


# ============= LOAN ENDPOINTS =============
@app.post("/api/loan", response_model=schemas.LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """Create new loan"""
    return crud.create_loan(db, loan)


@app.get("/api/loan/{user_id}", response_model=List[schemas.LoanResponse])
def get_loans(user_id: int, db: Session = Depends(get_db)):
    """Get all loans for a user"""
    return crud.get_loans_by_user(db, user_id)


@app.put("/api/loan/{loan_id}/outstanding")
def update_loan_outstanding(loan_id: int, new_outstanding: float, db: Session = Depends(get_db)):
    """Update loan outstanding amount"""
    loan = crud.update_loan_outstanding(db, loan_id, new_outstanding)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


# ============= INSURANCE ENDPOINTS =============
@app.post("/api/insurance", response_model=schemas.InsuranceResponse, status_code=status.HTTP_201_CREATED)
def create_insurance(insurance: schemas.InsuranceCreate, db: Session = Depends(get_db)):
    """Create new insurance policy"""
    return crud.create_insurance(db, insurance)


@app.get("/api/insurance/{user_id}", response_model=List[schemas.InsuranceResponse])
def get_insurances(user_id: int, db: Session = Depends(get_db)):
    """Get all insurance policies for a user"""
    return crud.get_insurances_by_user(db, user_id)


# ============= CREDIT CARD ENDPOINTS =============
@app.post("/api/credit-card", response_model=schemas.CreditCardResponse, status_code=status.HTTP_201_CREATED)
def create_credit_card(card: schemas.CreditCardCreate, db: Session = Depends(get_db)):
    """Create new credit card"""
    return crud.create_credit_card(db, card)


@app.get("/api/credit-card/{user_id}", response_model=List[schemas.CreditCardResponse])
def get_credit_cards(user_id: int, db: Session = Depends(get_db)):
    """Get all credit cards for a user"""
    return crud.get_credit_cards_by_user(db, user_id)


@app.put("/api/credit-card/{card_id}/outstanding")
def update_credit_card_outstanding(card_id: int, new_outstanding: float, db: Session = Depends(get_db)):
    """Update credit card outstanding"""
    card = crud.update_credit_card_outstanding(db, card_id, new_outstanding)
    if not card:
        raise HTTPException(status_code=404, detail="Credit card not found")
    return card


# ============= LUMP SUM ENDPOINTS =============
@app.post("/api/lump-sum", response_model=schemas.LumpSumResponse, status_code=status.HTTP_201_CREATED)
def create_lump_sum(lump_sum: schemas.LumpSumCreate, db: Session = Depends(get_db)):
    """Create new lump sum investment"""
    return crud.create_lump_sum(db, lump_sum)


@app.get("/api/lump-sum/{user_id}", response_model=List[schemas.LumpSumResponse])
def get_lump_sums(user_id: int, db: Session = Depends(get_db)):
    """Get all lump sum investments for a user"""
    return crud.get_lump_sums_by_user(db, user_id)


# ============= NET WORTH ENDPOINTS =============
@app.get("/api/net-worth/{user_id}", response_model=List[schemas.NetWorthResponse])
def get_net_worth_history(user_id: int, limit: int = 12, db: Session = Depends(get_db)):
    """Get net worth history for a user"""
    return crud.get_net_worth_history(db, user_id, limit)


@app.get("/api/net-worth/{user_id}/latest", response_model=schemas.NetWorthResponse)
def get_latest_net_worth(user_id: int, db: Session = Depends(get_db)):
    """Get latest net worth snapshot"""
    net_worth = crud.get_latest_net_worth(db, user_id)
    if not net_worth:
        raise HTTPException(status_code=404, detail="No net worth data found")
    return net_worth


@app.post("/api/net-worth/snapshot", response_model=schemas.NetWorthResponse, status_code=status.HTTP_201_CREATED)
def create_net_worth_snapshot(user_id: int = 1, month: date = date.today(), db: Session = Depends(get_db)):
    """Calculate and store a monthly net worth snapshot"""
    snapshot_data = compute_snapshot_data(db, user_id, month)
    snapshot = crud.create_net_worth_snapshot(db, user_id, month, snapshot_data)
    return snapshot


def compute_snapshot_data(db: Session, user_id: int, month: date) -> dict:
    """Compute net worth snapshot data for a user and month"""
    stocks = crud.get_stocks_by_user(db, user_id)
    sips = crud.get_sips_by_user(db, user_id)
    mutual_funds = crud.get_mutual_funds_by_user(db, user_id)
    lump_sums = crud.get_lump_sums_by_user(db, user_id)
    loans = crud.get_loans_by_user(db, user_id)
    credit_cards = crud.get_credit_cards_by_user(db, user_id)

    total_stocks_value = sum((s.current_value or 0) for s in stocks)
    total_sip_value = sum((s.current_value or 0) for s in sips)
    total_mutual_fund_value = sum((m.current_value or 0) for m in mutual_funds)
    total_lump_sum_value = sum((l.maturity_value or 0) for l in lump_sums)

    income = crud.get_income_by_month(db, user_id, month)
    expenses = crud.get_expenses_by_month(db, user_id, month)
    monthly_income = income.total_income if income else 0.0
    monthly_expense = sum(e.amount for e in expenses) if expenses else 0.0
    savings = monthly_income - monthly_expense

    total_assets = total_stocks_value + total_sip_value + total_mutual_fund_value + total_lump_sum_value + max(savings, 0)

    total_loan_outstanding = sum((l.outstanding_amount or 0) for l in loans)
    total_credit_card_outstanding = sum((c.outstanding_amount or 0) for c in credit_cards)
    total_liabilities = total_loan_outstanding + total_credit_card_outstanding

    net_worth = total_assets - total_liabilities

    return {
        "total_stocks_value": round(total_stocks_value, 2),
        "total_sip_value": round(total_sip_value, 2),
        "total_mutual_fund_value": round(total_mutual_fund_value, 2),
        "total_lump_sum_value": round(total_lump_sum_value, 2),
        "savings": round(max(savings, 0), 2),
        "total_assets": round(total_assets, 2),
        "total_loan_outstanding": round(total_loan_outstanding, 2),
        "total_credit_card_outstanding": round(total_credit_card_outstanding, 2),
        "total_liabilities": round(total_liabilities, 2),
        "net_worth": round(net_worth, 2),
        "predicted_next_month": None,
    }


def _scheduled_monthly_snapshot():
    """Background task to store monthly net worth snapshot for default user"""
    from database.connection import SessionLocal
    db = SessionLocal()
    try:
        today = date.today()
        month_start = today.replace(day=1)
        data = compute_snapshot_data(db, user_id=1, month=month_start)
        # Upsert-like behavior: simply create a new snapshot for this month
        crud.create_net_worth_snapshot(db, user_id=1, month=month_start, data=data)
    except Exception as e:
        print(f"Scheduler error: {e}")
    finally:
        db.close()


def start_scheduler():
    """Start background scheduler for monthly automation"""
    scheduler = BackgroundScheduler()
    # Run once daily; inside it we store snapshot for the month
    scheduler.add_job(_scheduled_monthly_snapshot, 'interval', days=1, id='monthly_snapshot_job', replace_existing=True)
    scheduler.start()
    print("🗓️ Scheduler started: monthly snapshot job active")
    atexit.register(lambda: scheduler.shutdown(wait=False))


if __name__ == "__main__":
    import uvicorn
    start_scheduler()
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
