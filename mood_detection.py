# mood_detection.py
import scipy.signal.windows as windows
import librosa
import numpy as np
import os
from typing import Dict, Union, Tuple

class MoodDetector:
    # Define thresholds as class constants
    THRESHOLDS = {
        'energetic': {
            'tempo': 110,
            'spectral_centroid': 2000,
            'spectral_bandwidth': 1500,
            'rms': 0.05
        },
        'calm': {
            'tempo': 90,
            'spectral_centroid': 1500,
            'spectral_bandwidth': 1200,
            'rms': 0.03
        }
    }

    @staticmethod
    def extract_features(y: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract audio features from the signal using the Hann window from scipy.signal.windows."""
        # Use the Hann window function directly from scipy.signal.windows
        window_func = windows.hann

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroid = np.mean(
            librosa.feature.spectral_centroid(y=y, sr=sr, window=window_func)
        )
        spectral_bandwidth = np.mean(
            librosa.feature.spectral_bandwidth(y=y, sr=sr, window=window_func)
        )
        spectral_rolloff = np.mean(
            librosa.feature.spectral_rolloff(y=y, sr=sr, window=window_func)
        )
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
        rms = np.mean(librosa.feature.rms(y=y))

        return {
            'tempo': tempo,
            'spectral_centroid': spectral_centroid,
            'spectral_bandwidth': spectral_bandwidth,
            'spectral_rolloff': spectral_rolloff,
            'zero_crossing_rate': zero_crossing_rate,
            'rms': rms
        }

    @staticmethod
    def classify_mood(features: Dict[str, float]) -> Tuple[str, Dict[str, bool]]:
        """Classify mood based on features and return mood with criteria details."""
        # Check energetic criteria
        is_energetic = all([
            features['tempo'] > MoodDetector.THRESHOLDS['energetic']['tempo'],
            features['spectral_centroid'] > MoodDetector.THRESHOLDS['energetic']['spectral_centroid'],
            features['spectral_bandwidth'] > MoodDetector.THRESHOLDS['energetic']['spectral_bandwidth'],
            features['rms'] > MoodDetector.THRESHOLDS['energetic']['rms']
        ])

        # Check calm criteria
        is_calm = all([
            features['tempo'] < MoodDetector.THRESHOLDS['calm']['tempo'],
            features['spectral_centroid'] < MoodDetector.THRESHOLDS['calm']['spectral_centroid'],
            features['spectral_bandwidth'] < MoodDetector.THRESHOLDS['calm']['spectral_bandwidth'],
            features['rms'] < MoodDetector.THRESHOLDS['calm']['rms']
        ])

        criteria_met = {
            'energetic_criteria': {
                'tempo': features['tempo'] > MoodDetector.THRESHOLDS['energetic']['tempo'],
                'spectral_centroid': features['spectral_centroid'] > MoodDetector.THRESHOLDS['energetic']['spectral_centroid'],
                'spectral_bandwidth': features['spectral_bandwidth'] > MoodDetector.THRESHOLDS['energetic']['spectral_bandwidth'],
                'rms': features['rms'] > MoodDetector.THRESHOLDS['energetic']['rms']
            },
            'calm_criteria': {
                'tempo': features['tempo'] < MoodDetector.THRESHOLDS['calm']['tempo'],
                'spectral_centroid': features['spectral_centroid'] < MoodDetector.THRESHOLDS['calm']['spectral_centroid'],
                'spectral_bandwidth': features['spectral_bandwidth'] < MoodDetector.THRESHOLDS['calm']['spectral_bandwidth'],
                'rms': features['rms'] < MoodDetector.THRESHOLDS['calm']['rms']
            }
        }

        if is_energetic:
            return "Energetic 🎉", criteria_met
        elif is_calm:
            return "Calm 😌", criteria_met
        else:
            return "Neutral 🎶", criteria_met

    @staticmethod
    def detect_mood(audio_path: str) -> Dict[str, Union[str, Dict, float]]:
        """
        Detect mood from audio file and return detailed analysis.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing mood classification and detailed analysis
        """
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError("Audio file not found")

            # Load and analyze audio
            y, sr = librosa.load(audio_path)
            features = MoodDetector.extract_features(y, sr)
            mood, criteria_met = MoodDetector.classify_mood(features)

            return {
                'mood': mood,
                'features': features,
                'criteria_met': criteria_met,
                'status': 'success'
            }

        except Exception as e:
            return {
                'mood': "Error",
                'error_message': str(e),
                'status': 'error'
            }

def main():
    sample_path = 'data/raw_songs/sample.mp3'
    detector = MoodDetector()
    result = detector.detect_mood(sample_path)
    
    if result['status'] == 'success':
        print(f"\nDetected Mood: {result['mood']}")
        print("\nAudio Features:")
        for feature, value in result['features'].items():
            print(f"{feature}: {value:.2f}")
        
        print("\nCriteria Analysis:")
        for mood_type, criteria in result['criteria_met'].items():
            print(f"\n{mood_type}:")
            for criterion, met in criteria.items():
                print(f"  {criterion}: {'✓' if met else '✗'}")
    else:
        print(f"Error: {result['error_message']}")

if __name__ == '__main__':
    main()
