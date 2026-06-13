"""
LSTM/BiLSTM Model for Net Worth Forecasting
Predicts future net worth for 6-12 months based on historical data
"""
import numpy as np
import pandas as pd
from tensorflow import keras
from keras import layers, models
from sklearn.preprocessing import MinMaxScaler
from typing import List, Tuple
import joblib
import os


class NetWorthForecaster:
    """LSTM/BiLSTM model for net worth forecasting"""
    
    def __init__(self, lookback_period: int = 12, forecast_period: int = 6):
        """
        Initialize forecaster
        
        Args:
            lookback_period: Number of past months to consider
            forecast_period: Number of future months to predict
        """
        self.lookback_period = lookback_period
        self.forecast_period = forecast_period
        self.model = None
        self.scaler = MinMaxScaler()
        self.is_trained = False
    
    def build_model(self, input_shape: Tuple) -> models.Sequential:
        """
        Build BiLSTM model architecture
        
        Args:
            input_shape: Shape of input data (lookback_period, features)
        
        Returns:
            Compiled Keras model
        """
        model = models.Sequential([
            # First BiLSTM layer
            layers.Bidirectional(
                layers.LSTM(64, return_sequences=True, activation='tanh'),
                input_shape=input_shape
            ),
            layers.Dropout(0.2),
            
            # Second BiLSTM layer
            layers.Bidirectional(
                layers.LSTM(32, return_sequences=False, activation='tanh')
            ),
            layers.Dropout(0.2),
            
            # Dense layers
            layers.Dense(16, activation='relu'),
            layers.Dense(self.forecast_period)  # Output: forecast_period predictions
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences for training
        
        Args:
            data: Time series data (net worth history)
        
        Returns:
            X (input sequences) and y (target values)
        """
        X, y = [], []
        
        for i in range(len(data) - self.lookback_period - self.forecast_period + 1):
            X.append(data[i:(i + self.lookback_period)])
            y.append(data[(i + self.lookback_period):(i + self.lookback_period + self.forecast_period)])
        
        return np.array(X), np.array(y)
    
    def train(self, net_worth_history: pd.DataFrame, epochs: int = 100, batch_size: int = 32):
        """
        Train the LSTM model
        
        Args:
            net_worth_history: DataFrame with columns ['month', 'net_worth']
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        # Extract net worth values
        values = net_worth_history['net_worth'].values.reshape(-1, 1)
        
        # Scale data
        scaled_data = self.scaler.fit_transform(values)
        
        # Prepare sequences
        X, y = self.prepare_sequences(scaled_data.flatten())
        
        if len(X) == 0:
            print("⚠️ Insufficient data for training. Need at least", 
                  self.lookback_period + self.forecast_period, "months of data.")
            return
        
        # Reshape for LSTM [samples, timesteps, features]
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Build model
        self.model = self.build_model((self.lookback_period, 1))
        
        # Train model
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
        
        self.is_trained = True
        print(f"✅ Model trained! Final loss: {history.history['loss'][-1]:.4f}")
    
    def predict(self, recent_net_worth: List[float]) -> List[float]:
        """
        Predict future net worth
        
        Args:
            recent_net_worth: List of recent net worth values (last N months)
        
        Returns:
            Predicted net worth for next forecast_period months
        """
        if not self.is_trained or self.model is None:
            print("⚠️ Model not trained yet!")
            return []
        
        # Take last lookback_period values
        input_data = recent_net_worth[-self.lookback_period:]
        
        if len(input_data) < self.lookback_period:
            print(f"⚠️ Need at least {self.lookback_period} months of data for prediction")
            return []
        
        # Scale and reshape
        input_array = np.array(input_data).reshape(-1, 1)
        scaled_input = self.scaler.transform(input_array)
        scaled_input = scaled_input.reshape((1, self.lookback_period, 1))
        
        # Predict
        scaled_prediction = self.model.predict(scaled_input, verbose=0)
        
        # Inverse transform
        prediction = self.scaler.inverse_transform(scaled_prediction.reshape(-1, 1))
        
        return prediction.flatten().tolist()
    
    def save_model(self, path: str = "ml_models/saved_models/"):
        """Save trained model and scaler"""
        os.makedirs(path, exist_ok=True)
        
        if self.model:
            self.model.save(f"{path}lstm_net_worth.h5")
            joblib.dump(self.scaler, f"{path}lstm_scaler.pkl")
            print(f"✅ Model saved to {path}")
    
    def load_model(self, path: str = "ml_models/saved_models/"):
        """Load trained model and scaler"""
        try:
            self.model = keras.models.load_model(f"{path}lstm_net_worth.h5")
            self.scaler = joblib.load(f"{path}lstm_scaler.pkl")
            self.is_trained = True
            print(f"✅ Model loaded from {path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")


def forecast_net_worth(net_worth_history: pd.DataFrame, months: int = 6) -> Dict:
    """
    Convenience function to forecast net worth
    
    Args:
        net_worth_history: DataFrame with net worth history
        months: Number of months to forecast
    
    Returns:
        Dictionary with predictions
    """
    forecaster = NetWorthForecaster(lookback_period=12, forecast_period=months)
    
    # Check if we have enough data
    if len(net_worth_history) < 18:  # Need 12 for lookback + 6 for training
        print("⚠️ Using simple linear extrapolation due to insufficient data")
        
        # Simple linear regression as fallback
        recent_values = net_worth_history['net_worth'].tail(6).values
        trend = np.polyfit(range(len(recent_values)), recent_values, 1)
        
        predictions = []
        for i in range(1, months + 1):
            pred = trend[0] * (len(recent_values) + i) + trend[1]
            predictions.append(round(pred, 2))
        
        return {
            "method": "linear_extrapolation",
            "predictions": predictions
        }
    
    # Train and predict using LSTM
    forecaster.train(net_worth_history, epochs=50)
    recent_values = net_worth_history['net_worth'].tail(12).tolist()
    predictions = forecaster.predict(recent_values)
    
    return {
        "method": "lstm",
        "predictions": [round(p, 2) for p in predictions]
    }
