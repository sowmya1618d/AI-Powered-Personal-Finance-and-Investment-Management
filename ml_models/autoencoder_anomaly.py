"""
Autoencoder Model for Expense Anomaly Detection
Detects unusual spending patterns
"""
import numpy as np
import pandas as pd
from tensorflow import keras
from keras import layers, models
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Tuple
import joblib
import os


class ExpenseAnomalyDetector:
    """Autoencoder for detecting anomalous expenses"""
    
    def __init__(self, encoding_dim: int = 4):
        """
        Initialize anomaly detector
        
        Args:
            encoding_dim: Dimension of encoded representation
        """
        self.encoding_dim = encoding_dim
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.threshold = 0.8  # Anomaly threshold (reconstruction error)
        
        # Expense categories
        self.categories = [
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
    
    def build_autoencoder(self, input_dim: int) -> Tuple[models.Model, models.Model]:
        """
        Build autoencoder model
        
        Args:
            input_dim: Number of input features
        
        Returns:
            Tuple of (autoencoder, encoder)
        """
        # Encoder
        input_layer = layers.Input(shape=(input_dim,))
        encoded = layers.Dense(8, activation='relu')(input_layer)
        encoded = layers.Dense(self.encoding_dim, activation='relu')(encoded)
        
        # Decoder
        decoded = layers.Dense(8, activation='relu')(encoded)
        decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)
        
        # Autoencoder model
        autoencoder = models.Model(input_layer, decoded)
        autoencoder.compile(optimizer='adam', loss='mse')
        
        # Encoder model (for embedding)
        encoder = models.Model(input_layer, encoded)
        
        return autoencoder, encoder
    
    def prepare_features(self, expenses_df: pd.DataFrame) -> np.ndarray:
        """
        Prepare expense features for training/detection
        
        Args:
            expenses_df: DataFrame with expense data
        
        Returns:
            Feature array
        """
        # Group by month and category, sum amounts
        monthly_expenses = expenses_df.pivot_table(
            index='month',
            columns='category',
            values='amount',
            aggfunc='sum',
            fill_value=0
        )
        
        # Ensure all categories are present
        for category in self.categories:
            if category not in monthly_expenses.columns:
                monthly_expenses[category] = 0
        
        # Reorder columns
        monthly_expenses = monthly_expenses[self.categories]
        
        return monthly_expenses.values
    
    def train(self, expenses_df: pd.DataFrame, epochs: int = 100, batch_size: int = 32):
        """
        Train the autoencoder
        
        Args:
            expenses_df: DataFrame with expense history
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        # Prepare features
        X = self.prepare_features(expenses_df)
        
        if len(X) < 5:
            print("⚠️ Insufficient data for training. Need at least 5 months of expense data.")
            return
        
        # Scale data
        X_scaled = self.scaler.fit_transform(X)
        
        # Build model
        self.model, self.encoder = self.build_autoencoder(len(self.categories))
        
        # Train
        history = self.model.fit(
            X_scaled, X_scaled,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            shuffle=True,
            verbose=0
        )
        
        # Calculate threshold (mean + 2*std of reconstruction errors on training data)
        reconstructions = self.model.predict(X_scaled, verbose=0)
        reconstruction_errors = np.mean(np.square(X_scaled - reconstructions), axis=1)
        self.threshold = np.mean(reconstruction_errors) + 2 * np.std(reconstruction_errors)
        
        self.is_trained = True
        print(f"✅ Autoencoder trained! Anomaly threshold: {self.threshold:.4f}")
    
    def detect_anomalies(self, expenses_df: pd.DataFrame) -> List[Dict]:
        """
        Detect anomalous expenses
        
        Args:
            expenses_df: DataFrame with expense data
        
        Returns:
            List of anomalous expense records
        """
        if not self.is_trained or self.model is None:
            return self._rule_based_detection(expenses_df)
        
        # Prepare features
        X = self.prepare_features(expenses_df)
        X_scaled = self.scaler.transform(X)
        
        # Get reconstructions
        reconstructions = self.model.predict(X_scaled, verbose=0)
        
        # Calculate reconstruction errors
        errors = np.mean(np.square(X_scaled - reconstructions), axis=1)
        
        # Identify anomalies
        anomalies = []
        months = expenses_df['month'].unique()
        
        for i, (month, error) in enumerate(zip(months, errors)):
            if error > self.threshold:
                month_data = expenses_df[expenses_df['month'] == month]
                anomalies.append({
                    'month': month,
                    'reconstruction_error': float(error),
                    'total_expense': float(month_data['amount'].sum()),
                    'categories': month_data.groupby('category')['amount'].sum().to_dict()
                })
        
        return anomalies
    
    def _rule_based_detection(self, expenses_df: pd.DataFrame) -> List[Dict]:
        """
        Rule-based anomaly detection (fallback)
        Detects expenses that are significantly higher than average
        
        Args:
            expenses_df: DataFrame with expense data
        
        Returns:
            List of anomalous expense records
        """
        anomalies = []
        
        # Group by month
        monthly_totals = expenses_df.groupby('month')['amount'].sum()
        
        if len(monthly_totals) < 3:
            return anomalies
        
        # Calculate mean and std
        mean_expense = monthly_totals.mean()
        std_expense = monthly_totals.std()
        
        # Detect months with expenses > mean + 2*std
        threshold = mean_expense + 2 * std_expense
        
        for month, total in monthly_totals.items():
            if total > threshold:
                month_data = expenses_df[expenses_df['month'] == month]
                anomalies.append({
                    'month': month,
                    'total_expense': float(total),
                    'threshold': float(threshold),
                    'deviation': float((total - mean_expense) / std_expense),
                    'categories': month_data.groupby('category')['amount'].sum().to_dict()
                })
        
        return anomalies
    
    def check_expense(self, category_expenses: Dict[str, float]) -> Dict:
        """
        Check if a single month's expenses are anomalous
        
        Args:
            category_expenses: Dictionary of category: amount
        
        Returns:
            Anomaly detection result
        """
        if not self.is_trained or self.model is None:
            return {"is_anomaly": False, "error": 0, "message": "Model not trained"}
        
        # Prepare input
        expense_array = np.array([category_expenses.get(cat, 0) for cat in self.categories]).reshape(1, -1)
        
        # Scale
        scaled_input = self.scaler.transform(expense_array)
        
        # Get reconstruction
        reconstruction = self.model.predict(scaled_input, verbose=0)
        
        # Calculate error
        error = np.mean(np.square(scaled_input - reconstruction))
        
        is_anomaly = error > self.threshold
        
        return {
            "is_anomaly": bool(is_anomaly),
            "reconstruction_error": float(error),
            "threshold": float(self.threshold),
            "confidence": float(min(error / self.threshold, 2.0))
        }
    
    def save_model(self, path: str = "ml_models/saved_models/"):
        """Save trained model and scaler"""
        os.makedirs(path, exist_ok=True)
        
        if self.model:
            self.model.save(f"{path}autoencoder_anomaly.h5")
            self.encoder.save(f"{path}autoencoder_encoder.h5")
            joblib.dump(self.scaler, f"{path}autoencoder_scaler.pkl")
            joblib.dump(self.threshold, f"{path}autoencoder_threshold.pkl")
            print(f"✅ Model saved to {path}")
    
    def load_model(self, path: str = "ml_models/saved_models/"):
        """Load trained model and scaler"""
        try:
            self.model = keras.models.load_model(f"{path}autoencoder_anomaly.h5")
            self.encoder = keras.models.load_model(f"{path}autoencoder_encoder.h5")
            self.scaler = joblib.load(f"{path}autoencoder_scaler.pkl")
            self.threshold = joblib.load(f"{path}autoencoder_threshold.pkl")
            self.is_trained = True
            print(f"✅ Model loaded from {path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")


def detect_expense_anomalies(expenses_df: pd.DataFrame) -> Dict:
    """
    Convenience function to detect expense anomalies
    
    Args:
        expenses_df: DataFrame with expense data (columns: month, category, amount)
    
    Returns:
        Dictionary with anomaly detection results
    """
    detector = ExpenseAnomalyDetector()
    
    if len(expenses_df) < 10:
        print("⚠️ Using rule-based detection due to insufficient data")
        anomalies = detector._rule_based_detection(expenses_df)
        return {
            "method": "rule_based",
            "anomalies": anomalies,
            "total_anomalies": len(anomalies)
        }
    
    # Train and detect
    detector.train(expenses_df, epochs=50)
    anomalies = detector.detect_anomalies(expenses_df)
    
    return {
        "method": "autoencoder",
        "anomalies": anomalies,
        "total_anomalies": len(anomalies),
        "threshold": detector.threshold
    }
