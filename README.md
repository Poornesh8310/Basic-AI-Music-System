# Basic-Music-System
Basic Music System: A Python project that blends algorithmic music composition with audio mood detection. It generates unique melodies and uses digital signal processing to analyze audio moods—all within an interactive Streamlit web interface.

**Note**: This project is not deployed version and runs locally.

This Python-based project mainly combines algorithmic music generation with audio mood detection. The system generates unique melodies using algorithmic composition techniques and then analyzes the mood of audio files using digital signal processing (DSP) and rule-based classification.

## Features

- **Melody Generation:**  
  - Generates unique melodies by randomly selecting notes from a specified musical scale (e.g., C Major, A Minor).
  - Randomly selects instruments from a predefined list of General MIDI programs.
  - Converts generated MIDI files to WAV files using FluidSynth via the `midi2audio` package.

- **Mood Detection:**  
  - Extracts audio features such as tempo, spectral centroid, spectral bandwidth, spectral rolloff, zero crossing rate, and RMS energy using Librosa.
  - Classifies the mood (Energetic, Calm, or Neutral) based on rule-based thresholds.
  - Provides a detailed criteria analysis of the features used for mood classification.

- **User Interface:**  
  - A Streamlit-based web application that lets you:
    - Generate melodies with customizable parameters (tempo, melody length, scale).
    - Preview generated melodies with an integrated audio player.
    - Upload audio files to analyze their mood.
    - Visualize audio features using Plotly radar charts and tables.

## Project Structure

<pre>
  <code>
    AI_Music_System/
├── data/
│   ├── raw_songs/        # Store sample audio files here
│   └── midi/            # Pre-trained MIDI datasets (optional)
├── scripts/
│   ├── music_generator.py # Melody generation script
│   ├── mood_detection.py  # Mood analysis script
│   └── app.py           # Streamlit UI
├── generated/
│   ├── midi/            # AI-generated MIDI files
│   └── audio/           # Rendered WAV/MP3 files
├── FluidR3_GM/          # SoundFont for MIDI rendering
│   └── FluidR3_GM.sf2   # The SoundFont file
└── requirements.txt     # List of dependencies
  </code>
</pre>


## Prerequisites

- **Python 3.11** (or another supported version)
- **FluidSynth:**  
  Install via Homebrew on macOS:
  ```bash
  brew install fluid-synth

### SoundFont :
Download the FluidR3_GM.sf2 file from the internet and place it in a known directory. **Update** the SOUND_FONT path in music_generator.py accordingly. This helps in previewing of the generated melody in the interface.

## Installation :

### **Clone the repository** : 
<pre>
  <code>
    git clone https://github.com/your-username/AI_Music_System.git
    cd AI_Music_System
  </code>
</pre>

### **Create and activate a virtual environment** :
<pre>
  <code>
    python3 -m venv ai_music_env
    source ai_music_env/bin/activate  # On macOS/Linux
    # For Windows: ai_music_env\Scripts\activate
  </code>
</pre>

**Or** you can also use the Conda environments with the following code :
<pre>
  <code>
    conda create -n ai_music_env_py311 python=3.11
    conda activate ai_music_env_py311
  </code>
</pre>

### **Install Dependencies:**
<pre>
  <code>
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
  </code>
</pre>

## Usage:

### **Run the Streamlit Application:**
From the project root, run:
<pre>
  <code>
    streamlit run scripts/app.py
  </code>
</pre>
This will open the web interface in your default browser.

### **Generate a Melody:**
- Navigate to the "Generate Melody" section.
- Adjust parameters such as tempo, melody length, and scale.
- Click "Generate Melody" to create and preview the generated melody along with the selected instrument.
- The generated melody can be previewed in the same page and it is also saved in the generated folder.

### **Detect Mood:**
- Navigate to the "Mood Detection" section.
- Upload an audio file (MP3/WAV) to analyze its mood.
- View detailed audio feature analysis and criteria comparisons.

**Note:** refer the "screenshots of the project.pdf" it contains the images of the project interface. 

## How it uses AI :
Although the project uses rule-based methods rather than advanced deep learning models, it employs key AI concepts:

- **Algorithmic Composition:**
  The system generates unique melodies by randomly selecting notes from a chosen musical scale (such as C Major or A Minor). It further enriches the creative process by randomly picking from a variety of General MIDI instruments. The melodies are initially created as MIDI files using the PrettyMIDI library and are then converted into WAV files with FluidSynth (via the midi2audio package), allowing them to be played and previewed.
  
- **Digital Signal Processing (DSP) for Feature Extraction:**
  The project leverages the Librosa library to extract critical audio features—such as tempo, spectral centroid, spectral bandwidth, spectral rolloff, zero crossing rate, and RMS energy—from audio files. These features are used in a rule-based classifier that compares them against predefined thresholds to categorize the mood of a song as "Energetic," "Calm," or "Neutral." This approach illustrates how digital signal processing can mimic aspects of human auditory perception and decision-making.
  
- **Automated Decision-Making:**
  The entire system is wrapped in an intuitive Streamlit web application. Users can generate new melodies by adjusting parameters like tempo, melody length, and scale, and then preview the results instantly. Additionally, users can upload any audio file (MP3/WAV) to analyze its mood, with the app providing a detailed breakdown of the extracted audio features and the criteria used for classification.

Overall, AI Music System is an accessible and engaging example of applying AI techniques to the creative domain of music. It showcases how algorithmic methods and DSP can be harnessed to automate both the composition of music and the interpretation of its emotional content.

## Acknowledgements:
- Librosa for audio analysis.
- PrettyMIDI for MIDI file handling.
- Streamlit for the interactive web interface.
- midi2audio for MIDI-to-WAV conversion.

# Thank you!!!

**Suggestion and Contributions are always welcome!** <br> Please fork the repository and create a pull request with your changes.
