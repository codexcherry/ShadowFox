"""
Utility functions for fetching and processing NASA Earth data.
"""

import requests
import datetime
import numpy as np
import pandas as pd
import xarray as xr
from typing import Tuple, Dict, List, Optional
import sys
import os

# Add the project root to the path so we can import the config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import NASA_API_KEY

class NASAEarthdata:
    """Class to handle NASA Earthdata API requests and data processing."""
    
    def __init__(self, api_key: str = NASA_API_KEY):
        """Initialize with NASA API key for open data access."""
        self.api_key = api_key
        
        # For NASA Earth Data API v1
        self.headers = {
            "Accept": "application/json"
        }
        
        # Store API key for URL parameters
        self.api_params = {
            "api_key": self.api_key
        }
        
    def get_lst_data(self, lat: float, lon: float, radius: float, 
                     days: int = 6) -> pd.DataFrame:
        """
        Get Land Surface Temperature data for a location using NASA POWER API.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Radius in km
            days: Number of days of historical data
            
        Returns:
            DataFrame with date and temperature data
        """
        # Calculate date range
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Format dates for API
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")
        
        # Use NASA POWER API which is open and doesn't require authentication
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        
        # Build parameters
        params = {
            "start": start_str,
            "end": end_str,
            "latitude": lat,
            "longitude": lon,
            "community": "AG",  # Agricultural community
            "parameters": "T2M,T2M_MAX,T2M_MIN",  # Temperature parameters
            "format": "JSON",
            **self.api_params  # Add API key if needed
        }
        
        try:
            # Make API request to NASA POWER
            print(f"Fetching NASA POWER temperature data at coordinates ({lat}, {lon})")
            response = requests.get(base_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            # Process the response
            data = response.json()
            
            if 'properties' not in data or 'parameter' not in data['properties']:
                print("No temperature data found in the response")
                return pd.DataFrame(columns=['date', 'temperature'])
            
            # Extract temperature data
            temp_data = data['properties']['parameter']
            
            # Create lists for date and temperature
            dates = []
            temperatures = []
            
            # Process each date in the response
            for date_str, values in temp_data.get('T2M', {}).items():
                if date_str != 'units':  # Skip the units entry
                    try:
                        # Parse the date
                        date = datetime.datetime.strptime(date_str, "%Y%m%d")
                        # Get temperature in Celsius (POWER data is already in Celsius)
                        temp = float(values)
                        
                        # Skip invalid temperature values (-999 is NASA's missing data indicator)
                        if temp == -999:
                            continue
                        
                        dates.append(date)
                        temperatures.append(temp)
                    except (ValueError, TypeError) as e:
                        print(f"Error processing date {date_str}: {e}")
            
            # Create DataFrame
            if dates and temperatures:
                df = pd.DataFrame({
                    'date': dates,
                    'temperature': temperatures
                })
                
                # Sort by date
                df = df.sort_values('date')
                
                return df
            else:
                print("No temperature data could be extracted")
                return pd.DataFrame(columns=['date', 'temperature'])
            
        except Exception as e:
            print(f"Error fetching NASA temperature data: {e}")
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=['date', 'temperature'])
    
    def get_soil_moisture(self, lat: float, lon: float, radius: float, 
                         days: int = 6) -> pd.DataFrame:
        """
        Get soil moisture data for a location using NASA POWER API.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Radius in km
            days: Number of days of historical data
            
        Returns:
            DataFrame with date and soil moisture data
        """
        # Calculate date range
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Format dates for API
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")
        
        # Use NASA POWER API which is open and doesn't require authentication
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        
        # Build parameters - use soil moisture parameters
        params = {
            "start": start_str,
            "end": end_str,
            "latitude": lat,
            "longitude": lon,
            "community": "AG",  # Agricultural community
            "parameters": "PRECTOTCORR,RH2M,GWETPROF,GWETROOT,GWETTOP",  # Soil moisture related parameters
            "format": "JSON",
            **self.api_params  # Add API key if needed
        }
        
        try:
            # Make API request to NASA POWER
            print(f"Fetching NASA POWER soil moisture data at coordinates ({lat}, {lon})")
            response = requests.get(base_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            # Process the response
            data = response.json()
            
            if 'properties' not in data or 'parameter' not in data['properties']:
                print("No soil moisture data found in the response")
                return pd.DataFrame(columns=['date', 'soil_moisture'])
            
            # Extract soil moisture data - use GWETROOT (Root zone soil moisture)
            # GWETROOT is the fraction of soil moisture in the root zone (0-1)
            moisture_data = data['properties']['parameter'].get('GWETROOT', {})
            
            if not moisture_data or moisture_data == {}:
                # Try GWETPROF (Soil moisture profile) if GWETROOT is not available
                moisture_data = data['properties']['parameter'].get('GWETPROF', {})
                
            if not moisture_data or moisture_data == {}:
                # Try GWETTOP (Top soil layer moisture) as last resort
                moisture_data = data['properties']['parameter'].get('GWETTOP', {})
            
            # Create lists for date and soil moisture
            dates = []
            moisture_values = []
            
            # Process each date in the response
            for date_str, value in moisture_data.items():
                if date_str != 'units':  # Skip the units entry
                    try:
                        # Parse the date
                        date = datetime.datetime.strptime(date_str, "%Y%m%d")
                        
                        # Skip invalid moisture values (-999 is NASA's missing data indicator)
                        if float(value) == -999:
                            continue
                        
                        # Convert fraction to percentage (0-100%)
                        moisture = float(value) * 100.0
                        
                        dates.append(date)
                        moisture_values.append(moisture)
                    except (ValueError, TypeError) as e:
                        print(f"Error processing date {date_str}: {e}")
            
            # Create DataFrame
            if dates and moisture_values:
                df = pd.DataFrame({
                    'date': dates,
                    'soil_moisture': moisture_values
                })
                
                # Sort by date
                df = df.sort_values('date')
                
                return df
            else:
                print("No soil moisture data could be extracted")
                return pd.DataFrame(columns=['date', 'soil_moisture'])
            
        except Exception as e:
            print(f"Error fetching NASA soil moisture data: {e}")
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=['date', 'soil_moisture'])
        
    def process_temperature_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process temperature data: convert units, handle missing values, etc.
        
        Args:
            df: DataFrame with temperature data
            
        Returns:
            Processed DataFrame
        """
        # Check if DataFrame is empty
        if df.empty:
            return df
            
        # Ensure date column is datetime type
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception as e:
                print(f"Error converting date column to datetime: {e}")
                # Return the DataFrame without the additional features if conversion fails
                return df
        
        # Convert from Kelvin to Celsius if needed
        if df['temperature'].mean() > 100:  # Simple check if in Kelvin
            df['temperature'] = df['temperature'] - 273.15
            
        # Handle missing values - using ffill() instead of fillna(method='ffill')
        df['temperature'] = df['temperature'].ffill()
        
        # Add additional features
        try:
            df['day_of_year'] = df['date'].dt.dayofyear
            df['month'] = df['date'].dt.month
        except Exception as e:
            print(f"Error adding date features: {e}")
            # If we can't add features, just return the DataFrame with temperature
        
        return df
        
    def merge_datasets(self, temp_df: pd.DataFrame, moisture_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge temperature and moisture datasets.
        
        Args:
            temp_df: Temperature DataFrame
            moisture_df: Soil moisture DataFrame
            
        Returns:
            Merged DataFrame
        """
        # Check if either DataFrame is empty
        if temp_df.empty and moisture_df.empty:
            return pd.DataFrame(columns=['date', 'temperature', 'soil_moisture'])
        elif temp_df.empty:
            return moisture_df
        elif moisture_df.empty:
            return temp_df
            
        # Ensure date columns are datetime type before merging
        try:
            if not pd.api.types.is_datetime64_any_dtype(temp_df['date']):
                temp_df['date'] = pd.to_datetime(temp_df['date'])
                
            if not pd.api.types.is_datetime64_any_dtype(moisture_df['date']):
                moisture_df['date'] = pd.to_datetime(moisture_df['date'])
        except Exception as e:
            print(f"Error converting date columns to datetime before merge: {e}")
            
        try:
            # Merge on date
            merged = pd.merge(temp_df, moisture_df, on='date', how='outer')
            
            # Sort by date
            merged = merged.sort_values('date')
            
            # Handle any missing values after merge - using ffill/bfill instead of fillna(method=...)
            merged = merged.ffill().bfill()
            
            return merged
        except Exception as e:
            print(f"Error merging datasets: {e}")
            # If merge fails, return the temperature DataFrame as fallback
            return temp_df 