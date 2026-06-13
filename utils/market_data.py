"""
Real-time market data fetching utilities
Specialized for Indian stock market (NSE)
"""
import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from config.settings import settings


class MarketDataFetcher:
    """Fetch real-time market data from NSE using yfinance"""
    
    def __init__(self):
        self.stock_suffix = settings.STOCK_SUFFIX
    
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """
        Get current stock price for NSE symbol
        
        Args:
            symbol: Stock symbol (e.g., "RELIANCE", "TCS")
        
        Returns:
            Current stock price or None if not found
        """
        try:
            # Add .NS suffix for NSE stocks
            if not symbol.endswith(self.stock_suffix):
                symbol = f"{symbol}{self.stock_suffix}"
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            
            if not data.empty:
                return round(data['Close'].iloc[-1], 2)
            return None
            
        except Exception as e:
            print(f"Error fetching stock price for {symbol}: {e}")
            return None
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get detailed stock information
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Dictionary with stock info
        """
        try:
            if not symbol.endswith(self.stock_suffix):
                symbol = f"{symbol}{self.stock_suffix}"
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "symbol": symbol,
                "name": info.get("longName", "N/A"),
                "current_price": info.get("currentPrice", 0),
                "previous_close": info.get("previousClose", 0),
                "day_high": info.get("dayHigh", 0),
                "day_low": info.get("dayLow", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "market_cap": info.get("marketCap", 0),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A")
            }
            
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            return {}
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Get historical stock data
        
        Args:
            symbol: Stock symbol
            period: Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            DataFrame with historical data
        """
        try:
            if not symbol.endswith(self.stock_suffix):
                symbol = f"{symbol}{self.stock_suffix}"
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def search_stocks(self, query: str) -> List[Dict]:
        """
        Search for stocks by name or symbol
        
        Args:
            query: Search query
        
        Returns:
            List of matching stocks
        """
        # Popular NSE stocks for quick search
        popular_stocks = [
            {"symbol": "RELIANCE", "name": "Reliance Industries Ltd"},
            {"symbol": "TCS", "name": "Tata Consultancy Services Ltd"},
            {"symbol": "INFY", "name": "Infosys Ltd"},
            {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd"},
            {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd"},
            {"symbol": "SBIN", "name": "State Bank of India"},
            {"symbol": "BHARTIARTL", "name": "Bharti Airtel Ltd"},
            {"symbol": "ITC", "name": "ITC Ltd"},
            {"symbol": "HINDUNILVR", "name": "Hindustan Unilever Ltd"},
            {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank Ltd"},
            {"symbol": "LT", "name": "Larsen & Toubro Ltd"},
            {"symbol": "AXISBANK", "name": "Axis Bank Ltd"},
            {"symbol": "BAJFINANCE", "name": "Bajaj Finance Ltd"},
            {"symbol": "WIPRO", "name": "Wipro Ltd"},
            {"symbol": "MARUTI", "name": "Maruti Suzuki India Ltd"},
            {"symbol": "TATAMOTORS", "name": "Tata Motors Ltd"},
            {"symbol": "TITAN", "name": "Titan Company Ltd"},
            {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical Industries Ltd"},
            {"symbol": "ASIANPAINT", "name": "Asian Paints Ltd"},
            {"symbol": "NTPC", "name": "NTPC Ltd"}
        ]
        
        query = query.upper()
        results = [
            stock for stock in popular_stocks
            if query in stock["symbol"] or query in stock["name"].upper()
        ]
        
        return results
    
    def get_mutual_fund_nav(self, scheme_code: str) -> Optional[float]:
        """
        Get mutual fund NAV (Net Asset Value)
        Note: This is a placeholder. Real implementation would use AMFI API
        
        Args:
            scheme_code: Mutual fund scheme code
        
        Returns:
            Current NAV
        """
        # Placeholder - implement with real API
        return None
    
    def get_market_indices(self) -> Dict:
        """
        Get major Indian market indices (NIFTY, SENSEX)
        
        Returns:
            Dictionary with index values
        """
        try:
            # NIFTY 50
            nifty = yf.Ticker("^NSEI")
            nifty_data = nifty.history(period="1d")
            
            # SENSEX
            sensex = yf.Ticker("^BSESN")
            sensex_data = sensex.history(period="1d")
            
            return {
                "nifty_50": {
                    "value": round(nifty_data['Close'].iloc[-1], 2) if not nifty_data.empty else 0,
                    "change": round(nifty_data['Close'].iloc[-1] - nifty_data['Open'].iloc[-1], 2) if not nifty_data.empty else 0
                },
                "sensex": {
                    "value": round(sensex_data['Close'].iloc[-1], 2) if not sensex_data.empty else 0,
                    "change": round(sensex_data['Close'].iloc[-1] - sensex_data['Open'].iloc[-1], 2) if not sensex_data.empty else 0
                }
            }
            
        except Exception as e:
            print(f"Error fetching market indices: {e}")
            return {}


# Global instance
market_data_fetcher = MarketDataFetcher()
