"""
Test script for the LLM Assistant functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_assistant import LLMAssistant
from config import CROP_TEMP_RANGES

def main():
    """Test the LLM Assistant functionality."""
    print("Initializing LLM Assistant...")
    assistant = LLMAssistant()
    
    # Test basic question answering
    print("\n=== Testing Basic Question Answering ===")
    question = "Which crops grow well in 30°C and 60% humidity?"
    print(f"Question: {question}")
    response = assistant.ask(question)
    print(f"Response: {response}")
    
    # Test RAG if environmental logs exist
    logs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "environmental_logs.txt")
    if os.path.exists(logs_path):
        print("\n=== Testing Retrieval-Augmented Generation ===")
        print(f"Setting up RAG with documents from {logs_path}")
        rag_result = assistant.setup_rag(logs_path)
        print(f"RAG Setup Result: {rag_result}")
        
        if rag_result['status'] == 'success':
            question = "What caused the temperature drop on June 5?"
            print(f"Question: {question}")
            response = assistant.ask_with_context(question)
            print(f"Response: {response}")
    
    # Test crop recommendation
    print("\n=== Testing Crop Recommendation ===")
    temperature = 28
    soil_moisture = 70
    print(f"Conditions: {temperature}°C, {soil_moisture}% soil moisture")
    
    recommendations = assistant.recommend_crops(temperature, soil_moisture)
    print(f"Recommended Crops: {recommendations['recommended_crops']}")
    print(f"Explanation: {recommendations['explanation']}")
    
    print("\nLLM Assistant testing completed!")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    main() 