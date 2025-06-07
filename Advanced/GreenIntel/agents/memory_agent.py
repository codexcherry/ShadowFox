"""
Memory Agent for maintaining history of predictions and decisions.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
import os
from datetime import datetime

class MemoryAgent:
    """
    Agent for maintaining history of predictions and decisions.
    """
    
    def __init__(self, memory_file: str = 'data/memory.json'):
        """
        Initialize the memory agent.
        
        Args:
            memory_file: Path to the memory storage file
        """
        self.memory_file = memory_file
        self.memory = self._load_memory()
        
    def _load_memory(self) -> Dict[str, Any]:
        """
        Load memory from file or initialize if not exists.
        
        Returns:
            Memory dictionary
        """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
                
        # Initialize empty memory
        return {
            'predictions': [],
            'recommendations': [],
            'crop_history': {},
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        }
        
    def _save_memory(self) -> None:
        """Save memory to file."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        # Update last_updated timestamp
        self.memory['metadata']['last_updated'] = datetime.now().isoformat()
        
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
            
    def store_prediction(self, date: str, crop: str, 
                        predicted_temp: float, actual_temp: float = None) -> None:
        """
        Store a temperature prediction.
        
        Args:
            date: Date of prediction
            crop: Crop being grown
            predicted_temp: Predicted temperature
            actual_temp: Actual temperature (if known)
        """
        # Check if we already have a prediction for this date
        existing_index = None
        for i, pred in enumerate(self.memory['predictions']):
            if pred['date'] == date:
                existing_index = i
                break
        
        if existing_index is not None:
            # Update existing prediction with actual temperature
            self.memory['predictions'][existing_index]['actual_temp'] = actual_temp
            self.memory['predictions'][existing_index]['updated_at'] = datetime.now().isoformat()
        else:
            # Create new prediction
            prediction = {
                'date': date,
                'crop': crop,
                'predicted_temp': predicted_temp,
                'actual_temp': actual_temp,
                'recorded_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.memory['predictions'].append(prediction)
        
        self._save_memory()
        
    def store_recommendation(self, date: str, crop: str, 
                           recommendations: Dict[str, Any]) -> None:
        """
        Store actuator recommendations.
        
        Args:
            date: Date of recommendation
            crop: Crop being grown
            recommendations: Dictionary of recommendations
        """
        recommendation = {
            'date': date,
            'crop': crop,
            'recommendations': recommendations,
            'recorded_at': datetime.now().isoformat()
        }
        
        self.memory['recommendations'].append(recommendation)
        self._save_memory()
        
    def update_crop_performance(self, crop: str, performance_score: float) -> None:
        """
        Update crop performance history.
        
        Args:
            crop: Crop name
            performance_score: Performance score (0-100)
        """
        if crop not in self.memory['crop_history']:
            self.memory['crop_history'][crop] = []
            
        entry = {
            'date': datetime.now().isoformat(),
            'score': performance_score
        }
        
        self.memory['crop_history'][crop].append(entry)
        self._save_memory()
        
    def get_prediction_accuracy(self) -> Dict[str, float]:
        """
        Calculate prediction accuracy metrics.
        
        Returns:
            Dictionary of accuracy metrics
        """
        predictions = [p for p in self.memory['predictions'] 
                     if p['actual_temp'] is not None]
                     
        if not predictions:
            return {'mae': None, 'rmse': None}
            
        errors = [abs(p['predicted_temp'] - p['actual_temp']) for p in predictions]
        mae = sum(errors) / len(errors)
        rmse = np.sqrt(sum(e**2 for e in errors) / len(errors))
        
        return {
            'mae': mae,
            'rmse': rmse
        }
        
    def get_crop_history(self, crop: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get crop performance history.
        
        Args:
            crop: Specific crop to get history for (None for all)
            
        Returns:
            Dictionary of crop history
        """
        if crop is not None:
            return {crop: self.memory['crop_history'].get(crop, [])}
        return self.memory['crop_history']
        
    def get_recent_predictions(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent predictions.
        
        Args:
            n: Number of predictions to return
            
        Returns:
            List of recent predictions
        """
        return self.memory['predictions'][-n:]
        
    def update_actual_temperature(self, date: str, actual_temp: float) -> bool:
        """
        Update a prediction with the actual temperature.
        
        Args:
            date: Date of prediction
            actual_temp: Actual temperature
            
        Returns:
            True if prediction was found and updated, False otherwise
        """
        for pred in self.memory['predictions']:
            if pred['date'] == date:
                pred['actual_temp'] = actual_temp
                pred['updated_at'] = datetime.now().isoformat()
                self._save_memory()
                return True
                
        return False
        
    def get_performance_history(self, crop: str) -> Dict[str, Any]:
        """
        Get historical performance data for a specific crop.
        
        Args:
            crop: Crop name
            
        Returns:
            Dictionary with performance metrics and history
        """
        # Get crop history
        crop_history = self.memory['crop_history'].get(crop, [])
        
        # Get predictions for this crop
        crop_predictions = [p for p in self.memory['predictions'] if p['crop'] == crop and p['actual_temp'] is not None]
        
        # Calculate prediction accuracy for this crop
        if crop_predictions:
            errors = [abs(p['predicted_temp'] - p['actual_temp']) for p in crop_predictions]
            mae = sum(errors) / len(errors)
            rmse = np.sqrt(sum(e**2 for e in errors) / len(errors))
        else:
            mae = None
            rmse = None
            
        # Get recent recommendations for this crop
        crop_recommendations = [r for r in self.memory['recommendations'] if r['crop'] == crop][-5:]
        
        return {
            'crop': crop,
            'history': crop_history,
            'prediction_accuracy': {
                'mae': mae,
                'rmse': rmse,
                'sample_size': len(crop_predictions)
            },
            'recent_recommendations': crop_recommendations
        } 