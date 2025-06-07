# Image Tagging with TensorFlow.js

A simple web application that uses TensorFlow.js and the MobileNet model to classify images into various categories.

## Features

- Dark-themed user interface
- Real-time image classification
- Uses MobileNet, a pre-trained model for image classification
- Displays classification results with confidence scores
- Responsive design for mobile and desktop
- Option to download and use the model locally

## Technologies Used

- HTML5
- CSS3
- JavaScript (ES6+)
- TensorFlow.js
- MobileNet pre-trained model
- Python (for model downloading and conversion)

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.6+ (for model downloading)
- Internet connection (for initial setup)

### Setting Up the Model

This project includes Python scripts to download and convert the MobileNet model for local use:

1. Install the required Python packages:
   ```bash
   python setup.py
   ```

2. Download the MobileNet model:
   ```bash
   python download_model.py
   ```

3. Convert the model to TensorFlow.js format:
   ```bash
   python convert_model.py
   ```

This will create a `models/tfjs_model` directory containing the model files.

### Running the Application

After setting up the model, you can run the application:

```bash
# Using Python 3
python -m http.server 

http://localhost:8000 #open in the browser
```

## How It Works

1. The Python scripts download the MobileNet model and convert it to TensorFlow.js format
2. The web application loads the model from the local directory
3. Users upload an image through the interface
4. The model processes the image and returns classification predictions
5. Results are displayed showing the top predicted classes and confidence scores

## Model Information

This application uses MobileNet V2, a pre-trained convolutional neural network that is optimized for mobile devices. The model can classify images into 1000 different categories including various animals, objects, and scenes.

## Project Structure

```
├── index.html              # Main HTML file
├── style.css               # CSS styles
├── app.js                  # JavaScript for the web application
├── setup.py                # Script to install Python dependencies
├── download_model.py       # Script to download the MobileNet model
├── convert_model.py        # Script to convert the model to TensorFlow.js format
└── models/                 # Directory for model files
    └── tfjs_model/         # TensorFlow.js model files
```

## Limitations

- Classification accuracy depends on the quality and clarity of the uploaded image
- The model works best with images that clearly show a single subject
- Some specialized or uncommon objects may not be recognized accurately

## Future Improvements

- Add support for image capture from webcam
- Implement custom model training for specific use cases
- Add batch processing for multiple images
- Improve UI with additional features like history of classifications 

## Developed by

codexcherry © 2025