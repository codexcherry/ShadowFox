"""
Main Streamlit application for the Greenhouse Intelligence System.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from datetime import datetime, timedelta

    # Set up the page - MUST be the first Streamlit command
st.set_page_config(
    page_title="Greenhouse Intelligence System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom theme with CSS
st.markdown("""
<style>
    /* Main background and text colors for dark theme */
    .stApp {
        background-color: #0a0a0a;
        color: #f0f0f0;
    }
    
    /* Header styling with animation */
    h1, h2, h3 {
        color: #4CAF50 !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
    }
    
    h1 {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        0% { text-shadow: 0 0 10px rgba(76, 175, 80, 0.3); }
        100% { text-shadow: 0 0 20px rgba(76, 175, 80, 0.7); }
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #121212;
        border-right: 1px solid #2E7D32;
    }
    
    /* Card/container styling with hover effect */
    div.stBlock {
        background-color: #121212;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2E7D32;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stBlock:hover {
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.3);
        transform: translateY(-2px);
    }
    
    /* Button styling with animation */
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #2E7D32, #1B5E20);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46, 125, 50, 0.4);
    }
    
    /* Metric styling with animation */
    div[data-testid="stMetric"] {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(46, 125, 50, 0.3);
    }
    
    div[data-testid="stMetric"] > div:first-child {
        color: #4CAF50 !important;
    }
    
    div[data-testid="stMetric"] > div:nth-child(2) {
        font-size: 1.8em !important;
        font-weight: 600 !important;
    }
    
    /* Map container styling */
    .map-container {
        border: 1px solid #2E7D32;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        width: 100% !important;
        transition: all 0.3s ease;
    }
    
    .map-container:hover {
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.4);
    }
    
    /* Fix map alignment */
    .stFolium [style*="position: relative"] {
        width: 100% !important;
    }
    
    .stFolium iframe {
        width: 100% !important;
        left: 0 !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        color: #999;
        font-size: 0.8em;
        border-top: 1px solid #2E7D32;
        margin-top: 30px;
        background-color: #0a0a0a;
    }
    
    /* Tab styling with animation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #2E7D32;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #121212;
        border-radius: 8px 8px 0 0;
        padding: 10px 16px;
        border: 1px solid #2E7D32;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1E1E1E;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #2E7D32, #1B5E20) !important;
        color: white !important;
        border: 1px solid #4CAF50 !important;
        border-bottom: none !important;
        box-shadow: 0 -4px 10px rgba(46, 125, 50, 0.3);
    }
    
    /* Fix expander styling */
    .streamlit-expanderHeader {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #1E1E1E;
    }
    
    .streamlit-expanderContent {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-top: none;
        border-radius: 0 0 5px 5px;
    }
    
    /* Table styling */
    div[data-testid="stDataFrame"] table {
        background-color: #121212;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #2E7D32;
    }
    
    div[data-testid="stDataFrame"] th {
        background-color: #1B5E20 !important;
        color: white !important;
        padding: 12px 15px !important;
        border-bottom: 2px solid #2E7D32;
    }
    
    div[data-testid="stDataFrame"] td {
        background-color: #121212 !important;
        color: #f0f0f0 !important;
        padding: 10px 15px !important;
        border-bottom: 1px solid #2E7D32;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stDataFrame"] tr:hover td {
        background-color: #1E1E1E !important;
    }
    
    /* Success and error colors */
    .success-text {
        color: #4CAF50 !important;
        font-weight: 600;
    }
    
    .error-text {
        color: #F44336 !important;
        font-weight: 600;
    }
    
    /* Chart styling */
    .chart-container {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.4);
    }
    
    /* Progress bar styling */
    div[role="progressbar"] > div {
        background: linear-gradient(90deg, #4CAF50, #2E7D32) !important;
    }
    
    /* Alert styling */
    div[data-baseweb="notification"] {
        background-color: #121212 !important;
        border: 1px solid #2E7D32 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Select box styling */
    div[data-baseweb="select"] > div {
        background-color: #121212 !important;
        border: 1px solid #2E7D32 !important;
    }
    
    /* Slider styling */
    div[data-testid="stSlider"] > div > div {
        background-color: #2E7D32 !important;
    }
    
    div[data-testid="stSlider"] > div > div > div {
        background-color: #4CAF50 !important;
    }
    
    /* Status indicators */
    .status-on {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(46, 125, 50, 0.4);
        animation: pulse 2s infinite;
    }
    
    .status-off {
        background: linear-gradient(90deg, #F44336, #C62828);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(198, 40, 40, 0.4);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
</style>
""", unsafe_allow_html=True)

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.coordinator_agent import CoordinatorAgent
from config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_RADIUS, CROP_TEMP_RANGES

# Initialize the coordinator agent
@st.cache_resource
def get_coordinator():
    return CoordinatorAgent()

coordinator = get_coordinator()

# Header
st.title("🌿 Greenhouse Intelligence System")
st.markdown("Powered by NASA Earth Data APIs and AI Agent Architecture")

# Sidebar for inputs
st.sidebar.header("Region Selection")

# Map for location selection
with st.sidebar.expander("Select Location on Map", expanded=True):
    # Default location (Bengaluru)
    if 'latitude' not in st.session_state:
        st.session_state.latitude = DEFAULT_LATITUDE
    if 'longitude' not in st.session_state:
        st.session_state.longitude = DEFAULT_LONGITUDE
    
    # Create a container div for better alignment
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Create a map centered at the default location
    m = folium.Map(
        location=[st.session_state.latitude, st.session_state.longitude], 
        zoom_start=10,
        tiles=None,  # Start with no tiles
        width='100%',
        height='100%'
    )
    
    # Add OpenStreetMap tile layer
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name='OpenStreetMap',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add a marker for the selected location
    folium.Marker(
        [st.session_state.latitude, st.session_state.longitude],
        popup="Selected Location",
        tooltip="Selected Location",
        icon=folium.Icon(color="green")
    ).add_to(m)
    
    # Add circle to show radius
    folium.Circle(
        location=[st.session_state.latitude, st.session_state.longitude],
        radius=DEFAULT_RADIUS * 1000,  # Convert km to meters
        color="#4CAF50",
        fill=True,
        fill_opacity=0.2
    ).add_to(m)
    
    # Display the map with full width
    st_folium(m, width=None, height=300)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Manual coordinate input with better alignment
    st.markdown("#### Coordinates")
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", value=st.session_state.latitude, format="%.5f")
    with col2:
        longitude = st.number_input("Longitude", value=st.session_state.longitude, format="%.5f")
        
    # Update session state if values change
    if latitude != st.session_state.latitude or longitude != st.session_state.longitude:
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.rerun()
        
    # Radius selection with better styling
    st.markdown("#### Area Settings")
    radius = st.slider("Radius (km)", min_value=1, max_value=50, value=DEFAULT_RADIUS)

# Crop selection with improved styling
st.sidebar.header("Crop Selection")
crop_options = list(CROP_TEMP_RANGES.keys())
selected_crop = st.sidebar.selectbox("Select Crop", crop_options)

# Display crop temperature range with better styling
min_temp, max_temp = CROP_TEMP_RANGES[selected_crop]
st.sidebar.markdown(f"""
<div style='background-color: #1E1E1E; padding: 10px; border-radius: 5px; border: 1px solid #333;'>
    <p style='margin: 0; color: #4CAF50;'><strong>Ideal Temperature Range</strong></p>
    <p style='margin: 0; font-size: 1.2em;'>{min_temp}°C – {max_temp}°C</p>
</div>
""", unsafe_allow_html=True)

# Data fetching with improved button
st.sidebar.header("Data")
days = st.sidebar.slider("Days of Historical Data", min_value=1, max_value=30, value=6)

fetch_button = st.sidebar.button("Fetch NASA Data", use_container_width=True)
if fetch_button:
    with st.spinner("Fetching data from NASA Earth Data APIs..."):
        result = coordinator.fetch_data(
            st.session_state.latitude,
            st.session_state.longitude,
            radius,
            days
        )
        
        if result['status'] == 'success':
            st.sidebar.success(result['message'])
            
            # Set the crop
            coordinator.set_crop(selected_crop)
            
            # Train the prediction model
            with st.spinner("Training prediction model..."):
                training_result = coordinator.train_prediction_model()
                if training_result['status'] == 'success':
                    st.sidebar.success("Prediction model trained successfully")
                else:
                    st.sidebar.error(training_result['message'])
        else:
            st.sidebar.error(result['message'])

# Main content area
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🔍 Analysis", "📈 History", "🤖 AI Assistant", "🌱 Crop Recommendation"])

# Dashboard tab
with tab1:
    st.header("Greenhouse Intelligence Dashboard")
    
    # Get recommendations if data is available
    if coordinator.current_data is not None and coordinator.current_crop is not None:
        recommendations = coordinator.get_recommendations()
        
        if recommendations['status'] in ['success', 'partial']:
            # Create columns for the dashboard with improved styling
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Current Conditions")
                
                # Create a container for current temperature with animation
                # Get temperature from recommendations structure
                temp_metrics = recommendations['recommendations']['temperature'] if 'recommendations' in recommendations and 'temperature' in recommendations.get('recommendations', {}) else 25.0
                
                st.markdown(f"""
                <div class="chart-container" style="padding: 20px; text-align: center;">
                    <h4 style="margin-bottom: 15px;">Current Temperature</h4>
                    <div style="font-size: 3em; font-weight: 700; margin: 15px 0; 
                         background: linear-gradient(90deg, #4CAF50, #2E7D32); 
                         -webkit-background-clip: text; 
                         -webkit-text-fill-color: transparent;
                         animation: glow 3s ease-in-out infinite alternate;">
                        {temp_metrics:.2f}°C
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display soil moisture if available with a gauge visualization
                soil_moisture = None
                if 'recommendations' in recommendations and 'soil_moisture' in recommendations['recommendations']:
                    soil_moisture = recommendations['recommendations']['soil_moisture']
                
                if soil_moisture is not None:
                    moisture = soil_moisture
                    moisture_color = "#4CAF50" if moisture > 60 else "#FFC107" if moisture > 30 else "#F44336"
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px; text-align: center;">
                        <h4 style="margin-bottom: 15px;">Soil Moisture</h4>
                        <div style="font-size: 2.2em; font-weight: 700; margin: 15px 0; color: {moisture_color};">
                            {moisture:.1f}%
                        </div>
                        <div style="width: 100%; height: 20px; background-color: #333; border-radius: 10px; overflow: hidden; margin-top: 10px;">
                            <div style="height: 100%; width: {moisture}%; 
                                 background: linear-gradient(90deg, 
                                 {('#F44336' if moisture < 30 else '#FFC107' if moisture < 60 else '#4CAF50')}, 
                                 {('#C62828' if moisture < 30 else '#FFA000' if moisture < 60 else '#2E7D32')}); 
                                 border-radius: 10px; transition: width 1s ease-in-out;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                            <span style="color: #F44336;">Dry</span>
                            <span style="color: #FFC107;">Moderate</span>
                            <span style="color: #4CAF50;">Optimal</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Display crop info with enhanced styling
                st.markdown(f"""
                <div class="chart-container" style="padding: 20px;">
                    <h4 style="margin-bottom: 15px; text-align: center;">Crop Information</h4>
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #4CAF50; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">🌱</span>
                        </div>
                        <div>
                            <div style="color: #999; font-size: 0.9em;">Selected Crop</div>
                            <div style="font-size: 1.3em; font-weight: 600;">{coordinator.current_crop}</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #2196F3; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">📉</span>
                        </div>
                        <div>
                            <div style="color: #999; font-size: 0.9em;">Ideal Temperature Range</div>
                            <div style="font-size: 1.3em; font-weight: 600;">{recommendations.get('ideal_range', 'N/A')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display feasibility with enhanced styling
                if 'feasibility' in recommendations:
                    feasibility = recommendations['feasibility']
                    icon = "✅" if feasibility == 'Ideal' else "⚠️" if feasibility in ['Above Ideal', 'Below Ideal'] else "❌"
                    color = "#4CAF50" if feasibility == 'Ideal' else "#FFC107" if feasibility in ['Above Ideal', 'Below Ideal'] else "#F44336"
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px; text-align: center;">
                        <h4 style="margin-bottom: 15px;">Growing Conditions</h4>
                        <div style="font-size: 1.8em; font-weight: 700; margin: 15px 0; color: {color};">
                            {icon} {feasibility}
                        </div>
                        <div style="color: #999; font-size: 0.9em;">
                            {
                            "Current temperature is within the ideal range for this crop." if feasibility == 'Ideal' else
                            "Temperature is higher than the ideal range for this crop." if feasibility == 'Above Ideal' else
                            "Temperature is lower than the ideal range for this crop." if feasibility == 'Below Ideal' else
                            "Current conditions are not suitable for this crop."
                            }
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("Recommendations")
                
                # Display predicted temperature with animation
                if 'prediction' in recommendations and 'predicted_temperature' in recommendations['prediction']:
                    pred_temp = recommendations['prediction']['predicted_temperature']
                    current_temp = recommendations['recommendations'].get('temperature', 25.0)
                    temp_diff = pred_temp - current_temp
                    trend = "rising" if temp_diff > 0.5 else "falling" if temp_diff < -0.5 else "stable"
                    trend_icon = "↗️" if trend == "rising" else "↘️" if trend == "falling" else "➡️"
                    trend_color = "#F44336" if trend == "rising" else "#2196F3" if trend == "falling" else "#FFC107"
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px; text-align: center;">
                        <h4 style="margin-bottom: 15px;">Predicted Temperature (Next Day)</h4>
                        <div style="font-size: 3em; font-weight: 700; margin: 15px 0; 
                             background: linear-gradient(90deg, #2196F3, #1976D2); 
                             -webkit-background-clip: text; 
                             -webkit-text-fill-color: transparent;
                             animation: glow 3s ease-in-out infinite alternate;">
                            {pred_temp:.2f}°C
                        </div>
                        <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                            <span style="margin-right: 10px;">Trend:</span>
                            <span style="color: {trend_color}; font-weight: 600;">
                                {trend_icon} {trend.capitalize()} ({temp_diff:+.2f}°C)
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display actuator recommendations with animated status indicators
                actuators = recommendations.get('actuator_recommendations', {
                    'fan': 'OFF',
                    'heater': 'OFF',
                    'water_pump': 'OFF',
                    'reasoning': 'No actuator recommendations available'
                })
                
                # Make sure actuators has all required keys
                if not isinstance(actuators, dict):
                    actuators = {
                        'fan': 'OFF',
                        'heater': 'OFF',
                        'water_pump': 'OFF',
                        'reasoning': 'No actuator recommendations available'
                    }
                
                # Ensure all required keys exist
                for key in ['fan', 'heater', 'water_pump', 'reasoning']:
                    if key not in actuators:
                        actuators[key] = 'OFF' if key != 'reasoning' else 'No data available'
                
                st.markdown("""
                <div class="chart-container" style="padding: 20px;">
                    <h4 style="margin-bottom: 15px; text-align: center;">Actuator Control</h4>
                """, unsafe_allow_html=True)
                
                # Fan status
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                             background-color: {'#4CAF50' if actuators['fan'] == 'ON' else '#333'}; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;
                             {'animation: pulse 2s infinite' if actuators['fan'] == 'ON' else ''}">
                            <span style="color: white; font-size: 20px;">💨</span>
                        </div>
                        <span style="font-size: 1.2em;">Fan</span>
                    </div>
                    <span class="{'status-on' if actuators['fan'] == 'ON' else 'status-off'}">{actuators['fan']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Heater status
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                             background-color: {'#4CAF50' if actuators['heater'] == 'ON' else '#333'}; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;
                             {'animation: pulse 2s infinite' if actuators['heater'] == 'ON' else ''}">
                            <span style="color: white; font-size: 20px;">🔥</span>
                        </div>
                        <span style="font-size: 1.2em;">Heater</span>
                    </div>
                    <span class="{'status-on' if actuators['heater'] == 'ON' else 'status-off'}">{actuators['heater']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Water pump status
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                             background-color: {'#4CAF50' if actuators['water_pump'] == 'ON' else '#333'}; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;
                             {'animation: pulse 2s infinite' if actuators['water_pump'] == 'ON' else ''}">
                            <span style="color: white; font-size: 20px;">💧</span>
                        </div>
                        <span style="font-size: 1.2em;">Water Pump</span>
                    </div>
                    <span class="{'status-on' if actuators['water_pump'] == 'ON' else 'status-off'}">{actuators['water_pump']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Display reasoning
                st.markdown(f"""
                <div style="margin-top: 20px; padding: 15px; background-color: #1E1E1E; border-radius: 5px; border-left: 4px solid #4CAF50;">
                    <div style="color: #4CAF50; font-weight: 600; margin-bottom: 5px;">Reasoning:</div>
                    <div style="color: #ddd;">{actuators['reasoning']}</div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Display temperature chart with improved styling
            st.subheader("Temperature History")
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            plt.style.use('dark_background')
            
            # Set dark background
            fig.patch.set_facecolor('#121212')
            ax.set_facecolor('#121212')
            
            # Plot temperature data with improved styling
            data = coordinator.current_data
            
            # Add ideal range as a shaded area
            min_temp, max_temp = CROP_TEMP_RANGES[selected_crop]
            ax.axhspan(min_temp, max_temp, alpha=0.2, color='#4CAF50', label='Ideal Range')
            
            # Plot the temperature line with gradient color based on temperature
            cmap = plt.cm.RdYlGn_r
            norm = plt.Normalize(min_temp - 5, max_temp + 5)
            
            for i in range(len(data) - 1):
                ax.plot([data['date'].iloc[i], data['date'].iloc[i+1]], 
                       [data['temperature'].iloc[i], data['temperature'].iloc[i+1]], 
                       color=cmap(norm(data['temperature'].iloc[i])), 
                       linewidth=3)
            
            # Add scatter points
            scatter = ax.scatter(data['date'], data['temperature'], 
                               c=data['temperature'], cmap=cmap, norm=norm, 
                               s=100, zorder=5, edgecolor='white', linewidth=1)
            
            # Add labels and grid
            ax.set_xlabel('Date', color='#999')
            ax.set_ylabel('Temperature (°C)', color='#999')
            ax.set_title(f'Temperature History with Ideal Range for {selected_crop}', 
                        color='#4CAF50', fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.3, color='#555')
            
            # Set tick colors
            ax.tick_params(colors='#999')
            for spine in ax.spines.values():
                spine.set_edgecolor('#555')
            
            # Add colorbar
            cbar = fig.colorbar(scatter, ax=ax)
            cbar.set_label('Temperature (°C)', color='#999')
            cbar.ax.yaxis.set_tick_params(color='#999')
            cbar.outline.set_edgecolor('#555')
            
            # Format x-axis dates
            fig.autofmt_xdate()
            
            # Add legend
            ax.legend(loc='upper right', framealpha=0.8, facecolor='#121212', edgecolor='#555')
            
            # Add value labels for the last point
            last_temp = data['temperature'].iloc[-1]
            last_date = data['date'].iloc[-1]
            ax.annotate(f'{last_temp:.2f}°C', 
                       xy=(last_date, last_temp),
                       xytext=(0, 10),
                       textcoords='offset points',
                       ha='center', va='bottom',
                       color='white', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', fc='#4CAF50', alpha=0.7))
            
            fig.tight_layout()
            
            # Display the chart
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.warning(recommendations['message'])
    else:
        st.info("Please fetch data using the sidebar controls to view the dashboard.")

# Analysis tab
with tab2:
    st.header("Environmental Analysis")
    
    if coordinator.current_data is not None:
        # Get analysis results
        analysis = coordinator.analyze_conditions()
        
        if analysis['status'] == 'success':
            # Display temperature metrics
            st.subheader("Temperature Metrics")
            temp_metrics = analysis['temperature']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Temperature", f"{temp_metrics['mean']:.2f}°C")
            with col2:
                st.metric("Min Temperature", f"{temp_metrics['min']:.2f}°C")
            with col3:
                st.metric("Max Temperature", f"{temp_metrics['max']:.2f}°C")
            with col4:
                st.metric("Trend", temp_metrics['trend'].capitalize())
                
            # Display crop suitability
            st.subheader("Crop Suitability Analysis")
            
            # Create a DataFrame for the crop suitability data
            crop_data = []
            for crop, metrics in analysis['crop_suitability'].items():
                crop_data.append({
                    'Crop': crop,
                    'Status': metrics['status'],
                    'Score': metrics['score'],
                    'Deviation': metrics['deviation'],
                    'Ideal Range': metrics['ideal_range']
                })
                
            crop_df = pd.DataFrame(crop_data)
            
            # Sort by score (descending)
            crop_df = crop_df.sort_values('Score', ascending=False)
            
            # Display as a table
            st.dataframe(crop_df, use_container_width=True)
            
            # Create a bar chart of crop scores
            st.subheader("Crop Suitability Scores")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Create bars with color based on score
            bars = ax.bar(crop_df['Crop'], crop_df['Score'], color=plt.cm.RdYlGn(crop_df['Score']/100))
            
            # Add labels
            ax.set_xlabel('Crop')
            ax.set_ylabel('Suitability Score (0-100)')
            ax.set_ylim(0, 100)
            ax.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height:.0f}', ha='center', va='bottom')
                
            st.pyplot(fig)
            
            # Display soil moisture if available
            if analysis['soil_moisture'] is not None:
                st.subheader("Soil Moisture")
                st.metric("Current Soil Moisture", f"{analysis['soil_moisture']:.1f}%")
                
                # Create a gauge chart for soil moisture
                fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': 'polar'})
                
                # Convert moisture percentage to radians (0-100% -> 0-π)
                moisture = analysis['soil_moisture']
                theta = np.pi * (moisture / 100)
                
                # Create the gauge
                ax.set_theta_zero_location("N")
                ax.set_theta_direction(-1)
                ax.set_rlim(0, 1)
                ax.set_thetamin(0)
                ax.set_thetamax(180)
                
                # Add colored regions
                ax.bar(np.linspace(0, np.pi/3, 50), [1]*50, width=np.pi/150, color=plt.cm.Reds_r(np.linspace(0.2, 0.8, 50)))
                ax.bar(np.linspace(np.pi/3, 2*np.pi/3, 50), [1]*50, width=np.pi/150, color=plt.cm.Greens(np.linspace(0.2, 0.8, 50)))
                ax.bar(np.linspace(2*np.pi/3, np.pi, 50), [1]*50, width=np.pi/150, color=plt.cm.Blues_r(np.linspace(0.2, 0.8, 50)))
                
                # Add the needle
                ax.plot([0, theta], [0, 0.8], color='black', linewidth=2)
                ax.scatter(theta, 0.8, color='black', s=50)
                
                # Remove unnecessary elements
                ax.set_yticklabels([])
                ax.set_xticklabels(['0%', '', '30%', '', '60%', '', '100%'])
                ax.spines['polar'].set_visible(False)
                
                # Add title
                ax.set_title('Soil Moisture Level', pad=15)
                
                st.pyplot(fig)
        else:
            st.warning(analysis['message'])
    else:
        st.info("Please fetch data using the sidebar controls to view the analysis.")

# History tab
with tab3:
    st.header("Historical Performance")

    # Get historical data
    try:
        history = coordinator.get_historical_performance()
        
        if history['status'] == 'success':
            # Display prediction accuracy
            accuracy = history['performance']['prediction_accuracy']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Mean Absolute Error", 
                        f"{accuracy['mae']:.2f}°C" if accuracy['mae'] is not None else "N/A")
                
            with col2:
                st.metric("Root Mean Square Error", 
                        f"{accuracy['rmse']:.2f}°C" if accuracy['rmse'] is not None else "N/A")
                
            # Display performance history
            if history['performance']['history']:
                st.subheader(f"Performance History for {history['performance']['crop']}")
                
                # Convert to DataFrame for easier plotting
                df = pd.DataFrame(history['performance']['history'])
                df['date'] = pd.to_datetime(df['date'])
                
                fig, ax = plt.subplots(figsize=(10, 5))
                plt.style.use('dark_background')
                
                # Set dark background
                fig.patch.set_facecolor('#121212')
                ax.set_facecolor('#121212')
                
                # Plot performance scores
                ax.plot(df['date'], df['score'], color='#4CAF50', linewidth=3, marker='o', 
                    markersize=8, markerfacecolor='#4CAF50', markeredgecolor='white')
                
                # Add labels and grid
                ax.set_xlabel('Date', color='#999')
                ax.set_ylabel('Performance Score', color='#999')
                ax.set_title(f'Performance History for {history["performance"]["crop"]}', 
                            color='#4CAF50', fontsize=14, fontweight='bold')
                ax.grid(True, linestyle='--', alpha=0.3, color='#555')
                
                # Set tick colors
                ax.tick_params(colors='#999')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#555')
                    
                st.pyplot(fig)
            else:
                st.info(f"No performance history available for {history['performance']['crop']}")
        else:
            st.warning(history['message'])
    except (AttributeError, KeyError) as e:
        st.warning(f"Historical performance data is not available yet. Please set a crop and generate some predictions first.")
        print(f"Error in historical performance tab: {e}")

# AI Assistant tab
with tab4:
    st.header("🤖 AI-Powered Greenhouse Assistant")
    
    # Create a single column for the assistant
    st.subheader("Ask the Greenhouse Assistant")
    
    # Question input
    user_question = st.text_input("Ask a question about greenhouse management, crops, or environmental conditions:", 
                                 placeholder="E.g., What caused the temperature drop on June 5?")
    
    # Use context toggle
    use_context = st.toggle("Use historical context for answers", value=True)
    
    # Submit button with custom styling
    if st.button("Ask Assistant", use_container_width=True):
        if user_question:
            with st.spinner("Generating response..."):
                # Get response from LLM assistant
                response = coordinator.ask_assistant(user_question, use_context=use_context)
                
                if response['status'] == 'success':
                    # Display the response in a styled container
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.markdown(f"**Question:** {user_question}")
                    st.markdown(f"**Answer:** {response['response']}")
                    
                    # Show context info
                    if use_context:
                        st.markdown(
                            "<div style='font-size: 0.8em; color: #999; margin-top: 15px;'>"
                            "Response generated using historical environmental data context."
                            "</div>", 
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(response['message'])
        else:
            st.warning("Please enter a question.")

# Crop Recommendation tab
with tab5:
    st.header("🌱 Crop Recommendation System")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Environmental Conditions")
        # Temperature and moisture inputs
        temp = st.slider("Temperature (°C)", min_value=0.0, max_value=40.0, value=25.0, step=0.5)
        moisture = st.slider("Soil Moisture (%)", min_value=0, max_value=100, value=60)
        
        # Get recommendations button
        if st.button("Get Recommendations", use_container_width=True):
            with st.spinner("Analyzing conditions..."):
                # Get crop recommendations
                recommendations = coordinator.get_crop_recommendations(temp, moisture)
                
                if recommendations['status'] == 'success':
                    # Display recommendations in a styled container
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    
                    # Show recommended crops
                    rec = recommendations['recommendations']
                    if rec['recommended_crops']:
                        st.markdown("### Recommended Crops")
                        for crop in rec['recommended_crops']:
                            st.markdown(f"✅ **{crop}**")
                    else:
                        st.markdown("### No crops perfectly match these conditions")
                    
                    # Show explanation
                    st.markdown("### Expert Analysis")
                    st.markdown(rec['explanation'])
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(recommendations['message'])
    
    with col2:
        st.subheader("Crop Information")
        # Add crop information cards
        crops = ["Tomato", "Cucumber", "Lettuce", "Bell Pepper", "Spinach"]
        selected_crop = st.selectbox("Select a crop for detailed information", crops)
        
        # Display crop information based on selection
        if selected_crop == "Tomato":
            st.markdown("""
            <div style="background-color:#1E3C40; padding:15px; border-radius:10px">
                <h3 style="color:#4CAF50">🍅 Tomato</h3>
                <p><b>Ideal Temperature:</b> 21-27°C (70-80°F)</p>
                <p><b>Ideal Soil Moisture:</b> 60-70%</p>
                <p><b>Growing Period:</b> 60-80 days</p>
                <p><b>Light Requirements:</b> Full sun (6+ hours)</p>
                <p><b>Special Notes:</b> Requires support for vining varieties. Sensitive to temperature fluctuations for fruit setting.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_crop == "Cucumber":
            st.markdown("""
            <div style="background-color:#1E3C40; padding:15px; border-radius:10px">
                <h3 style="color:#4CAF50">🥒 Cucumber</h3>
                <p><b>Ideal Temperature:</b> 18-25°C (65-77°F)</p>
                <p><b>Ideal Soil Moisture:</b> 65-75%</p>
                <p><b>Growing Period:</b> 50-70 days</p>
                <p><b>Light Requirements:</b> Full sun (6+ hours)</p>
                <p><b>Special Notes:</b> Needs consistent moisture. Benefits from trellising. Sensitive to cold temperatures.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_crop == "Lettuce":
            st.markdown("""
            <div style="background-color:#1E3C40; padding:15px; border-radius:10px">
                <h3 style="color:#4CAF50">🥬 Lettuce</h3>
                <p><b>Ideal Temperature:</b> 15-20°C (60-68°F)</p>
                <p><b>Ideal Soil Moisture:</b> 60-70%</p>
                <p><b>Growing Period:</b> 30-60 days</p>
                <p><b>Light Requirements:</b> Partial shade to full sun</p>
                <p><b>Special Notes:</b> Cool season crop. Will bolt (go to seed) in high temperatures. Good for succession planting.</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_crop == "Bell Pepper":
            st.markdown("""
            <div style="background-color:#1E3C40; padding:15px; border-radius:10px">
                <h3 style="color:#4CAF50">🫑 Bell Pepper</h3>
                <p><b>Ideal Temperature:</b> 18-24°C (65-75°F)</p>
                <p><b>Ideal Soil Moisture:</b> 60-65%</p>
                <p><b>Growing Period:</b> 60-90 days</p>
                <p><b>Light Requirements:</b> Full sun (6+ hours)</p>
                <p><b>Special Notes:</b> Needs warm soil to germinate. May drop flowers if temperatures exceed 32°C (90°F).</p>
            </div>
            """, unsafe_allow_html=True)
        elif selected_crop == "Spinach":
            st.markdown("""
            <div style="background-color:#1E3C40; padding:15px; border-radius:10px">
                <h3 style="color:#4CAF50">🍃 Spinach</h3>
                <p><b>Ideal Temperature:</b> 10-20°C (50-68°F)</p>
                <p><b>Ideal Soil Moisture:</b> 60-70%</p>
                <p><b>Growing Period:</b> 40-50 days</p>
                <p><b>Light Requirements:</b> Partial shade to full sun</p>
                <p><b>Special Notes:</b> Cool season crop that bolts quickly in heat. Good for succession planting and early/late season growing.</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("Powered by codexcherry")
st.markdown("© 2025 Greenhouse Intelligence System")
st.markdown("</div>", unsafe_allow_html=True) 
