"""
Run the Greenhouse Intelligence System application.
"""

import os
import subprocess
import sys

def main():
    """Run the Streamlit application."""
    try:
        # Check if streamlit is installed
        import streamlit
        print("Starting Greenhouse Intelligence System...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])
    except ImportError:
        print("Streamlit is not installed. Please install requirements first:")
        print("pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 