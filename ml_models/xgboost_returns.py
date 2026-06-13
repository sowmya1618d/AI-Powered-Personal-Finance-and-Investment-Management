"""
XGBoost Model for Investment Return Prediction
Predicts expected returns based on multiple features
"""
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, List
import joblib
import os


class InvestmentReturnPredictor:
    """XGBoost model for predicting investment returns"""
    
    def __init__(self):
        """Initialize predictor"""
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'investment_amount',
            'duration_months',
            'risk_level',  # 0: Low, 1: Medium, 2: High
            'market_trend',  # -1: Bearish, 0: Neutral, 1: Bullish
            'asset_type',  # 0: Debt, 1: Hybrid, 2: Equity
            'historical_return',
            'volatility',
            'expense_ratio',
            'aum',  # Assets Under Management
            'fund_age_years'
        ]
    
    def build_model(self) -> xgb.XGBRegressor:
        """
        Build XGBoost model
        
        Returns:
            XGBoost regressor
        """
        model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective='reg:squarederror'
        )
        return model
    
    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for training/prediction
        
        Args:
            data: DataFrame with feature columns
        
        Returns:
            Feature array
        """
        # Ensure all required features are present
        for feature in self.feature_names:
            if feature not in data.columns:
                data[feature] = 0
        
        return data[self.feature_names].values
    
    def train(self, training_data: pd.DataFrame, target_column: str = 'actual_return'):
        """
        Train the XGBoost model
        
        Args:
            training_data: DataFrame with features and target
            target_column: Name of target column
        """
        X = self.prepare_features(training_data)
        y = training_data[target_column].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = self.build_model()
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=False
        )
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        print(f"✅ Model trained! MSE: {mse:.4f}, R²: {r2:.4f}")
    
    def predict_return(self, investment_features: Dict) -> float:
        """
        Predict investment return
        
        Args:
            investment_features: Dictionary with investment features
        
        Returns:
            Predicted annual return percentage
        """
        if not self.is_trained or self.model is None:
            # Use rule-based fallback
            return self._fallback_prediction(investment_features)
        
        # Prepare features
        feature_array = np.array([[
            investment_features.get('investment_amount', 10000),
            investment_features.get('duration_months', 12),
            investment_features.get('risk_level', 1),
            investment_features.get('market_trend', 0),
            investment_features.get('asset_type', 1),
            investment_features.get('historical_return', 10),
            investment_features.get('volatility', 15),
            investment_features.get('expense_ratio', 1.5),
            investment_features.get('aum', 1000),
            investment_features.get('fund_age_years', 5)
        ]])
        
        # Scale and predict
        scaled_features = self.scaler.transform(feature_array)
        prediction = self.model.predict(scaled_features)
        
        return round(float(prediction[0]), 2)
    
    def _fallback_prediction(self, features: Dict) -> float:
        """
        Rule-based fallback prediction when model is not trained
        
        Args:
            features: Investment features
        
        Returns:
            Estimated return percentage
        """
        risk_level = features.get('risk_level', 1)
        asset_type = features.get('asset_type', 1)
        
        # Base returns for Indian market
        base_returns = {
            'low_risk': 6.5,      # FD, Debt funds
            'medium_risk': 10.0,  # Balanced/Hybrid funds
            'high_risk': 14.0     # Equity funds, Stocks
        }
        
        risk_mapping = {0: 'low_risk', 1: 'medium_risk', 2: 'high_risk'}
        base_return = base_returns[risk_mapping.get(risk_level, 'medium_risk')]
        
        # Adjust for market trend
        market_trend = features.get('market_trend', 0)
        trend_adjustment = market_trend * 2  # +/- 2% based on trend
        
        predicted_return = base_return + trend_adjustment
        
        return round(predicted_return, 2)
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance scores
        
        Returns:
            DataFrame with feature importance
        """
        if not self.is_trained or self.model is None:
            return pd.DataFrame()
        
        importance = self.model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def save_model(self, path: str = "ml_models/saved_models/"):
        """Save trained model and scaler"""
        os.makedirs(path, exist_ok=True)
        
        if self.model:
            joblib.dump(self.model, f"{path}xgboost_returns.pkl")
            joblib.dump(self.scaler, f"{path}xgboost_scaler.pkl")
            print(f"✅ Model saved to {path}")
    
    def load_model(self, path: str = "ml_models/saved_models/"):
        """Load trained model and scaler"""
        try:
            self.model = joblib.load(f"{path}xgboost_returns.pkl")
            self.scaler = joblib.load(f"{path}xgboost_scaler.pkl")
            self.is_trained = True
            print(f"✅ Model loaded from {path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")


def predict_investment_return(
    investment_amount: float,
    duration_months: int,
    risk_level: str,
    asset_type: str = "Hybrid"
) -> Dict:
    """
    Convenience function to predict investment return
    
    Args:
        investment_amount: Investment amount in INR
        duration_months: Investment duration in months
        risk_level: "Low", "Medium", or "High"
        asset_type: "Debt", "Hybrid", or "Equity"
    
    Returns:
        Dictionary with prediction details
    """
    predictor = InvestmentReturnPredictor()
    
    # Map string values to numeric
    risk_map = {"Low": 0, "Medium": 1, "High": 2}
    asset_map = {"Debt": 0, "Hybrid": 1, "Equity": 2}
    
    features = {
        'investment_amount': investment_amount,
        'duration_months': duration_months,
        'risk_level': risk_map.get(risk_level, 1),
        'market_trend': 0,  # Neutral
        'asset_type': asset_map.get(asset_type, 1),
        'historical_return': 10.0,
        'volatility': 15.0,
        'expense_ratio': 1.5,
        'aum': 1000,
        'fund_age_years': 5
    }
    
    predicted_return = predictor.predict_return(features)
    
    # Calculate future value
    years = duration_months / 12
    future_value = investment_amount * ((1 + predicted_return/100) ** years)
    
    return {
        "investment_amount": investment_amount,
        "duration_months": duration_months,
        "risk_level": risk_level,
        "predicted_annual_return": predicted_return,
        "estimated_future_value": round(future_value, 2),
        "estimated_gains": round(future_value - investment_amount, 2)
    }
