import pandas as pd

# Load the dataset
print("Loading dataset...")
try:
    df = pd.read_csv('data/car.csv')
    print("Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    print(df.head())
except Exception as e:
    print(f"Error loading dataset: {e}") 