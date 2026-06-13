"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class RiskLevelEnum(str, Enum):
    """Risk level enumeration"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Income Schemas
class IncomeCreate(BaseModel):
    user_id: int = Field(default=1)
    month: date
    salary: float = Field(ge=0)
    other_income: float = Field(default=0, ge=0)
    other_income_source: Optional[str] = None


class IncomeResponse(BaseModel):
    id: int
    user_id: int
    month: date
    salary: float
    other_income: float
    other_income_source: Optional[str]
    total_income: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Expense Schemas
class ExpenseCreate(BaseModel):
    user_id: int = Field(default=1)
    month: date
    category: str
    amount: float = Field(gt=0)
    description: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    month: date
    category: str
    amount: float
    description: Optional[str]
    is_anomaly: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Stock Schemas
class StockCreate(BaseModel):
    user_id: int = Field(default=1)
    company_name: str
    symbol: str
    quantity: int = Field(gt=0)
    purchase_price: float = Field(gt=0)
    purchase_date: date


class StockResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    symbol: str
    quantity: int
    purchase_price: float
    purchase_date: date
    current_price: Optional[float]
    current_value: Optional[float]
    last_updated: Optional[datetime]
    
    class Config:
        from_attributes = True


# SIP Schemas
class SIPCreate(BaseModel):
    user_id: int = Field(default=1)
    fund_name: str
    monthly_amount: float = Field(gt=0)
    start_date: date
    expected_return_rate: float = Field(ge=0)


class SIPResponse(BaseModel):
    id: int
    user_id: int
    fund_name: str
    monthly_amount: float
    start_date: date
    expected_return_rate: float
    total_invested: float
    current_value: float
    is_active: bool
    
    class Config:
        from_attributes = True


# Mutual Fund Schemas
class MutualFundCreate(BaseModel):
    user_id: int = Field(default=1)
    fund_name: str
    investment_amount: float = Field(gt=0)
    investment_date: date
    expected_return_rate: float = Field(ge=0)


class MutualFundResponse(BaseModel):
    id: int
    user_id: int
    fund_name: str
    investment_amount: float
    investment_date: date
    expected_return_rate: float
    current_value: Optional[float]
    
    class Config:
        from_attributes = True


# SWP Schemas
class SWPCreate(BaseModel):
    user_id: int = Field(default=1)
    source_investment_type: str
    source_investment_id: int
    monthly_withdrawal: float = Field(gt=0)
    start_date: date
    linked_loan_id: Optional[int] = None


class SWPResponse(BaseModel):
    id: int
    user_id: int
    source_investment_type: str
    source_investment_id: int
    monthly_withdrawal: float
    start_date: date
    is_active: bool
    linked_loan_id: Optional[int]
    
    class Config:
        from_attributes = True


# Loan Schemas
class LoanCreate(BaseModel):
    user_id: int = Field(default=1)
    loan_type: str
    principal_amount: float = Field(gt=0)
    interest_rate: float = Field(gt=0)
    tenure_months: int = Field(gt=0)
    start_date: date


class LoanResponse(BaseModel):
    id: int
    user_id: int
    loan_type: str
    principal_amount: float
    interest_rate: float
    tenure_months: int
    emi: float
    outstanding_amount: float
    start_date: date
    is_active: bool
    
    class Config:
        from_attributes = True


# Insurance Schemas
class InsuranceCreate(BaseModel):
    user_id: int = Field(default=1)
    insurance_type: str
    policy_name: str
    policy_number: str
    premium_amount: float = Field(gt=0)
    premium_frequency: str
    coverage_amount: float = Field(gt=0)
    tenure_years: int = Field(gt=0)
    start_date: date


class InsuranceResponse(BaseModel):
    id: int
    user_id: int
    insurance_type: str
    policy_name: str
    policy_number: str
    premium_amount: float
    premium_frequency: str
    coverage_amount: float
    tenure_years: int
    start_date: date
    maturity_date: Optional[date]
    is_active: bool
    
    class Config:
        from_attributes = True


# Credit Card Schemas
class CreditCardCreate(BaseModel):
    user_id: int = Field(default=1)
    card_name: str
    card_number_last4: str = Field(min_length=4, max_length=4)
    credit_limit: float = Field(gt=0)
    outstanding_amount: float = Field(default=0, ge=0)
    due_date: int = Field(ge=1, le=31)


class CreditCardResponse(BaseModel):
    id: int
    user_id: int
    card_name: str
    card_number_last4: str
    credit_limit: float
    outstanding_amount: float
    due_date: int
    
    class Config:
        from_attributes = True


# Lump Sum Schemas
class LumpSumCreate(BaseModel):
    user_id: int = Field(default=1)
    investment_name: str
    principal: float = Field(gt=0)
    interest_rate: float = Field(ge=0)
    tenure_months: int = Field(gt=0)
    start_date: date


class LumpSumResponse(BaseModel):
    id: int
    user_id: int
    investment_name: str
    principal: float
    interest_rate: float
    tenure_months: int
    start_date: date
    maturity_value: Optional[float]
    maturity_date: Optional[date]
    is_active: bool
    
    class Config:
        from_attributes = True


# Net Worth Schemas
class NetWorthResponse(BaseModel):
    id: int
    user_id: int
    month: date
    total_stocks_value: float
    total_sip_value: float
    total_mutual_fund_value: float
    total_lump_sum_value: float
    savings: float
    total_assets: float
    total_loan_outstanding: float
    total_credit_card_outstanding: float
    total_liabilities: float
    net_worth: float
    predicted_next_month: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# AI Investment Suggestion Input
class InvestmentSuggestionInput(BaseModel):
    salary: float = Field(gt=0)
    expenses: float = Field(ge=0)
    other_income: float = Field(default=0, ge=0)
    risk_level: RiskLevelEnum


# AI Investment Suggestion Output
class InvestmentAllocation(BaseModel):
    sip: float
    mutual_funds: float
    stocks: float
    fd: float
    savings: float
    insurance: float


class InvestmentSuggestionOutput(BaseModel):
    total_investable: float
    risk_level: str
    allocation: InvestmentAllocation
    recommendations: List[str]
