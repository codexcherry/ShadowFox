"""
Environmental Analysis Agent for analyzing NASA data and assessing crop suitability.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import sys
import os

# Add the project root to the path so we can import the config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CROP_TEMP_RANGES

class EnvironmentalAgent:
    """
    Agent for analyzing environmental data and determining crop suitability.
    """
    
    def __init__(self):
        """Initialize the environmental agent."""
        self.crop_temp_ranges = CROP_TEMP_RANGES
        
    def analyze_temperature(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze temperature data and extract key metrics.
        
        Args:
            df: DataFrame with temperature data
            
        Returns:
            Dictionary of temperature metrics
        """
        if df.empty:
            return {
                'mean': None,
                'min': None,
                'max': None,
                'trend': None
            }
            
        # Calculate basic statistics
        mean_temp = df['temperature'].mean()
        min_temp = df['temperature'].min()
        max_temp = df['temperature'].max()
        
        # Calculate trend (simple linear regression)
        x = np.arange(len(df))
        y = df['temperature'].values
        
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
            trend = 'rising' if slope > 0.1 else 'falling' if slope < -0.1 else 'stable'
        else:
            trend = 'unknown'
        
        return {
            'mean': mean_temp,
            'min': min_temp,
            'max': max_temp,
            'trend': trend
        }
        
    def assess_crop_suitability(self, temp_metrics: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Assess the suitability of different crops based on temperature.
        
        Args:
            temp_metrics: Dictionary of temperature metrics
            
        Returns:
            Dictionary mapping crop names to suitability metrics
        """
        if temp_metrics['mean'] is None:
            return {}
            
        results = {}
        
        for crop, (min_temp, max_temp) in self.crop_temp_ranges.items():
            # Calculate how close the mean temperature is to the ideal range
            mean_temp = temp_metrics['mean']
            
            if min_temp <= mean_temp <= max_temp:
                status = 'Ideal'
                deviation = 0
            elif mean_temp < min_temp:
                status = 'Below Ideal'
                deviation = min_temp - mean_temp
            else:  # mean_temp > max_temp
                status = 'Above Ideal'
                deviation = mean_temp - max_temp
                
            # Calculate a suitability score (0-100)
            if status == 'Ideal':
                score = 100
            else:
                # Reduce score based on deviation from ideal range
                # Assume a 1°C deviation reduces score by 10 points
                score = max(0, 100 - 10 * abs(deviation))
                
            results[crop] = {
                'status': status,
                'deviation': deviation,
                'score': score,
                'ideal_range': f"{min_temp}°C – {max_temp}°C"
            }
            
        return results
        
    def get_recommendations(self, crop: str, temp_metrics: Dict[str, Any], 
                           soil_moisture: float = None) -> Dict[str, Any]:
        """
        Get actuator recommendations based on environmental conditions.
        
        Args:
            crop: Selected crop
            temp_metrics: Temperature metrics
            soil_moisture: Soil moisture percentage (optional)
            
        Returns:
            Dictionary of actuator recommendations
        """
        if crop not in self.crop_temp_ranges or temp_metrics['mean'] is None:
            return {
                'fan': 'OFF',
                'heater': 'OFF',
                'water_pump': 'OFF',
                'reasoning': 'Insufficient data'
            }
            
        min_temp, max_temp = self.crop_temp_ranges[crop]
        mean_temp = temp_metrics['mean']
        
        # Initialize recommendations
        fan = 'OFF'
        heater = 'OFF'
        water_pump = 'OFF'
        reasoning = []
        
        # Temperature-based recommendations
        if mean_temp > max_temp + 1:
            fan = 'ON'
            reasoning.append(f"Fan ON because temperature exceeds optimal range by {mean_temp - max_temp:.2f}°C")
        elif mean_temp < min_temp - 1:
            heater = 'ON'
            reasoning.append(f"Heater ON because temperature is below optimal range by {min_temp - mean_temp:.2f}°C")
            
        # Soil moisture-based recommendations (if available)
        if soil_moisture is not None:
            if soil_moisture < 30:  # Assuming 30% is the minimum threshold
                water_pump = 'ON'
                reasoning.append(f"Water pump ON because soil moisture ({soil_moisture:.1f}%) is below threshold")
                
        # Create the recommendations dictionary with all required fields
        recommendations = {
            'fan': fan,
            'heater': heater,
            'water_pump': water_pump,
            'reasoning': '. '.join(reasoning) if reasoning else 'All conditions within optimal range',
            'temperature': mean_temp,
            'soil_moisture': soil_moisture
        }
        
        return recommendations 