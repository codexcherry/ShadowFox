import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
from datetime import datetime
import os
import traceback

try:
    # Create model directory if it doesn't exist
    if not os.path.exists('model'):
        os.makedirs('model')
    
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv('data/car.csv')
    
    # Display basic information
    print("\nDataset Information:")
    print(f"Shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
    
    # Check for missing values
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # Data Preprocessing
    print("\nPerforming data preprocessing...")
    
    # Calculate car age
    current_year = datetime.now().year
    df['Car_Age'] = current_year - df['Year']
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Exploratory Data Analysis
    print("\nPerforming Exploratory Data Analysis...")
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Save correlation matrix
    plt.figure(figsize=(12, 10))
    correlation = df.select_dtypes(include=[np.number]).corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig('static/correlation_matrix.png')
    print("Saved correlation matrix plot")
    
    # Selling Price Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Selling_Price'], kde=True)
    plt.title('Distribution of Selling Price')
    plt.xlabel('Selling Price (in lakhs)')
    plt.savefig('static/selling_price_distribution.png')
    print("Saved selling price distribution plot")
    
    # Relationship between Car Age and Selling Price
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Car_Age', y='Selling_Price', data=df)
    plt.title('Car Age vs Selling Price')
    plt.xlabel('Car Age (years)')
    plt.ylabel('Selling Price (in lakhs)')
    plt.savefig('static/age_vs_price.png')
    print("Saved age vs price plot")
    
    # Relationship between Kms Driven and Selling Price
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Kms_Driven', y='Selling_Price', data=df)
    plt.title('Kilometers Driven vs Selling Price')
    plt.xlabel('Kilometers Driven')
    plt.ylabel('Selling Price (in lakhs)')
    plt.savefig('static/kms_vs_price.png')
    print("Saved kilometers vs price plot")
    
    # Boxplot of Fuel Type vs Selling Price
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Fuel_Type', y='Selling_Price', data=df)
    plt.title('Fuel Type vs Selling Price')
    plt.xlabel('Fuel Type')
    plt.ylabel('Selling Price (in lakhs)')
    plt.savefig('static/fuel_vs_price.png')
    print("Saved fuel type vs price plot")
    
    # Boxplot of Transmission vs Selling Price
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Transmission', y='Selling_Price', data=df)
    plt.title('Transmission vs Selling Price')
    plt.xlabel('Transmission')
    plt.ylabel('Selling Price (in lakhs)')
    plt.savefig('static/transmission_vs_price.png')
    print("Saved transmission vs price plot")
    
    # Feature Engineering
    print("\nPerforming Feature Engineering...")
    
    # Log transformation for Kms_Driven if it's skewed
    if df['Kms_Driven'].skew() > 0.5:
        df['Kms_Driven_Log'] = np.log1p(df['Kms_Driven'])
        print("Applied log transformation to Kms_Driven")
    
    # Prepare data for model training
    # Define features and target
    X = df.drop(['Car_Name', 'Selling_Price', 'Year'], axis=1)
    y = df['Selling_Price']
    
    # Define categorical features
    categorical_features = ['Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']
    numerical_features = [col for col in X.columns if col not in categorical_features]
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
        ],
        remainder='passthrough'
    )
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\nTraining set shape:", X_train.shape)
    print("Testing set shape:", X_test.shape)
    
    # Model Training
    print("\nTraining models...")
    
    # 1. Random Forest
    print("\nTraining Random Forest model...")
    rf_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    rf_pipeline.fit(X_train, y_train)
    
    # 2. Linear Regression
    print("\nTraining Linear Regression model...")
    lr_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])
    
    lr_pipeline.fit(X_train, y_train)
    
    # 3. XGBoost
    print("\nTraining XGBoost model...")
    xgb_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', xgb.XGBRegressor(random_state=42))
    ])
    
    xgb_pipeline.fit(X_train, y_train)
    
    # Model Evaluation
    print("\nEvaluating models...")
    
    # Function to evaluate model
    def evaluate_model(model, X_test, y_test):
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        return {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2
        }
    
    # Evaluate Random Forest
    rf_metrics = evaluate_model(rf_pipeline, X_test, y_test)
    print("\nRandom Forest Metrics:")
    for metric, value in rf_metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Evaluate Linear Regression
    lr_metrics = evaluate_model(lr_pipeline, X_test, y_test)
    print("\nLinear Regression Metrics:")
    for metric, value in lr_metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Evaluate XGBoost
    xgb_metrics = evaluate_model(xgb_pipeline, X_test, y_test)
    print("\nXGBoost Metrics:")
    for metric, value in xgb_metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Select the best model based on R2 score
    models = {
        'Random Forest': (rf_pipeline, rf_metrics['R2']),
        'Linear Regression': (lr_pipeline, lr_metrics['R2']),
        'XGBoost': (xgb_pipeline, xgb_metrics['R2'])
    }
    
    best_model_name = max(models, key=lambda k: models[k][1])
    best_model = models[best_model_name][0]
    best_r2 = models[best_model_name][1]
    
    print(f"\nBest model: {best_model_name} with R2 score of {best_r2:.4f}")
    
    # Save the best model
    print(f"\nSaving {best_model_name} model...")
    joblib.dump(best_model, 'model/car_price_model.pkl')
    
    # Save feature names and categorical features for later use
    model_info = {
        'model_type': best_model_name,
        'categorical_features': categorical_features,
        'numerical_features': numerical_features,
        'metrics': models[best_model_name][1],
        'current_year': current_year
    }
    
    joblib.dump(model_info, 'model/model_info.pkl')
    
    print("\nModel training completed and saved successfully!")

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc() 