import os
import requests
import zipfile
import io
import shutil

def download_mobilenet_tfjs():
    """Download MobileNet model in TensorFlow.js format"""
    
    print("Downloading MobileNet model in TensorFlow.js format...")
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
        print("Created models directory")
    
    # URL for the pre-converted MobileNet model
    model_url = "https://storage.googleapis.com/tfjs-models/savedmodel/mobilenet_v2_1.0_224/model.json"
    shard_url_template = "https://storage.googleapis.com/tfjs-models/savedmodel/mobilenet_v2_1.0_224/group{}-shard1of1"
    
    # Create model directory
    model_dir = os.path.join('models', 'mobilenet_tfjs')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Download model.json
    print("Downloading model.json...")
    response = requests.get(model_url)
    if response.status_code == 200:
        model_json_path = os.path.join(model_dir, 'model.json')
        with open(model_json_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved model.json to {model_json_path}")
    else:
        print(f"Failed to download model.json: {response.status_code}")
        return False
    
    # Alternative approach: download directly from CDN
    print("\nDownloading pre-packaged MobileNet model...")
    
    # URL for the MobileNet model from TensorFlow.js CDN
    cdn_url = "https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet@2.1.0/dist/mobilenet.min.js"
    
    # Download the model
    print(f"Downloading from {cdn_url}...")
    response = requests.get(cdn_url)
    if response.status_code == 200:
        model_path = os.path.join(model_dir, 'mobilenet.min.js')
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved model to {model_path}")
    else:
        print(f"Failed to download model: {response.status_code}")
        return False
    
    print("\nModel download complete!")
    print(f"Model files saved to {model_dir}")
    print("\nUpdate your index.html to include the local model:")
    print(f'<script src="./models/mobilenet_tfjs/mobilenet.min.js"></script>')
    
    return True

if __name__ == "__main__":
    try:
        download_mobilenet_tfjs()
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("\nPlease make sure you have the required packages installed:")
        print("pip install requests") 