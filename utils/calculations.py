"""
Financial calculation utilities
"""
import pandas as pd
import numpy as np
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List


class FinancialCalculator:
    """Financial calculations for various investment and loan products"""
    
    @staticmethod
    def calculate_sip_value(monthly_amount: float, annual_return: float, months: int) -> Dict[float, float]:
        """
        Calculate SIP maturity value using compound interest
        
        Args:
            monthly_amount: Monthly SIP amount
            annual_return: Expected annual return percentage
            months: Number of months
        
        Returns:
            Dict with total_invested and current_value
        """
        monthly_rate = annual_return / (12 * 100)
        
        # Future value of annuity formula
        if monthly_rate > 0:
            fv = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        else:
            fv = monthly_amount * months
        
        total_invested = monthly_amount * months
        
        return {
            "total_invested": round(total_invested, 2),
            "current_value": round(fv, 2)
        }
    
    @staticmethod
    def calculate_lump_sum_value(principal: float, annual_return: float, years: float) -> float:
        """
        Calculate lump sum maturity value
        
        Args:
            principal: Principal amount
            annual_return: Annual return percentage
            years: Time period in years
        
        Returns:
            Maturity value
        """
        maturity = principal * ((1 + annual_return/100) ** years)
        return round(maturity, 2)
    
    @staticmethod
    def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
        """
        Calculate EMI for a loan
        
        Args:
            principal: Loan principal
            annual_rate: Annual interest rate percentage
            tenure_months: Loan tenure in months
        
        Returns:
            Monthly EMI amount
        """
        monthly_rate = annual_rate / (12 * 100)
        
        if monthly_rate > 0:
            emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
        else:
            emi = principal / tenure_months
        
        return round(emi, 2)
    
    @staticmethod
    def calculate_loan_schedule(principal: float, annual_rate: float, tenure_months: int, emi: float) -> pd.DataFrame:
        """
        Generate loan amortization schedule
        
        Args:
            principal: Loan principal
            annual_rate: Annual interest rate
            tenure_months: Loan tenure in months
            emi: Monthly EMI
        
        Returns:
            DataFrame with amortization schedule
        """
        monthly_rate = annual_rate / (12 * 100)
        
        schedule = []
        balance = principal
        
        for month in range(1, tenure_months + 1):
            interest = balance * monthly_rate
            principal_paid = emi - interest
            balance -= principal_paid
            
            schedule.append({
                "month": month,
                "emi": emi,
                "interest": round(interest, 2),
                "principal": round(principal_paid, 2),
                "balance": round(max(balance, 0), 2)
            })
        
        return pd.DataFrame(schedule)
    
    @staticmethod
    def calculate_months_between(start_date: date, end_date: date = None) -> int:
        """
        Calculate number of months between two dates
        
        Args:
            start_date: Start date
            end_date: End date (default: today)
        
        Returns:
            Number of months
        """
        if end_date is None:
            end_date = date.today()
        
        delta = relativedelta(end_date, start_date)
        return delta.years * 12 + delta.months
    
    @staticmethod
    def calculate_cagr(initial_value: float, final_value: float, years: float) -> float:
        """
        Calculate Compound Annual Growth Rate (CAGR)
        
        Args:
            initial_value: Initial investment value
            final_value: Final value
            years: Time period in years
        
        Returns:
            CAGR percentage
        """
        if initial_value <= 0 or years <= 0:
            return 0.0
        
        cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
        return round(cagr, 2)
    
    @staticmethod
    def calculate_xirr(cashflows: List[Dict[str, float]], dates: List[date]) -> float:
        """
        Calculate XIRR (Extended Internal Rate of Return)
        
        Args:
            cashflows: List of cashflow amounts (negative for investment, positive for returns)
            dates: Corresponding dates
        
        Returns:
            XIRR percentage
        """
        # Simplified implementation using Newton-Raphson method
        # For production, use numpy-financial's irr function
        
        if len(cashflows) != len(dates):
            return 0.0
        
        # Convert dates to years from first date
        first_date = dates[0]
        years = [(d - first_date).days / 365.25 for d in dates]
        
        # Initial guess
        rate = 0.1
        
        for _ in range(100):  # Max iterations
            npv = sum(cf / ((1 + rate) ** y) for cf, y in zip(cashflows, years))
            dnpv = sum(-cf * y / ((1 + rate) ** (y + 1)) for cf, y in zip(cashflows, years))
            
            if abs(dnpv) < 1e-6:
                break
            
            rate = rate - npv / dnpv
        
        return round(rate * 100, 2)
    
    @staticmethod
    def calculate_tax_savings(investment_amount: float, tax_rate: float = 30.0) -> float:
        """
        Calculate tax savings under 80C (₹1.5 lakh limit)
        
        Args:
            investment_amount: Investment amount
            tax_rate: Tax rate percentage
        
        Returns:
            Tax savings amount
        """
        max_80c = 150000  # ₹1.5 lakh limit
        eligible_amount = min(investment_amount, max_80c)
        tax_savings = eligible_amount * (tax_rate / 100)
        
        return round(tax_savings, 2)
    
    @staticmethod
    def calculate_net_worth(assets: Dict[str, float], liabilities: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate net worth
        
        Args:
            assets: Dictionary of asset categories and values
            liabilities: Dictionary of liability categories and values
        
        Returns:
            Dictionary with total assets, liabilities, and net worth
        """
        total_assets = sum(assets.values())
        total_liabilities = sum(liabilities.values())
        net_worth = total_assets - total_liabilities
        
        return {
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(total_liabilities, 2),
            "net_worth": round(net_worth, 2)
        }
    
    @staticmethod
    def calculate_investment_allocation(total_amount: float, percentages: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate investment allocation based on percentages
        
        Args:
            total_amount: Total investable amount
            percentages: Dictionary of investment categories and their percentages
        
        Returns:
            Dictionary with allocated amounts
        """
        allocation = {}
        
        for category, percentage in percentages.items():
            allocation[category] = round(total_amount * (percentage / 100), 2)
        
        return allocation
    
    @staticmethod
    def calculate_emergency_fund(monthly_expenses: float, months: int = 6) -> float:
        """
        Calculate recommended emergency fund
        
        Args:
            monthly_expenses: Average monthly expenses
            months: Number of months to cover (default: 6)
        
        Returns:
            Emergency fund amount
        """
        return round(monthly_expenses * months, 2)


# Global instance
financial_calculator = FinancialCalculator()
