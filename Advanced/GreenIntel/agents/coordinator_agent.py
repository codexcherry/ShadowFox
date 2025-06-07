"""
Coordinator Agent for managing the interaction between all agents.
"""

import pandas as pd
from typing import Dict, Any, List, Optional
import datetime
import sys
import os

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.environmental_agent import EnvironmentalAgent
from agents.prediction_agent import PredictionAgent
from agents.memory_agent import MemoryAgent
from utils.nasa_data import NASAEarthdata
from utils.llm_assistant import LLMAssistant
from config import CROP_TEMP_RANGES

class CoordinatorAgent:
    """
    Agent for coordinating the interaction between all other agents.
    """
    
    def __init__(self):
        """Initialize the coordinator agent and its sub-agents."""
        self.env_agent = EnvironmentalAgent()
        self.prediction_agent = PredictionAgent()
        self.memory_agent = MemoryAgent()
        self.nasa_data = NASAEarthdata()
        self.llm_assistant = LLMAssistant()
        
        self.current_data = None
        self.current_crop = None
        
        # Try to set up RAG with environmental logs if they exist
        logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "data", "environmental_logs.txt")
        if os.path.exists(logs_path):
            self.llm_assistant.setup_rag(logs_path)
        
    def fetch_data(self, lat: float, lon: float, radius: float, days: int = 6) -> Dict[str, Any]:
        """
        Fetch NASA data for the specified location.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Radius in km
            days: Number of days of historical data
            
        Returns:
            Status dictionary
        """
        try:
            # Fetch temperature data
            temp_df = self.nasa_data.get_lst_data(lat, lon, radius, days)
            
            # Fetch soil moisture data
            moisture_df = self.nasa_data.get_soil_moisture(lat, lon, radius, days)
            
            # Process temperature data
            temp_df = self.nasa_data.process_temperature_data(temp_df)
            
            # Merge datasets
            self.current_data = self.nasa_data.merge_datasets(temp_df, moisture_df)
            
            # Update actual temperatures in memory if we have a crop set
            if self.current_crop is not None:
                self._update_actual_temperatures()
            
            return {
                'status': 'success',
                'message': f'Successfully fetched data for location ({lat}, {lon})',
                'data_shape': self.current_data.shape
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error fetching data: {str(e)}'
            }
            
    def _update_actual_temperatures(self) -> None:
        """
        Update actual temperatures in memory based on newly fetched data.
        """
        if self.current_data is None:
            return
            
        # Get the last few days of data
        recent_data = self.current_data.copy()
        
        try:
            # Ensure date column is datetime type
            if not pd.api.types.is_datetime64_any_dtype(recent_data['date']):
                recent_data['date'] = pd.to_datetime(recent_data['date'])
            
            # Convert date to string format used in memory
            recent_data['date_str'] = recent_data['date'].dt.strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Error converting dates in _update_actual_temperatures: {e}")
            # Use a simple string conversion as fallback
            recent_data['date_str'] = recent_data['date'].astype(str)
        
        # Update actual temperatures in memory
        for _, row in recent_data.iterrows():
            try:
                self.memory_agent.update_actual_temperature(row['date_str'], float(row['temperature']))
            except Exception as e:
                print(f"Error updating temperature in memory: {e}")
            
    def set_crop(self, crop: str) -> Dict[str, Any]:
        """
        Set the current crop.
        
        Args:
            crop: Crop name
            
        Returns:
            Status dictionary
        """
        if crop not in CROP_TEMP_RANGES:
            return {
                'status': 'error',
                'message': f'Unknown crop: {crop}. Available crops: {", ".join(CROP_TEMP_RANGES.keys())}'
            }
            
        self.current_crop = crop
        return {
            'status': 'success',
            'message': f'Crop set to {crop}'
        }
        
    def analyze_conditions(self) -> Dict[str, Any]:
        """
        Analyze current environmental conditions.
        
        Returns:
            Analysis results
        """
        if self.current_data is None:
            return {
                'status': 'error',
                'message': 'No data available. Please fetch data first.'
            }
            
        # Analyze temperature
        temp_metrics = self.env_agent.analyze_temperature(self.current_data)
        
        # Assess crop suitability for all crops
        crop_suitability = self.env_agent.assess_crop_suitability(temp_metrics)
        
        # Get latest soil moisture if available
        soil_moisture = None
        if 'soil_moisture' in self.current_data.columns:
            soil_moisture = self.current_data['soil_moisture'].iloc[-1]
            
        return {
            'status': 'success',
            'temperature': temp_metrics,
            'crop_suitability': crop_suitability,
            'soil_moisture': soil_moisture
        }
        
    def train_prediction_model(self) -> Dict[str, Any]:
        """
        Train the prediction model with current data.
        
        Returns:
            Training results
        """
        if self.current_data is None:
            return {
                'status': 'error',
                'message': 'No data available. Please fetch data first.'
            }
            
        return self.prediction_agent.train(self.current_data)
        
    def get_recommendations(self) -> Dict[str, Any]:
        """
        Get recommendations for the current crop and conditions.
        
        Returns:
            Recommendations dictionary
        """
        if self.current_data is None or self.current_crop is None:
            return {
                'status': 'error',
                'message': 'Data or crop not set. Please fetch data and set crop first.'
            }
            
        # Analyze current conditions
        temp_metrics = self.env_agent.analyze_temperature(self.current_data)
        
        # Get soil moisture if available
        soil_moisture = None
        if 'soil_moisture' in self.current_data.columns and not self.current_data.empty:
            try:
                soil_moisture = self.current_data['soil_moisture'].iloc[-1]
            except IndexError:
                # Handle empty DataFrame or other indexing errors
                soil_moisture = None
            
        # Get recommendations
        recommendations = self.env_agent.get_recommendations(
            self.current_crop, temp_metrics, soil_moisture
        )
        
        # Add current temperature to recommendations
        recommendations['temperature'] = temp_metrics.get('mean', 25.0)
        
        # Add crop information
        min_temp, max_temp = CROP_TEMP_RANGES.get(self.current_crop, (20, 30))
        recommendations['ideal_range'] = f"{min_temp}°C – {max_temp}°C"
        
        # Try to predict next day temperature
        prediction_result = self.prediction_agent.predict_next_day(self.current_data)
        
        # Add LLM-enhanced explanation if available
        if soil_moisture is not None and 'predicted_temperature' in prediction_result:
            try:
                llm_explanation = self.llm_assistant.recommend_crops(
                    prediction_result['predicted_temperature'],
                    soil_moisture
                )
                
                # Add LLM explanation to recommendations
                recommendations['llm_explanation'] = llm_explanation.get('explanation', '')
                recommendations['llm_recommended_crops'] = llm_explanation.get('recommended_crops', [])
            except Exception as e:
                print(f"Error getting LLM recommendations: {e}")
        
        return {
            'status': 'success',
            'recommendations': recommendations,
            'prediction': prediction_result,
            'ideal_range': f"{min_temp}°C – {max_temp}°C",
            'crop': self.current_crop,
            'actuator_recommendations': recommendations  # Ensure actuator recommendations are directly accessible
        }
        
    def get_historical_performance(self) -> Dict[str, Any]:
        """
        Get historical performance data for the current crop.
        
        Returns:
            Historical performance data
        """
        if self.current_crop is None:
            return {
                'status': 'error',
                'message': 'Crop not set. Please set crop first.'
            }
            
        performance = self.memory_agent.get_performance_history(self.current_crop)
        
        return {
            'status': 'success',
            'performance': performance
        }
        
    def ask_assistant(self, question: str, use_context: bool = True) -> Dict[str, Any]:
        """
        Ask a question to the LLM assistant.
        
        Args:
            question: Question to ask
            use_context: Whether to use RAG for context-aware responses
            
        Returns:
            Assistant response
        """
        try:
            if use_context:
                response = self.llm_assistant.ask_with_context(question)
            else:
                response = self.llm_assistant.ask(question)
                
            return {
                'status': 'success',
                'response': response,
                'used_context': use_context
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error querying assistant: {str(e)}'
            }
            
    def get_crop_recommendations(self, temperature: float, moisture: float) -> Dict[str, Any]:
        """
        Get crop recommendations based on temperature and moisture.
        
        Args:
            temperature: Temperature in Celsius
            moisture: Soil moisture percentage
            
        Returns:
            Crop recommendations
        """
        try:
            recommendations = self.llm_assistant.recommend_crops(temperature, moisture)
            
            return {
                'status': 'success',
                'recommendations': recommendations
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error getting crop recommendations: {str(e)}'
            } 