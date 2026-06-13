"""
Configuration settings for the AI Personal Finance Application
"""
import os
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application Info
    APP_NAME: str = "AI Personal Finance Manager"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "finance_user"
    DB_PASSWORD: str = "your_password"
    DB_NAME: str = "finance_db"
    
    # FastAPI Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # OpenAI Configuration (for AI Agents)
    OPENAI_API_KEY: Optional[str] = None
    
    # Currency
    CURRENCY: str = "INR"
    CURRENCY_SYMBOL: str = "₹"
    
    # Stock Market
    STOCK_MARKET: str = "NSE"
    STOCK_SUFFIX: str = ".NS"  # For yfinance NSE stocks
    
    # Risk Levels
    RISK_LEVELS: list = ["Low", "Medium", "High"]
    
    # Investment Categories
    INVESTMENT_CATEGORIES: list = [
        "SIP",
        "Mutual Funds",
        "Stocks",
        "Fixed Deposit",
        "Savings",
        "Insurance"
    ]
    
    # Loan Types
    LOAN_TYPES: list = [
        "Home Loan",
        "Personal Loan",
        "Mortgage Loan"
    ]
    
    # Insurance Types
    INSURANCE_TYPES: list = [
        "Term Insurance",
        "Life Insurance",
        "Health Insurance",
        "Child Insurance",
        "Retirement Insurance"
    ]
    
    # Expense Categories
    EXPENSE_CATEGORIES: list = [
        "Food & Dining",
        "Transportation",
        "Shopping",
        "Entertainment",
        "Bills & Utilities",
        "Healthcare",
        "Education",
        "Travel",
        "EMI Payments",
        "Others"
    ]
    
    # ML Model Parameters
    LSTM_LOOKBACK: int = 12  # months
    LSTM_FORECAST_PERIOD: int = 6  # months
    XGBOOST_FEATURES: int = 10
    AUTOENCODER_THRESHOLD: float = 0.8
    
    # File Paths
    MODEL_PATH: str = "ml_models/saved_models/"
    REPORT_PATH: str = "reports/"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL with properly encoded password"""
        # URL-encode the password to handle special characters like @
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
