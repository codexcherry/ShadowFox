# Car Price Prediction System

A comprehensive machine learning-based web application that predicts the resale value of used cars based on various features like age, mileage, fuel type, and more.

## Project Overview

This project implements a complete end-to-end machine learning solution for predicting car prices. It includes:

1. **Data preprocessing and exploratory data analysis** - Cleaning, transforming, and visualizing car data
2. **Feature engineering** - Creating relevant features like car age and applying transformations
3. **Machine learning model training and evaluation** - Training and comparing multiple regression models
4. **Web application with Flask backend** - Interactive user interface for making predictions
5. **Responsive UI with dark mode** - Modern, user-friendly interface with intuitive design

## Dataset

The dataset (`data/car.csv`) contains detailed information about used cars, including:

- Car name/model
- Year of manufacture 
- Selling price (target variable)
- Present price (showroom price)
- Kilometers driven
- Fuel type (Petrol, Diesel, CNG)
- Seller type (Dealer, Individual)
- Transmission type (Manual, Automatic)
- Owner history (First, Second, Third, or more)

## Features

- **Comprehensive Data Visualization**: 
  - Correlation matrix heatmap
  - Selling price distribution analysis
  - Car age vs. price relationship
  - Kilometers driven vs. price relationship
  - Fuel type and transmission impact on price

- **Multiple ML Models**: 
  - Random Forest Regression
  - Linear Regression
  - XGBoost Regression
  - Automatic selection of best-performing model

- **Robust Model Evaluation**: 
  - Mean Absolute Error (MAE)
  - Mean Squared Error (MSE)
  - Root Mean Squared Error (RMSE)
  - R² score for goodness of fit

- **User-friendly Interface**: 
  - Clean, responsive web interface
  - Dark mode design
  - Form validation
  - Interactive elements with Font Awesome icons

- **Advanced Prediction Insights**: 
  - Estimated resale value
  - Depreciation percentage calculation
  - Confidence range for predictions
  - Market value comparison (above/below/fair)

## Project Structure

```
car_price_prediction/
├── data/
│   └── car.csv                  # Dataset with car information
├── model/
│   ├── car_price_model.pkl      # Trained machine learning model
│   └── model_info.pkl           # Model metadata and configuration
├── static/
│   ├── style.css                # CSS styling for web interface
│   ├── correlation_matrix.png   # Correlation heatmap visualization
│   ├── selling_price_distribution.png  # Price distribution chart
│   ├── age_vs_price.png         # Car age vs price visualization
│   ├── kms_vs_price.png         # Kilometers vs price visualization
│   ├── fuel_vs_price.png        # Fuel type vs price boxplot
│   └── transmission_vs_price.png # Transmission vs price boxplot
├── templates/
│   └── index.html               # Main web interface template
├── app.py                       # Flask application for web interface
├── model_training.py            # Script for training ML models
├── debug.py                     # Debugging utilities
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Installation and Setup

1. Clone the repository:

2. Create and activate a virtual environment (recommended):
   ```
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   
   # For macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Train the model (or use pre-trained model):
   ```
   python model_training.py
   ```
   This will:
   - Load and preprocess the dataset
   - Generate visualization plots in the static folder
   - Train multiple regression models
   - Select the best model based on R² score
   - Save the model and its metadata

5. Run the Flask application:
   ```
   python app.py
   ```

## Usage

1. Fill in the form with details about the car:
   - Manufacturing year (2000-2025)
   - Showroom price (in lakhs ₹)
   - Kilometers driven
   - Fuel type (Petrol, Diesel, CNG)
   - Seller type (Dealer, Individual)
   - Transmission type (Manual, Automatic)
   - Previous owners (0, 1, 2, 3+)

2. Click "Estimate Selling Price"

3. View the comprehensive prediction results:
   - Estimated resale value in lakhs (₹)
   - Depreciation percentage from original price
   - Confidence range showing upper and lower bounds
   - Market comparison indicating if the price is above, below, or fair market value

## Technical Implementation Details

### Data Preprocessing
- Handling missing values and outliers
- Feature engineering (car age calculation)
- Log transformation for skewed features
- One-hot encoding for categorical variables

### Model Training
- Pipeline approach with preprocessing steps
- Cross-validation for robust evaluation
- Hyperparameter tuning for optimal performance
- Model comparison and selection based on R² score

### Web Application
- Flask backend with RESTful API support
- Form validation and error handling
- Responsive design with modern CSS
- Interactive UI elements with Font Awesome icons

## Technologies Used

- **Python 3.x**: Core programming language
- **Data Processing**: 
  - Pandas for data manipulation
  - NumPy for numerical operations
- **Machine Learning**: 
  - Scikit-learn for traditional ML models
  - XGBoost for gradient boosting
  - Joblib for model serialization
- **Data Visualization**: 
  - Matplotlib for basic plotting
  - Seaborn for statistical visualizations
- **Web Development**: 
  - Flask for backend server
  - HTML5 for structure
  - CSS3 for styling
  - Font Awesome for icons

## Future Improvements

- **Advanced Models**: 
  - Implement Neural Networks for potentially better accuracy
  - Add ensemble methods combining multiple models
- **Feature Engineering**: 
  - Extract more features from car names/models
  - Implement feature importance visualization using SHAP values
- **User Experience**: 
  - Add user authentication and history tracking
  - Implement car image upload and recognition
  - Create a mobile app version
- **Deployment**: 
  - Deploy the application to a cloud platform (AWS, Azure, or GCP)
  - Set up CI/CD pipeline for automated testing and deployment
- **Additional Features**:
  - Integrate with external APIs for real-time market data
  - Add geographical price variation analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Developed by

codexcherry © 2025
