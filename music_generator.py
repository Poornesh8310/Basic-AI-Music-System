import pretty_midi
import numpy as np
import os
import datetime
import random
from midi2audio import FluidSynth

# Set your soundfont path here.
SOUND_FONT = "file_path"  

if not os.path.exists(SOUND_FONT):
    print(f"Warning: SoundFont not found at {SOUND_FONT}. Please update the SOUND_FONT variable with the correct path.")

# Predefined instrument options (General MIDI programs)
INSTRUMENT_OPTIONS = {
    0: "Acoustic Grand Piano",
    1: "Bright Acoustic Piano",
    2: "Electric Grand Piano",
    4: "Electric Piano 1",
    24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)",
    40: "Violin",
    41: "Viola",
    56: "Trumpet",
    73: "Flute",
    80: "Lead 1 (square)",
    81: "Lead 2 (sawtooth)"
}

def generate_melody(melody_length=32, tempo=120, scale=None):
    """
    Generates a random melody as a MIDI file and converts it to a WAV file.
    Accepts an optional scale (list of MIDI note numbers).
    Returns a tuple (midi_path, wav_path, instrument_program) or (error_message, None, None) on error.
    """
    try:
        # Use default C Major scale if none is provided.
        if scale is None:
            scale = [60, 62, 64, 65, 67, 69, 71, 72]
        
        # Create a PrettyMIDI object with the specified tempo.
        pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
        # Randomly select an instrument from our options.
        program = random.choice(list(INSTRUMENT_OPTIONS.keys()))
        instrument = pretty_midi.Instrument(program=program)
        
        # Calculate note duration (quarter note) in seconds.
        note_duration = 60.0 / tempo
        start_time = 0.0
        
        # Generate the melody: choose random notes from the given scale.
        for _ in range(melody_length):
            note_number = np.random.choice(scale)
            note = pretty_midi.Note(
                velocity=100, 
                pitch=note_number,
                start=start_time, 
                end=start_time + note_duration
            )
            instrument.notes.append(note)
            start_time += note_duration
        
        pm.instruments.append(instrument)
        
        # Create unique file names using a timestamp.
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        midi_dir = os.path.join("generated", "midi")
        wav_dir = os.path.join("generated", "audio")
        os.makedirs(midi_dir, exist_ok=True)
        os.makedirs(wav_dir, exist_ok=True)
        midi_path = os.path.join(midi_dir, f"generated_melody_{timestamp}.mid")
        wav_path = os.path.join(wav_dir, f"generated_melody_{timestamp}.wav")
        
        # Write the MIDI file.
        pm.write(midi_path)
        
        # Convert MIDI to WAV using FluidSynth via midi2audio.
        fs = FluidSynth(SOUND_FONT)
        fs.midi_to_audio(midi_path, wav_path)
        
        return midi_path, wav_path, program
    except Exception as e:
        return f"Error generating melody: {str(e)}", None, None

if __name__ == "__main__":
    midi_path, wav_path, program = generate_melody()
    if wav_path:
        instrument_name = INSTRUMENT_OPTIONS.get(program, f"Program {program}")
        print(f"Melody generated with {instrument_name} and converted to WAV: {wav_path}")
    else:
        print(midi_path)
