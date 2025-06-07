from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load the dataset for demonstration
df = pd.read_csv('data/car.csv')

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Simulate car price prediction based on user inputs"""
    try:
        # Get current year for calculating car age
        current_year = datetime.now().year
        
        # Get form data
        if request.content_type == 'application/json':
            data = request.json
            year = int(data.get('year', 0))
            present_price = float(data.get('present_price', 0))
            kms_driven = int(data.get('kms_driven', 0))
            fuel_type = data.get('fuel_type', '')
            seller_type = data.get('seller_type', '')
            transmission = data.get('transmission', '')
            owner = int(data.get('owner', 0))
        else:
            year = int(request.form.get('year', 0))
            present_price = float(request.form.get('present_price', 0))
            kms_driven = int(request.form.get('kms_driven', 0))
            fuel_type = request.form.get('fuel_type', '')
            seller_type = request.form.get('seller_type', '')
            transmission = request.form.get('transmission', '')
            owner = int(request.form.get('owner', 0))
        
        # Calculate car age
        car_age = current_year - year
        
        # Simple price prediction logic (for demonstration)
        # This is a simplified formula based on common depreciation patterns
        # In a real model, this would be replaced by the trained ML model's prediction
        
        # Base depreciation: cars lose ~15-20% value in first year, then ~10% per year
        base_depreciation = 0.85 if car_age <= 1 else (0.85 - (0.1 * (car_age - 1)))
        
        # Adjust for kilometers driven (higher km = lower value)
        km_factor = 1.0 - (kms_driven / 200000)
        
        # Adjust for fuel type (diesel typically holds value better)
        fuel_factor = 1.05 if fuel_type == 'Diesel' else (0.98 if fuel_type == 'CNG' else 1.0)
        
        # Adjust for transmission (automatic typically commands premium)
        transmission_factor = 1.05 if transmission == 'Automatic' else 1.0
        
        # Adjust for owner history (more owners = lower value)
        owner_factor = 1.0 - (owner * 0.05)
        
        # Calculate estimated price
        prediction = present_price * base_depreciation * km_factor * fuel_factor * transmission_factor * owner_factor
        
        # Ensure prediction is reasonable (not negative or too high)
        prediction = max(0.1, min(prediction, present_price * 0.95))
        
        # Calculate depreciation percentage
        depreciation = ((present_price - prediction) / present_price) * 100
        
        # Determine price range (±5%)
        lower_bound = prediction * 0.95
        upper_bound = prediction * 1.05
        
        # Determine market comparison
        if depreciation < 10:
            market_comparison = "ABOVE MARKET VALUE"
        elif depreciation > 30:
            market_comparison = "BELOW MARKET VALUE"
        else:
            market_comparison = "FAIR PRICE"
        
        # Return results
        result = {
            'estimated_price': round(prediction, 2),
            'depreciation': round(depreciation, 2),
            'confidence_lower': round(lower_bound, 2),
            'confidence_upper': round(upper_bound, 2),
            'market_comparison': market_comparison
        }
        
        if request.content_type == 'application/json':
            return jsonify(result)
        else:
            return render_template('index.html', prediction=result)
    
    except Exception as e:
        if request.content_type == 'application/json':
            return jsonify({'error': str(e)}), 400
        else:
            return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True) 