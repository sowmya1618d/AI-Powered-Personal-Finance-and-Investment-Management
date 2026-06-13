"""
LangChain AI Agents for Financial Analysis
Multiple specialized agents for different financial tasks
"""
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from typing import Dict, List, Optional
import os


class MarketDataAgent:
    """Agent for analyzing market data and trends"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize market data agent"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("⚠️ OpenAI API key not found. Agent will use fallback responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo",
                api_key=self.api_key
            )
    
    def analyze_stock(self, symbol: str, current_price: float) -> Dict:
        """
        Analyze stock and provide insights
        
        Args:
            symbol: Stock symbol
            current_price: Current stock price
        
        Returns:
            Analysis dictionary
        """
        if not self.llm:
            return self._fallback_stock_analysis(symbol, current_price)
        
        prompt = f"""
        Analyze the Indian NSE stock {symbol} trading at ₹{current_price}.
        
        Provide:
        1. Brief company overview
        2. Current market sentiment
        3. Buy/Hold/Sell recommendation
        4. Risk factors
        
        Keep analysis concise and India-focused.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "symbol": symbol,
                "current_price": current_price,
                "analysis": response.content,
                "source": "ai_agent"
            }
        except Exception as e:
            print(f"Error in stock analysis: {e}")
            return self._fallback_stock_analysis(symbol, current_price)
    
    def _fallback_stock_analysis(self, symbol: str, current_price: float) -> Dict:
        """Fallback analysis when LLM is not available"""
        return {
            "symbol": symbol,
            "current_price": current_price,
            "analysis": f"Stock {symbol} is currently trading at ₹{current_price}. "
                       f"Please conduct your own research before investing.",
            "source": "fallback"
        }
    
    def get_market_sentiment(self) -> str:
        """Get overall market sentiment"""
        if not self.llm:
            return "Market sentiment: Neutral. Please check latest news for updates."
        
        prompt = """
        Provide a brief overview of the current Indian stock market (NSE) sentiment.
        Include Nifty 50 trends and key factors affecting the market.
        Keep it under 100 words.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error getting market sentiment: {e}")
            return "Unable to fetch market sentiment. Please check financial news."


class RiskAnalysisAgent:
    """Agent for risk profiling and assessment"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize risk analysis agent"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("⚠️ OpenAI API key not found. Agent will use fallback responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                temperature=0.5,
                model="gpt-3.5-turbo",
                api_key=self.api_key
            )
    
    def assess_risk_profile(
        self,
        age: int,
        income: float,
        expenses: float,
        dependents: int,
        risk_appetite: str
    ) -> Dict:
        """
        Assess user's risk profile
        
        Args:
            age: User's age
            income: Monthly income
            expenses: Monthly expenses
            dependents: Number of dependents
            risk_appetite: Self-assessed risk appetite
        
        Returns:
            Risk assessment dictionary
        """
        if not self.llm:
            return self._fallback_risk_assessment(age, income, expenses, risk_appetite)
        
        prompt = f"""
        Assess the investment risk profile for an Indian investor with:
        - Age: {age} years
        - Monthly Income: ₹{income}
        - Monthly Expenses: ₹{expenses}
        - Dependents: {dependents}
        - Self-assessed Risk Appetite: {risk_appetite}
        
        Provide:
        1. Recommended risk level (Low/Medium/High)
        2. Investment strategy
        3. Asset allocation suggestions
        4. Key considerations
        
        Keep response concise and actionable.
        """
        
        try:
            response = self.llm.invoke(prompt)
            
            # Determine risk level from response
            content_lower = response.content.lower()
            if "high risk" in content_lower or "aggressive" in content_lower:
                risk_level = "High"
            elif "low risk" in content_lower or "conservative" in content_lower:
                risk_level = "Low"
            else:
                risk_level = "Medium"
            
            return {
                "recommended_risk_level": risk_level,
                "assessment": response.content,
                "source": "ai_agent"
            }
        except Exception as e:
            print(f"Error in risk assessment: {e}")
            return self._fallback_risk_assessment(age, income, expenses, risk_appetite)
    
    def _fallback_risk_assessment(
        self,
        age: int,
        income: float,
        expenses: float,
        risk_appetite: str
    ) -> Dict:
        """Fallback risk assessment"""
        investable = income - expenses
        savings_rate = (investable / income * 100) if income > 0 else 0
        
        # Simple rule-based risk assessment
        if age < 30 and savings_rate > 30 and risk_appetite == "High":
            risk_level = "High"
            strategy = "Aggressive growth with equity focus"
        elif age > 50 or savings_rate < 20:
            risk_level = "Low"
            strategy = "Conservative with debt focus"
        else:
            risk_level = "Medium"
            strategy = "Balanced approach with diversification"
        
        return {
            "recommended_risk_level": risk_level,
            "assessment": f"Based on your profile, a {risk_level} risk approach with "
                         f"{strategy} is recommended. Investable amount: ₹{investable}",
            "source": "fallback"
        }


