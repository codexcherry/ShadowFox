import os
import tensorflowjs as tfjs
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

def convert_model_to_tfjs():
    print("Converting MobileNet model to TensorFlow.js format...")
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
        print("Created models directory")
    
    # Create tfjs_model directory if it doesn't exist
    tfjs_target_dir = os.path.join('models', 'tfjs_model')
    if not os.path.exists(tfjs_target_dir):
        os.makedirs(tfjs_target_dir)
    
    # Check if we have a saved model already
    saved_model_path = os.path.join('models', 'mobilenet_v2')
    
    if os.path.exists(saved_model_path):
        print(f"Found existing model at {saved_model_path}")
        model = tf.keras.models.load_model(saved_model_path)
    else:
        print("No saved model found, downloading MobileNetV2...")
        # Download MobileNetV2 model
        model = MobileNetV2(weights='imagenet')
    
    # Convert the model to TensorFlow.js format
    tfjs.converters.save_keras_model(model, tfjs_target_dir)
    print(f"Model converted and saved to {tfjs_target_dir}")
    
    print("\nConversion complete!")
    print("You can now use the model in your web application by updating app.js to load from:")
    print(f"./models/tfjs_model/model.json")

if __name__ == "__main__":
    try:
        import tensorflow as tf
        import tensorflowjs as tfjs
        
        convert_model_to_tfjs()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease make sure you have the required packages installed:")
        print("pip install tensorflow tensorflowjs") 