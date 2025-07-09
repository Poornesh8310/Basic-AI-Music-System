import streamlit as st
from music_generator import generate_melody, INSTRUMENT_OPTIONS
from mood_detection import MoodDetector
import os
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any
import time

class MusicSystemApp:
    def __init__(self):
        self.mood_detector = MoodDetector()
        self.setup_page()
        
    def setup_page(self):
        """Initialize the Streamlit page configuration"""
        st.set_page_config(
            page_title="AI Music System",
            page_icon="🎵",
            layout="wide"
        )
        st.title("AI Music System 🎵")
        
    def display_melody_generation(self):
        """Handle melody generation section"""
        st.header("Generate a Melody 🎼")
        
        col1, col2 = st.columns(2)
        with col1:
            tempo = st.slider("Tempo (BPM)", 60, 180, 120)
            melody_length = st.slider("Melody Length (beats)", 8, 64, 32)
        with col2:
            st.write("Generation Settings")
            advanced_options = st.expander("Advanced Options")
            with advanced_options:
                scale_options = {
                    "C Major": [60, 62, 64, 65, 67, 69, 71, 72],
                    "A Minor": [57, 59, 60, 62, 64, 65, 67, 69]
                }
                selected_scale_name = st.selectbox("Scale", list(scale_options.keys()))
                selected_scale = scale_options[selected_scale_name]
        
        if st.button("Generate Melody", key="generate_button"):
            with st.spinner("Generating melody..."):
                # Pass the selected scale to the melody generator.
                result = generate_melody(melody_length, tempo, selected_scale)
                
                if result[1] is None:  # Error occurred
                    st.error(result[0])
                else:
                    midi_path, wav_path, program = result
                    instrument_name = INSTRUMENT_OPTIONS.get(program, f"Program {program}")
                    st.success("✨ Melody generated successfully!")
                    
                    # Display file information in an organized way
                    info_col1, info_col2, info_col3 = st.columns(3)
                    with info_col1:
                        st.info(f"📄 MIDI File: {os.path.basename(midi_path)}")
                    with info_col2:
                        st.info(f"🔊 WAV File: {os.path.basename(wav_path)}")
                    with info_col3:
                        st.info(f"🎹 Instrument: {instrument_name}")
                    
                    # Audio player with some styling
                    st.write("### Preview Your Melody")
                    try:
                        with open(wav_path, "rb") as audio_file:
                            audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format="audio/wav")
                        
                        # Analyze the generated melody's mood
                        mood_result = self.mood_detector.detect_mood(wav_path)
                        if mood_result['status'] == 'success':
                            st.write(f"🎭 Generated Melody Mood: {mood_result['mood']}")
                    except Exception as e:
                        st.error(f"Error playing audio: {str(e)}")

    def display_mood_detection(self):
        """Handle mood detection section"""
        st.header("Mood Detection 🎭")
        
        uploaded_file = st.file_uploader(
            "Upload a song (MP3/WAV)", 
            type=['mp3', 'wav'],
            help="Upload an audio file to analyze its mood"
        )
        
        if uploaded_file:
            with st.spinner("Analyzing mood..."):
                # Save uploaded file
                temp_path = "data/raw_songs/temp_uploaded.mp3"
                os.makedirs("data/raw_songs", exist_ok=True)
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Analyze mood
                result = self.mood_detector.detect_mood(temp_path)
                
                if result['status'] == 'success':
                    # Create tabs for different views
                    mood_tab, features_tab, analysis_tab = st.tabs([
                        "Mood Result", "Audio Features", "Detailed Analysis"
                    ])
                    
                    with mood_tab:
                        st.success(f"### Detected Mood: {result['mood']}")
                        
                    with features_tab:
                        self.display_audio_features(result['features'])
                        
                    with analysis_tab:
                        self.display_criteria_analysis(result['criteria_met'])
                else:
                    st.error(f"Error analyzing mood: {result['error_message']}")

    def display_audio_features(self, features: Dict[str, float]):
        """Display audio features with visualizations"""
        # Create a radar chart for the features
        categories = list(features.keys())
        values = list(features.values())
        
        # Normalize values for better visualization
        max_values = {
            'tempo': 200,
            'spectral_centroid': 3000,
            'spectral_bandwidth': 2000,
            'spectral_rolloff': 12000,
            'zero_crossing_rate': 0.3,
            'rms': 0.1
        }
        
        normalized_values = [
            min(1.0, features[cat] / max_values[cat]) for cat in categories
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=categories,
            fill='toself',
            name='Audio Features'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False
        )
        
        st.plotly_chart(fig)
        
        # Display actual values in a formatted table
        feature_df = pd.DataFrame({
            'Feature': categories,
            'Value': [f"{v:.2f}" for v in values]
        })
        st.table(feature_df)

    def display_criteria_analysis(self, criteria: Dict[str, Dict[str, bool]]):
        """Display detailed criteria analysis"""
        for mood_type, checks in criteria.items():
            st.write(f"### {mood_type.replace('_', ' ').title()}")
            for criterion, met in checks.items():
                if met:
                    st.success(f"✓ {criterion}")
                else:
                    st.error(f"✗ {criterion}")

    def run(self):
        """Main method to run the application"""
        # Add a navigation menu
        menu = ["Home", "Generate Melody", "Mood Detection"]
        choice = st.sidebar.selectbox("Navigation", menu)
        
        if choice == "Home":
            st.write("""
            ## Welcome to AI Music System! 🎵
            
            This system combines AI-powered music generation with mood detection capabilities.
            
            ### Features:
            - 🎼 Generate unique melodies with customizable parameters
            - 🎭 Analyze the mood of any audio file
            - 📊 Get detailed audio feature analysis
            
            Choose an option from the sidebar to get started!
            """)
        
        elif choice == "Generate Melody":
            self.display_melody_generation()
            
        elif choice == "Mood Detection":
            self.display_mood_detection()

if __name__ == "__main__":
    app = MusicSystemApp()
    app.run()
