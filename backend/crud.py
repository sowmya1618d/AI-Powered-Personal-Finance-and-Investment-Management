"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from typing import List, Optional
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from database import models
from backend import schemas


# ============= INCOME CRUD =============
def create_income(db: Session, income: schemas.IncomeCreate):
    """Create income record"""
    total = income.salary + income.other_income
    db_income = models.Income(
        **income.model_dump(),
        total_income=total
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def get_incomes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all incomes for a user"""
    return db.query(models.Income).filter(
        models.Income.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_income_by_month(db: Session, user_id: int, month: date):
    """Get income for specific month"""
    return db.query(models.Income).filter(
        and_(
            models.Income.user_id == user_id,
            models.Income.month == month
        )
    ).first()


# ============= EXPENSE CRUD =============
def create_expense(db: Session, expense: schemas.ExpenseCreate):
    """Create expense record"""
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all expenses for a user"""
    return db.query(models.Expense).filter(
        models.Expense.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_expenses_by_month(db: Session, user_id: int, month: date):
    """Get expenses for specific month"""
    return db.query(models.Expense).filter(
        and_(
            models.Expense.user_id == user_id,
            models.Expense.month == month
        )
    ).all()


def get_total_expenses_by_month(db: Session, user_id: int, month: date) -> float:
    """Calculate total expenses for a month"""
    expenses = get_expenses_by_month(db, user_id, month)
    return sum(exp.amount for exp in expenses)


# ============= STOCK CRUD =============
def create_stock(db: Session, stock: schemas.StockCreate):
    """Create stock record"""
    db_stock = models.Stock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_stocks_by_user(db: Session, user_id: int):
    """Get all stocks for a user"""
    return db.query(models.Stock).filter(models.Stock.user_id == user_id).all()


def update_stock_price(db: Session, stock_id: int, current_price: float):
    """Update stock current price and value"""
    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if stock:
        stock.current_price = current_price
        stock.current_value = current_price * stock.quantity
        stock.last_updated = datetime.now()
        db.commit()
        db.refresh(stock)
    return stock


# ============= SIP CRUD =============
def create_sip(db: Session, sip: schemas.SIPCreate):
    """Create SIP record"""
    db_sip = models.SIP(**sip.model_dump())
    db.add(db_sip)
    db.commit()
    db.refresh(db_sip)
    return db_sip


def get_sips_by_user(db: Session, user_id: int):
    """Get all SIPs for a user"""
    return db.query(models.SIP).filter(models.SIP.user_id == user_id).all()


def update_sip_values(db: Session, sip_id: int, total_invested: float, current_value: float):
    """Update SIP invested and current values"""
    sip = db.query(models.SIP).filter(models.SIP.id == sip_id).first()
    if sip:
        sip.total_invested = total_invested
        sip.current_value = current_value
        db.commit()
        db.refresh(sip)
    return sip


# ============= MUTUAL FUND CRUD =============
def create_mutual_fund(db: Session, mf: schemas.MutualFundCreate):
    """Create mutual fund record"""
    db_mf = models.MutualFund(**mf.model_dump())
    db.add(db_mf)
    db.commit()
    db.refresh(db_mf)
    return db_mf


def get_mutual_funds_by_user(db: Session, user_id: int):
    """Get all mutual funds for a user"""
    return db.query(models.MutualFund).filter(models.MutualFund.user_id == user_id).all()


# ============= SWP CRUD =============
def create_swp(db: Session, swp: schemas.SWPCreate):
    """Create SWP record"""
    db_swp = models.SWP(**swp.model_dump())
    db.add(db_swp)
    db.commit()
    db.refresh(db_swp)
    return db_swp


def get_swps_by_user(db: Session, user_id: int):
    """Get all SWPs for a user"""
    return db.query(models.SWP).filter(models.SWP.user_id == user_id).all()


# ============= LOAN CRUD =============
def create_loan(db: Session, loan: schemas.LoanCreate):
    """Create loan record with EMI calculation"""
    # Calculate EMI using formula: P * r * (1+r)^n / ((1+r)^n - 1)
    P = loan.principal_amount
    r = loan.interest_rate / (12 * 100)  # Monthly interest rate
    n = loan.tenure_months
    
    emi = P * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    
    db_loan = models.Loan(
        **loan.model_dump(),
        emi=round(emi, 2),
        outstanding_amount=P
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_loans_by_user(db: Session, user_id: int):
    """Get all loans for a user"""
    return db.query(models.Loan).filter(models.Loan.user_id == user_id).all()


def update_loan_outstanding(db: Session, loan_id: int, new_outstanding: float):
    """Update loan outstanding amount"""
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if loan:
        loan.outstanding_amount = new_outstanding
        if new_outstanding <= 0:
            loan.is_active = False
        db.commit()
        db.refresh(loan)
    return loan


# ============= INSURANCE CRUD =============
def create_insurance(db: Session, insurance: schemas.InsuranceCreate):
    """Create insurance record"""
    maturity_date = insurance.start_date + relativedelta(years=insurance.tenure_years)
    db_insurance = models.Insurance(
        **insurance.model_dump(),
        maturity_date=maturity_date
    )
    db.add(db_insurance)
    db.commit()
    db.refresh(db_insurance)
    return db_insurance


def get_insurances_by_user(db: Session, user_id: int):
    """Get all insurances for a user"""
    return db.query(models.Insurance).filter(models.Insurance.user_id == user_id).all()


# ============= CREDIT CARD CRUD =============
def create_credit_card(db: Session, card: schemas.CreditCardCreate):
    """Create credit card record"""
    db_card = models.CreditCard(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def get_credit_cards_by_user(db: Session, user_id: int):
    """Get all credit cards for a user"""
    return db.query(models.CreditCard).filter(models.CreditCard.user_id == user_id).all()


def update_credit_card_outstanding(db: Session, card_id: int, new_outstanding: float):
    """Update credit card outstanding"""
    card = db.query(models.CreditCard).filter(models.CreditCard.id == card_id).first()
    if card:
        card.outstanding_amount = new_outstanding
        db.commit()
        db.refresh(card)
    return card


# ============= LUMP SUM CRUD =============
def create_lump_sum(db: Session, lump_sum: schemas.LumpSumCreate):
    """Create lump sum investment record"""
    # Calculate maturity value: A = P(1 + r/100)^t
    P = lump_sum.principal
    r = lump_sum.interest_rate
    t = lump_sum.tenure_months / 12
    
    maturity_value = P * ((1 + r/100) ** t)
    maturity_date = lump_sum.start_date + relativedelta(months=lump_sum.tenure_months)
    
    db_lump_sum = models.LumpSum(
        **lump_sum.model_dump(),
        maturity_value=round(maturity_value, 2),
        maturity_date=maturity_date
    )
    db.add(db_lump_sum)
    db.commit()
    db.refresh(db_lump_sum)
    return db_lump_sum


def get_lump_sums_by_user(db: Session, user_id: int):
    """Get all lump sum investments for a user"""
    return db.query(models.LumpSum).filter(models.LumpSum.user_id == user_id).all()


# ============= NET WORTH CRUD =============
def create_net_worth_snapshot(db: Session, user_id: int, month: date, data: dict):
    """Create monthly net worth snapshot"""
    db_net_worth = models.NetWorthHistory(
        user_id=user_id,
        month=month,
        **data
    )
    db.add(db_net_worth)
    db.commit()
    db.refresh(db_net_worth)
    return db_net_worth


def get_net_worth_history(db: Session, user_id: int, limit: int = 12):
    """Get net worth history for a user"""
    return db.query(models.NetWorthHistory).filter(
        models.NetWorthHistory.user_id == user_id
    ).order_by(models.NetWorthHistory.month.desc()).limit(limit).all()


def get_latest_net_worth(db: Session, user_id: int):
    """Get latest net worth snapshot"""
    return db.query(models.NetWorthHistory).filter(
        models.NetWorthHistory.user_id == user_id
    ).order_by(models.NetWorthHistory.month.desc()).first()
