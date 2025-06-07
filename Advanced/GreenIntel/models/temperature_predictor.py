"""
GRU-based model for temperature prediction.
"""

import numpy as np
import pandas as pd
import os
from typing import Tuple, List, Dict, Any
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import GRU, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import sys
import os

# Add the project root to the path so we can import the config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_PARAMS

class TemperaturePredictor:
    """GRU-based model for predicting next-day temperature."""
    
    def __init__(self, params: Dict[str, Any] = None):
        """
        Initialize the temperature predictor.
        
        Args:
            params: Model hyperparameters
        """
        self.params = params or MODEL_PARAMS['gru']
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_model.keras")
        self.scaler_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler_data.npy")
        
        # Try to load pre-trained model if it exists
        self._try_load_model()
        
    def _try_load_model(self) -> None:
        """Try to load a pre-trained model if it exists."""
        try:
            if os.path.exists(self.model_path):
                print(f"Loading pre-trained model from {self.model_path}")
                self.model = load_model(self.model_path)
                
                # Load scaler data if available
                if os.path.exists(self.scaler_data_path):
                    scaler_data = np.load(self.scaler_data_path)
                    self.scaler.min_, self.scaler.scale_ = scaler_data[0], scaler_data[1]
                    self.scaler.data_min_, self.scaler.data_max_ = scaler_data[2], scaler_data[3]
                    print("Loaded scaler data")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
        
    def _create_sequences(self, data: np.ndarray, seq_length: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create input sequences and target values for time series prediction.
        
        Args:
            data: Input data array
            seq_length: Sequence length for input
            
        Returns:
            Tuple of (X, y) where X is the input sequences and y is the target values
        """
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple[int, int]) -> None:
        """
        Build the GRU model.
        
        Args:
            input_shape: Shape of input data (sequence_length, features)
        """
        model = Sequential()
        model.add(GRU(
            units=self.params['units'],
            dropout=self.params['dropout'],
            recurrent_dropout=self.params['recurrent_dropout'],
            return_sequences=True,
            input_shape=input_shape
        ))
        model.add(GRU(
            units=self.params['units'] // 2,
            dropout=self.params['dropout'],
            recurrent_dropout=self.params['recurrent_dropout']
        ))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mse')
        self.model = model
        
    def train(self, df: pd.DataFrame, sequence_length: int = 5) -> Dict[str, Any]:
        """
        Train the model on temperature data.
        
        Args:
            df: DataFrame with 'temperature' column
            sequence_length: Length of input sequences
            
        Returns:
            Training history
        """
        try:
            # If model already exists and has been trained, skip training
            if self.model is not None and os.path.exists(self.model_path):
                print("Using pre-trained model. Skipping training.")
                return {'loss': [0], 'val_loss': [0]}
                
            # Check if DataFrame is valid
            if df.empty:
                return {'loss': [0], 'val_loss': [0]}
                
            # Ensure temperature column exists and has numeric values
            if 'temperature' not in df.columns:
                raise ValueError("DataFrame must contain 'temperature' column")
                
            # Convert temperature to numeric if needed
            df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
            
            # Drop any NaN values
            df = df.dropna(subset=['temperature'])
            
            if len(df) < sequence_length + 1:
                raise ValueError(f"Not enough data points after cleaning. Need at least {sequence_length + 1}, got {len(df)}")
            
            # Scale the data
            data = self.scaler.fit_transform(df[['temperature']].values)
            
            # Save scaler data for future use
            scaler_data = np.array([
                self.scaler.min_,
                self.scaler.scale_,
                self.scaler.data_min_,
                self.scaler.data_max_
            ])
            np.save(self.scaler_data_path, scaler_data)
            
            # Create sequences
            X, y = self._create_sequences(data, sequence_length)
            
            # Build model if not already built
            if self.model is None:
                self.build_model((X.shape[1], X.shape[2]))
                
            # Train model
            history = self.model.fit(
                X, y,
                epochs=self.params['epochs'],
                batch_size=self.params['batch_size'],
                validation_split=self.params['validation_split'],
                verbose=1
            )
            
            # Save the trained model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            self.model.save(self.model_path)
            print(f"Model saved to {self.model_path}")
            
            return history.history
            
        except Exception as e:
            print(f"Error training temperature model: {e}")
            # Return dummy history to avoid breaking the app
            return {'loss': [0], 'val_loss': [0]}
        
    def predict_next_day(self, df: pd.DataFrame, sequence_length: int = 5) -> float:
        """
        Predict the next day's temperature.
        
        Args:
            df: DataFrame with recent temperature data
            sequence_length: Length of input sequences
            
        Returns:
            Predicted temperature for the next day
        """
        try:
            if self.model is None:
                raise ValueError("Model has not been trained yet")
                
            # Check if DataFrame is valid
            if df.empty:
                raise ValueError("DataFrame is empty")
                
            # Ensure temperature column exists and has numeric values
            if 'temperature' not in df.columns:
                raise ValueError("DataFrame must contain 'temperature' column")
                
            # Convert temperature to numeric if needed
            df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
            
            # Drop any NaN values
            df = df.dropna(subset=['temperature'])
            
            if len(df) < sequence_length:
                raise ValueError(f"Not enough data points after cleaning. Need at least {sequence_length}, got {len(df)}")
            
            # Scale the data
            data = self.scaler.transform(df[['temperature']].values[-sequence_length:])
            
            # Reshape for prediction
            X = np.array([data])
            
            # Make prediction
            prediction = self.model.predict(X, verbose=0)  # Set verbose=0 to avoid printing progress
            
            # Inverse transform to get actual temperature
            prediction_rescaled = self.scaler.inverse_transform(prediction)
            
            return float(prediction_rescaled[0, 0])
            
        except Exception as e:
            print(f"Error predicting temperature: {e}")
            # Return the mean temperature as fallback
            if not df.empty and 'temperature' in df.columns:
                return float(df['temperature'].mean())
            else:
                # Return a reasonable default if we can't get the mean
                return 25.0  # Default to 25°C
        
    def save_model(self, filepath: str = None) -> None:
        """
        Save the trained model.
        
        Args:
            filepath: Path to save the model (optional)
        """
        if self.model is None:
            raise ValueError("No model to save")
        
        if filepath is None:
            filepath = self.model_path
            
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        
    def load_model(self, filepath: str = None) -> None:
        """
        Load a trained model.
        
        Args:
            filepath: Path to load the model from (optional)
        """
        if filepath is None:
            filepath = self.model_path
            
        if not os.path.exists(filepath):
            raise ValueError(f"Model file not found: {filepath}")
            
        self.model = load_model(filepath) 