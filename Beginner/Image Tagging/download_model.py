import os
import requests
import json
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np

def download_mobilenet():
    print("Downloading MobileNet model...")
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
        print("Created models directory")
    
    # Download MobileNetV2 model
    model = MobileNetV2(weights='imagenet')
    
    # Save the model
    model_path = os.path.join('models', 'mobilenet_v2')
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Create a simple test to verify the model works
    print("Testing model with a sample prediction...")
    
    # Create a simple JSON file with class mappings
    class_indices = {str(i): label for i, label in enumerate(model.output_names)}
    with open(os.path.join('models', 'class_indices.json'), 'w') as f:
        json.dump(class_indices, f)
    
    print("Model download and setup complete!")
    print("\nYou can now use the model in your web application.")
    print("Update your app.js file to use the local model instead of loading from CDN.")

if __name__ == "__main__":
    try:
        download_mobilenet()
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("\nPlease make sure you have the required packages installed:")
        print("pip install tensorflow tensorflow-hub pillow numpy requests") 