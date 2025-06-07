import subprocess
import sys

def install_requirements():
    print("Installing required packages...")
    
    requirements = [
        "tensorflow",
        "tensorflow-hub",
        "tensorflowjs",
        "pillow",
        "numpy",
        "requests"
    ]
    
    for package in requirements:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("\nAll required packages installed successfully!")
    print("Now you can run the model download and conversion scripts:")
    print("1. python download_model.py")
    print("2. python convert_model.py")

if __name__ == "__main__":
    try:
        install_requirements()
    except Exception as e:
        print(f"Error installing packages: {e}")
        print("Please try installing the packages manually:")
        print("pip install tensorflow tensorflow-hub tensorflowjs pillow numpy requests") 