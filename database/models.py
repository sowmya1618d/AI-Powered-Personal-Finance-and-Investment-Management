"""
SQLAlchemy database models for personal finance application
Comprehensive schema for India-specific financial tracking
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import enum


class RiskLevel(enum.Enum):
    """Risk level enumeration"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class User(Base):
    """User model for multi-user support"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    incomes = relationship("Income", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    stocks = relationship("Stock", back_populates="user", cascade="all, delete-orphan")
    sips = relationship("SIP", back_populates="user", cascade="all, delete-orphan")
    mutual_funds = relationship("MutualFund", back_populates="user", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    insurances = relationship("Insurance", back_populates="user", cascade="all, delete-orphan")
    credit_cards = relationship("CreditCard", back_populates="user", cascade="all, delete-orphan")
    lump_sums = relationship("LumpSum", back_populates="user", cascade="all, delete-orphan")
    net_worth_history = relationship("NetWorthHistory", back_populates="user", cascade="all, delete-orphan")
    swps = relationship("SWP", back_populates="user", cascade="all, delete-orphan")


class Income(Base):
    """Monthly income tracking"""
    __tablename__ = "incomes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Date, nullable=False, index=True)
    salary = Column(Float, default=0.0)
    other_income = Column(Float, default=0.0)
    other_income_source = Column(String(255), nullable=True)
    total_income = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="incomes")


class Expense(Base):
    """Category-wise expense tracking"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Date, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    is_anomaly = Column(Boolean, default=False)  # Detected by autoencoder
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="expenses")


class Stock(Base):
    """Stock portfolio tracking (NSE)"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(255), nullable=False)
    symbol = Column(String(50), nullable=False)  # e.g., "RELIANCE.NS"
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    current_price = Column(Float, nullable=True)  # Updated via API
    current_value = Column(Float, nullable=True)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="stocks")


class SIP(Base):
    """Systematic Investment Plan tracking"""
    __tablename__ = "sips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_name = Column(String(255), nullable=False)
    monthly_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    expected_return_rate = Column(Float, nullable=False)  # Annual %
    total_invested = Column(Float, default=0.0)
    current_value = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="sips")


class MutualFund(Base):
    """Mutual fund (lump sum) tracking"""
    __tablename__ = "mutual_funds"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_name = Column(String(255), nullable=False)
    investment_amount = Column(Float, nullable=False)
    investment_date = Column(Date, nullable=False)
    expected_return_rate = Column(Float, nullable=False)  # Annual %
    current_value = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="mutual_funds")


class SWP(Base):
    """Systematic Withdrawal Plan"""
    __tablename__ = "swps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_investment_type = Column(String(100), nullable=False)  # SIP, MutualFund, etc.
    source_investment_id = Column(Integer, nullable=False)
    monthly_withdrawal = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    linked_loan_id = Column(Integer, ForeignKey("loans.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="swps")
    linked_loan = relationship("Loan", foreign_keys=[linked_loan_id])


class Loan(Base):
    """Loan tracking (Home, Personal, Mortgage)"""
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_type = Column(String(100), nullable=False)
    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)  # Annual %
    tenure_months = Column(Integer, nullable=False)
    emi = Column(Float, nullable=False)
    outstanding_amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="loans")


class Insurance(Base):
    """Insurance policy tracking"""
    __tablename__ = "insurances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insurance_type = Column(String(100), nullable=False)
    policy_name = Column(String(255), nullable=False)
    policy_number = Column(String(100), unique=True, nullable=False)
    premium_amount = Column(Float, nullable=False)
    premium_frequency = Column(String(50), nullable=False)  # Monthly, Quarterly, Annual
    coverage_amount = Column(Float, nullable=False)
    tenure_years = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    maturity_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="insurances")


class CreditCard(Base):
    """Credit card tracking"""
    __tablename__ = "credit_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_name = Column(String(255), nullable=False)
    card_number_last4 = Column(String(4), nullable=False)
    credit_limit = Column(Float, nullable=False)
    outstanding_amount = Column(Float, default=0.0)
    due_date = Column(Integer, nullable=False)  # Day of month
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="credit_cards")


class LumpSum(Base):
    """Lump sum investment tracking (FD, etc.)"""
    __tablename__ = "lump_sums"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    investment_name = Column(String(255), nullable=False)
    principal = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)  # Annual %
    tenure_months = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    maturity_value = Column(Float, nullable=True)
    maturity_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="lump_sums")


class NetWorthHistory(Base):
    """Monthly net worth snapshot"""
    __tablename__ = "net_worth_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month = Column(Date, nullable=False, unique=True, index=True)
    
    # Assets
    total_stocks_value = Column(Float, default=0.0)
    total_sip_value = Column(Float, default=0.0)
    total_mutual_fund_value = Column(Float, default=0.0)
    total_lump_sum_value = Column(Float, default=0.0)
    savings = Column(Float, default=0.0)
    total_assets = Column(Float, nullable=False)
    
    # Liabilities
    total_loan_outstanding = Column(Float, default=0.0)
    total_credit_card_outstanding = Column(Float, default=0.0)
    total_liabilities = Column(Float, nullable=False)
    
    # Net Worth
    net_worth = Column(Float, nullable=False)
    
    # ML Predictions
    predicted_next_month = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="net_worth_history")
