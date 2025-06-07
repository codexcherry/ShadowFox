// DOM Elements
const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const predictBtn = document.getElementById('predictBtn');
const predictionsContainer = document.getElementById('predictions');
const loader = document.getElementById('loader');
const modelStatus = document.getElementById('modelStatus');
const downloadBtn = document.getElementById('downloadBtn');

// Global variables
let model;
let isModelLoaded = false;

// Initialize the app
async function init() {
    // Show loading message
    predictionsContainer.innerHTML = `
        <div class="prediction-item">
            Initializing application...
        </div>
    `;
    
    try {
        // Try to load the model
        await loadModel();
        
        // Add event listeners
        imageUpload.addEventListener('change', handleImageUpload);
        predictBtn.addEventListener('click', classifyImage);
        
        // Hide download button as we're using local model
        downloadBtn.style.display = 'none';
    } catch (error) {
        console.error('Error initializing app:', error);
        modelStatus.textContent = 'Error initializing. Please refresh the page.';
        modelStatus.style.color = 'var(--error-color)';
    }
}

// Load the MobileNet model
async function loadModel() {
    try {
        modelStatus.textContent = 'Loading model...';
        
        // Load the model from the local file
        model = await mobilenet.load();
        isModelLoaded = true;
        modelStatus.textContent = 'Model loaded successfully!';
        modelStatus.style.color = 'var(--success-color)';
        
        // Clear loading message
        predictionsContainer.innerHTML = `
            <div class="prediction-item">
                Upload an image and click "Classify Image" to see predictions.
            </div>
        `;
        
        console.log('MobileNet model loaded successfully');
    } catch (error) {
        console.error('Failed to load model:', error);
        modelStatus.textContent = 'Failed to load model. Check your internet connection.';
        modelStatus.style.color = 'var(--error-color)';
        predictionsContainer.innerHTML = `
            <div class="prediction-item" style="color: var(--error-color)">
                Error loading model. Please check your internet connection and try again.
            </div>
        `;
    }
}

// Handle image upload
function handleImageUpload(event) {
    const file = event.target.files[0];
    
    if (file && file.type.match('image.*')) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            predictBtn.disabled = false;
        };
        
        reader.readAsDataURL(file);
    }
}

// Classify the uploaded image
async function classifyImage() {
    if (!isModelLoaded) {
        predictionsContainer.innerHTML = `
            <div class="prediction-item" style="color: var(--error-color)">
                Model is not loaded yet. Please wait and try again.
            </div>
        `;
        return;
    }
    
    if (imagePreview.src === '#' || imagePreview.style.display === 'none') {
        predictionsContainer.innerHTML = `
            <div class="prediction-item" style="color: var(--error-color)">
                Please upload an image first.
            </div>
        `;
        return;
    }
    
    try {
        // Show loader
        loader.style.display = 'block';
        predictionsContainer.innerHTML = '';
        
        // Get predictions
        const predictions = await model.classify(imagePreview);
        
        // Hide loader
        loader.style.display = 'none';
        
        // Display results
        if (predictions && predictions.length > 0) {
            let resultsHTML = '';
            
            predictions.forEach(prediction => {
                const probability = (prediction.probability * 100).toFixed(2);
                resultsHTML += `
                    <div class="prediction-item">
                        <span class="prediction-label">${prediction.className}</span>
                        <span class="prediction-score">${probability}%</span>
                    </div>
                `;
            });
            
            predictionsContainer.innerHTML = resultsHTML;
        } else {
            predictionsContainer.innerHTML = `
                <div class="prediction-item">
                    No predictions found. Try another image.
                </div>
            `;
        }
    } catch (error) {
        // Hide loader
        loader.style.display = 'none';
        
        console.error('Error classifying image:', error);
        predictionsContainer.innerHTML = `
            <div class="prediction-item" style="color: var(--error-color)">
                Error classifying image. Please try again.
            </div>
        `;
    }
}

// Initialize the app when the page loads
window.addEventListener('DOMContentLoaded', init); 