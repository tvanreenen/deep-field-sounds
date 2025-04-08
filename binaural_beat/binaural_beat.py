import numpy as np
from scipy.io.wavfile import write
import os

def generate_binaural_beat(
    base_freq=200, 
    beat_freq=4, 
    duration=5,
    samplerate=44100
):
    """
    Generate a stereo WAV file with a binaural beat.
    
    Parameters:
    - base_freq: Base frequency (Hz) for the left ear
    - beat_freq: Frequency difference (Hz) between left and right ears
    - duration: Duration in seconds
    - samplerate: Samples per second
    """
    
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)
    
    stereo_signal = np.stack((left, right), axis=-1)
    stereo_signal = stereo_signal / np.max(np.abs(stereo_signal))  # Normalize

    filename = f"binaural_beat_{base_freq}Hz_L_{base_freq + beat_freq}Hz_R_{duration}s.wav"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, filename)
    write(filename, samplerate, (stereo_signal * 32767).astype(np.int16))

    print(f"Generated {filename}")

if __name__ == '__main__':
    # Delta wave (0.5-4 Hz) - Deep sleep
    # Lower base freq (100 Hz) for a deeper, more soothing tone
    generate_binaural_beat(base_freq=100, beat_freq=2)
    
    # Theta wave (4-8 Hz) - Meditation
    # Slightly higher base freq (150 Hz) maintains clarity while staying gentle
    generate_binaural_beat(base_freq=150, beat_freq=6)
    
    # Alpha wave (8-12 Hz) - Relaxation
    # Medium base freq (200 Hz) balances presence and comfort
    generate_binaural_beat(base_freq=200, beat_freq=10)
    
    # Beta wave (12-30 Hz) - Focus
    # Higher base freq (250 Hz) increases alertness while remaining pleasant
    generate_binaural_beat(base_freq=250, beat_freq=20)
    
    # Gamma wave (30-100 Hz) - High cognition
    # Highest base freq (300 Hz) promotes heightened awareness
    generate_binaural_beat(base_freq=300, beat_freq=40)

    print("\nDone! All files saved.")