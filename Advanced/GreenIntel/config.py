"""
Configuration settings for the Greenhouse Intelligence System.
"""

# NASA Earthdata API credentials
NASA_API_KEY = ""

# Hugging Face API token
HF_API_TOKEN = ""

# Default location (Bengaluru)
DEFAULT_LATITUDE = 12.97
DEFAULT_LONGITUDE = 77.59
DEFAULT_RADIUS = 10  # km

# Data settings
DATA_DAYS = 10  # Number of days of historical data to fetch

# Crop temperature ranges (°C)
CROP_TEMP_RANGES = {
    "Lettuce": (16, 20),
    "Tomato": (21, 27),
    "Bell Pepper": (18, 24),
    "Cucumber": (18, 25),
    "Spinach": (10, 20)
}

# NASA POWER API parameters
# We don't need specific dataset IDs for the POWER API
# as we specify parameters directly in the API call

# Model settings
MODEL_PARAMS = {
    "gru": {
        "units": 64,
        "dropout": 0.2,
        "recurrent_dropout": 0.2,
        "epochs": 50,
        "batch_size": 32,
        "validation_split": 0.2
    }
} 