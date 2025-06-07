"""
Prediction Agent for forecasting environmental conditions.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import os
import sys

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.temperature_predictor import TemperaturePredictor

class PredictionAgent:
    """
    Agent for predicting future environmental conditions.
    """
    
    def __init__(self):
        """Initialize the prediction agent."""
        self.temperature_predictor = TemperaturePredictor()
        self.is_trained = False
        
    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train the prediction models with historical data.
        
        Args:
            df: DataFrame with environmental data
            
        Returns:
            Training metrics
        """
        # Check if we have enough data
        if len(df) < 10:  # Need at least 10 data points for meaningful training
            return {'status': 'error', 'message': 'Not enough data for training'}
            
        # Train temperature model
        history = self.temperature_predictor.train(df)
        self.is_trained = True
        
        return {
            'status': 'success',
            'temperature_loss': history['loss'][-1],
            'epochs': len(history['loss'])
        }
        
    def predict_next_day(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Predict environmental conditions for the next day.
        
        Args:
            df: DataFrame with recent environmental data
            
        Returns:
            Dictionary of predictions
        """
        if not self.is_trained:
            return {'status': 'error', 'message': 'Model not trained yet'}
            
        # Predict temperature
        try:
            predicted_temp = self.temperature_predictor.predict_next_day(df)
            
            return {
                'status': 'success',
                'predicted_temperature': predicted_temp
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def save_models(self, directory: str) -> None:
        """
        Save trained models to disk.
        
        Args:
            directory: Directory to save models
        """
        if not self.is_trained:
            raise ValueError("Models not trained yet")
            
        os.makedirs(directory, exist_ok=True)
        self.temperature_predictor.save_model(os.path.join(directory, 'temperature_model'))
        
    def load_models(self, directory: str) -> None:
        """
        Load trained models from disk.
        
        Args:
            directory: Directory containing saved models
        """
        self.temperature_predictor.load_model(os.path.join(directory, 'temperature_model'))
        self.is_trained = True 