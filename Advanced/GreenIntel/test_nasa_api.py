"""
Simple test script for NASA POWER API without TensorFlow dependencies.
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_RADIUS

def fetch_nasa_power_data(lat, lon, days=6):
    """Fetch temperature data from NASA POWER API."""
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
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
        "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,GWETROOT",  # Temperature and soil moisture parameters
        "format": "JSON"
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        # Make API request to NASA POWER
        print(f"Fetching NASA POWER data at coordinates ({lat}, {lon})")
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        # Process the response
        data = response.json()
        
        if 'properties' not in data or 'parameter' not in data['properties']:
            print("No data found in the response")
            return None
        
        # Extract data
        parameters = data['properties']['parameter']
        
        # Create DataFrame
        dates = []
        temps = []
        soil_moisture = []
        
        # Get temperature data (T2M)
        temp_data = parameters.get('T2M', {})
        moisture_data = parameters.get('GWETROOT', {})
        
        for date_str in temp_data:
            if date_str != 'units':
                try:
                    date = datetime.strptime(date_str, "%Y%m%d")
                    temp = float(temp_data[date_str])
                    
                    # Skip invalid temperature values (-999 is NASA's missing data indicator)
                    if temp == -999:
                        continue
                    
                    # Get soil moisture if available
                    moisture = None
                    if date_str in moisture_data and moisture_data[date_str] != -999:
                        moisture = float(moisture_data[date_str]) * 100  # Convert to percentage
                    
                    dates.append(date)
                    temps.append(temp)
                    soil_moisture.append(moisture)
                except Exception as e:
                    print(f"Error processing date {date_str}: {e}")
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'temperature': temps,
            'soil_moisture': soil_moisture
        })
        
        return df
    
    except Exception as e:
        print(f"Error fetching NASA POWER data: {e}")
        return None

def main():
    """Main function to test NASA API."""
    # Fetch data for default location
    df = fetch_nasa_power_data(DEFAULT_LATITUDE, DEFAULT_LONGITUDE)
    
    if df is not None and not df.empty:
        print("\nData fetched successfully!")
        print(f"Shape: {df.shape}")
        print("\nFirst few rows:")
        print(df.head())
        
        # Plot the data
        plt.figure(figsize=(12, 6))
        
        # Temperature plot
        plt.subplot(1, 2, 1)
        plt.plot(df['date'], df['temperature'], 'o-', color='green')
        plt.title('Temperature Data')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Soil moisture plot
        plt.subplot(1, 2, 2)
        plt.plot(df['date'], df['soil_moisture'], 'o-', color='blue')
        plt.title('Soil Moisture Data')
        plt.xlabel('Date')
        plt.ylabel('Soil Moisture (%)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig('nasa_power_data.png')
        print("\nPlot saved as 'nasa_power_data.png'")
    else:
        print("Failed to fetch data from NASA POWER API")

if __name__ == "__main__":
    main() 