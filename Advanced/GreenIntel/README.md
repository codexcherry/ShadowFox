# Greenhouse Intelligence System 🌿 

A smart greenhouse monitoring and recommendation system powered by NASA Earth data APIs and AI agents, featuring a premium dark-themed UI with interactive visualizations.

## Features

- 🌍 Geographic region selection via interactive OpenStreetMap
- 🛰️ NASA POWER API integration for real-time environmental monitoring
- 🌱 Crop suitability analysis with visual scoring
- 🧠 AI-powered temperature prediction with accuracy metrics
- 🤖 Multi-agent system for intelligent recommendations
- 📊 Interactive data visualizations with animations
- 📱 Responsive premium dark-themed UI
- 📈 Historical performance tracking and analysis
- 🌡️ Last recorded temperature display and trend analysis
- 💬 LLM-powered assistant for greenhouse management Q&A
- 📚 Retrieval-Augmented Generation (RAG) for context-aware responses
- 🌿 AI-enhanced crop recommendations with explanations

## Dashboard Features

- **Current Conditions**: Real-time temperature and soil moisture monitoring with animated gauges
- **Recommendations**: Smart actuator controls with visual indicators and reasoning
- **Temperature History**: Interactive temperature charts with ideal range visualization
- **Prediction Accuracy**: Visual error tracking and performance metrics
- **Crop Performance**: Historical performance tracking with trend analysis
- **AI Assistant**: LLM-powered Q&A system with context-aware responses
- **Crop Advisor**: AI-enhanced crop recommendations based on environmental conditions

## AI-Driven Natural Language Processing Project

### Language Model Selection
Our project begins with the careful selection of Google's FLAN-T5-Small model, chosen after evaluating multiple language models for agricultural applications. We selected this specialized instruction-tuned model for its exceptional ability to follow natural language instructions while maintaining efficient computational requirements. The model's architecture provides an optimal balance between performance and resource utilization, making it ideal for deployment in greenhouse management systems where real-time responses are critical.

### Implementation Workflow
The implementation process follows a systematic workflow in `utils/llm_assistant.py`:
1. First, we initialize the FLAN-T5-Small model with appropriate parameters for agricultural domain tasks
2. Next, we implement robust rule-based fallback mechanisms to ensure system reliability during API disruptions
3. Then, we integrate domain-specific knowledge about crops, growing conditions, and greenhouse management
4. Finally, we develop a RAG (Retrieval-Augmented Generation) system that enhances responses with contextual environmental data

### Exploration and Analysis Process
Our exploration process in `test_llm_assistant.py` follows a structured methodology:
1. We begin by testing basic question-answering capabilities with simple greenhouse management queries
2. Then we evaluate the model's context-awareness by implementing and testing the RAG system with environmental logs
3. Next, we assess the crop recommendation system using various temperature and moisture parameters
4. Finally, we analyze performance across different input scenarios to identify strengths and limitations

### Research Questions and Methodology
Our research methodology addresses five key questions through systematic experimentation:
1. We evaluate the model's agricultural domain expertise by comparing responses to expert knowledge
2. We measure improvements in contextual understanding by comparing standard responses to RAG-enhanced outputs
3. We analyze the trade-offs between rule-based fallbacks and full LLM implementation through reliability testing
4. We assess real-time performance by integrating environmental data streams and measuring response quality
5. We examine ethical considerations through a framework analyzing bias, transparency, and decision impact

### Visualization and Analysis Techniques
Our visualization workflow processes data through multiple stages:
1. First, raw model outputs are captured and structured for analysis
2. Next, we generate interactive temperature charts that overlay ideal crop ranges with predictions
3. Then, we implement error tracking visualizations that highlight discrepancies between predictions and actual values
4. Finally, we create crop suitability scoring visualizations that communicate complex recommendations intuitively

### Project Alignment with NLP/ML Goals
Our development process aligns with broader NLP and ML advancement goals through:
1. First, applying cutting-edge LLM techniques to solve practical agricultural challenges
2. Then, implementing and evaluating RAG methodologies to enhance contextual understanding
3. Next, optimizing the balance between computational efficiency and response quality
4. Throughout development, addressing ethical considerations in AI-driven agricultural recommendations
5. Finally, ensuring transparency by providing clear explanations for all AI-generated advice

### Conclusion and Future Directions
Our analysis concludes that the FLAN-T5-Small model effectively serves agricultural applications when:
1. Implemented with robust fallback mechanisms that maintain system reliability
2. Enhanced with domain-specific knowledge that improves recommendation quality
3. Augmented with RAG capabilities that provide contextual awareness
4. Deployed with clear understanding of its limitations in complex environmental scenarios

The project establishes a foundation for future improvements including:
1. Fine-tuning the model on specialized agricultural datasets to enhance domain expertise
2. Expanding the RAG knowledge base with comprehensive environmental and crop data
3. Developing more sophisticated recommendation algorithms that incorporate additional parameters
4. Exploring larger model architectures that may offer improved reasoning capabilities for complex scenarios


## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up API access:
   ```
   NASA_API_KEY=your_api_key
   HG_FACE_API = your_api_key
   ```

4. Run the application:
   ```
   python run.py
   ```
   or
   ```
   streamlit run app/main.py
   ```

## Project Structure

- `app/`: Streamlit application files
- `data/`: Data storage and processing modules
- `models/`: ML models for prediction
- `agents/`: AI agent system components
- `utils/`: Helper functions and utilities

## Supported Crops

- 🥬 Lettuce (Ideal: 16–20°C)
- 🍅 Tomato (Ideal: 21–27°C)
- 🫑 Bell Pepper (Ideal: 18–24°C)
- 🥒 Cucumber (Ideal: 18–25°C)
- 🌱 Spinach (Ideal: 10–20°C)

## Developed by

codexcherry © 2025