class InvestmentAdvisorAgent:
    """Agent for personalized investment recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize investment advisor agent"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("⚠️ OpenAI API key not found. Agent will use fallback responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo",
                api_key=self.api_key
            )
    
    def get_investment_recommendations(
        self,
        amount: float,
        risk_level: str,
        goal: str,
        timeline: str
    ) -> Dict:
        """
        Get personalized investment recommendations
        
        Args:
            amount: Investment amount
            risk_level: Risk level
            goal: Investment goal
            timeline: Investment timeline
        
        Returns:
            Recommendations dictionary
        """
        if not self.llm:
            return self._fallback_recommendations(amount, risk_level)
        
        prompt = f"""
        Provide investment recommendations for an Indian investor:
        - Amount: ₹{amount}
        - Risk Level: {risk_level}
        - Goal: {goal}
        - Timeline: {timeline}
        
        Suggest:
        1. Specific investment products (SIP, mutual funds, stocks, etc.)
        2. Allocation strategy
        3. Expected returns
        4. Action steps
        
        Focus on India-specific options (NSE stocks, Indian mutual funds, etc.).
        Keep recommendations practical and actionable.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "amount": amount,
                "risk_level": risk_level,
                "recommendations": response.content,
                "source": "ai_agent"
            }
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self._fallback_recommendations(amount, risk_level)
    
    def _fallback_recommendations(self, amount: float, risk_level: str) -> Dict:
        """Fallback recommendations"""
        recommendations = {
            "Low": f"Conservative Strategy:\n"
                  f"• SIP in large-cap funds: ₹{amount * 0.3:.0f} (30%)\n"
                  f"• Fixed Deposits: ₹{amount * 0.25:.0f} (25%)\n"
                  f"• Liquid funds: ₹{amount * 0.25:.0f} (25%)\n"
                  f"• Insurance: ₹{amount * 0.2:.0f} (20%)",
            
            "Medium": f"Balanced Strategy:\n"
                     f"• SIP in diversified equity: ₹{amount * 0.4:.0f} (40%)\n"
                     f"• Large-cap stocks: ₹{amount * 0.2:.0f} (20%)\n"
                     f"• Debt funds: ₹{amount * 0.2:.0f} (20%)\n"
                     f"• FD/Savings: ₹{amount * 0.15:.0f} (15%)\n"
                     f"• Insurance: ₹{amount * 0.05:.0f} (5%)",
            
            "High": f"Aggressive Strategy:\n"
                   f"• SIP in mid/small cap: ₹{amount * 0.35:.0f} (35%)\n"
                   f"• Direct equity (NSE): ₹{amount * 0.35:.0f} (35%)\n"
                   f"• Sectoral funds: ₹{amount * 0.15:.0f} (15%)\n"
                   f"• Debt/FD: ₹{amount * 0.1:.0f} (10%)\n"
                   f"• Insurance: ₹{amount * 0.05:.0f} (5%)"
        }
        
        return {
            "amount": amount,
            "risk_level": risk_level,
            "recommendations": recommendations.get(risk_level, recommendations["Medium"]),
            "source": "fallback"
        }


class LoanOptimizationAgent:
    """Agent for loan optimization strategies"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize loan optimization agent"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("⚠️ OpenAI API key not found. Agent will use fallback responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                temperature=0.5,
                model="gpt-3.5-turbo",
                api_key=self.api_key
            )
    
    def optimize_loan_strategy(
        self,
        loan_type: str,
        principal: float,
        interest_rate: float,
        emi: float,
        outstanding: float,
        surplus_income: float
    ) -> Dict:
        """
        Get loan optimization strategies
        
        Args:
            loan_type: Type of loan
            principal: Original principal
            interest_rate: Interest rate
            emi: Monthly EMI
            outstanding: Outstanding amount
            surplus_income: Available surplus income
        
        Returns:
            Optimization strategies
        """
        if not self.llm:
            return self._fallback_loan_strategy(
                loan_type, outstanding, emi, surplus_income
            )
        
        prompt = f"""
        Provide loan optimization strategies for an Indian borrower:
        - Loan Type: {loan_type}
        - Original Principal: ₹{principal}
        - Interest Rate: {interest_rate}%
        - Monthly EMI: ₹{emi}
        - Outstanding: ₹{outstanding}
        - Surplus Income: ₹{surplus_income}
        
        Suggest:
        1. Prepayment strategy
        2. EMI optimization
        3. Refinancing options
        4. Tax benefits (if applicable)
        
        Provide specific, actionable advice for Indian context.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return {
                "loan_type": loan_type,
                "outstanding": outstanding,
                "strategy": response.content,
                "source": "ai_agent"
            }
        except Exception as e:
            print(f"Error in loan optimization: {e}")
            return self._fallback_loan_strategy(
                loan_type, outstanding, emi, surplus_income
            )
    
    def _fallback_loan_strategy(
        self,
        loan_type: str,
        outstanding: float,
        emi: float,
        surplus: float
    ) -> Dict:
        """Fallback loan strategy"""
        strategies = []
        
        if surplus > emi * 0.5:
            prepay_amount = surplus * 0.6
            strategies.append(f"• Make monthly prepayments of ₹{prepay_amount:.0f}")
        
        if loan_type == "Home Loan":
            strategies.append("• Claim tax deductions under Section 80C and 24(b)")
        
        strategies.append("• Compare refinancing options if rate drops by 1%+")
        strategies.append("• Set up auto-debit to avoid late payment charges")
        
        return {
            "loan_type": loan_type,
            "outstanding": outstanding,
            "strategy": "\n".join(strategies),
            "source": "fallback"
        }


# Global agent instances
market_agent = MarketDataAgent()
risk_agent = RiskAnalysisAgent()
investment_agent = InvestmentAdvisorAgent()
loan_agent = LoanOptimizationAgent()
