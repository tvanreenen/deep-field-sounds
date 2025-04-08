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
    Generate a binaural beat with aligned start/end periods.
    
    Parameters:
    - base_freq: Base frequency (Hz) for the left ear
    - beat_freq: Frequency difference (Hz) between left and right ears
    - duration: Duration in seconds
    - samplerate: Samples per second
    """
    print(f"\nGenerating binaural beat with base frequency {base_freq}Hz and beat frequency {beat_freq}Hz:")
    
    # Calculate the period of the beat frequency
    beat_period = 1.0 / beat_freq
    
    # Ensure duration is a multiple of the beat period
    num_periods = int(duration / beat_period)
    adjusted_duration = num_periods * beat_period
    
    print(f"Adjusted duration to {adjusted_duration:.2f}s to align with beat period ({beat_period:.2f}s)")
    
    # Generate time array
    t = np.linspace(0, adjusted_duration, int(samplerate * adjusted_duration), endpoint=False)
    
    # Generate sine waves for left and right channels
    left = np.sin(2 * np.pi * base_freq * t)
    # Add phase shift of pi to the right channel. This ensures the amplitude
    # envelope (beat) starts and ends at its minimum (zero crossing), 
    # which is useful for seamless looping.
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t + np.pi)
    
    # Debug print for signal before normalization
    print(f"Left channel range before normalization: {np.min(left):.2e} to {np.max(left):.2e}")
    print(f"Right channel range before normalization: {np.min(right):.2e} to {np.max(right):.2e}")
    
    # Calculate RMS for each channel
    left_rms = np.sqrt(np.mean(left**2))
    right_rms = np.sqrt(np.mean(right**2))
    print(f"Left channel RMS before normalization: {left_rms:.2e}")
    print(f"Right channel RMS before normalization: {right_rms:.2e}")
    
    # Normalize each channel to a target RMS value
    target_rms = 0.1  # Adjust this value to control overall volume
    
    if left_rms > 0:
        left *= (target_rms / left_rms)
    if right_rms > 0:
        right *= (target_rms / right_rms)
    
    # Stack the normalized channels
    stereo_signal = np.stack((left, right), axis=-1)
    
    # Ensure no clipping
    max_val = np.max(np.abs(stereo_signal))
    if max_val > 1.0:
        stereo_signal /= max_val
    
    # Debug print for final signal
    print(f"Final stereo signal range: {np.min(stereo_signal):.2e} to {np.max(stereo_signal):.2e}")
    print(f"Final left channel RMS: {np.sqrt(np.mean(stereo_signal[:, 0]**2)):.2e}")
    print(f"Final right channel RMS: {np.sqrt(np.mean(stereo_signal[:, 1]**2)):.2e}")

    # Create filename and save the file
    filename = f"binaural_beat_{base_freq}Hz_L_{base_freq + beat_freq}Hz_R_{adjusted_duration:.1f}s.wav"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, filename)
    
    # Scale to 16-bit PCM format
    scaled = np.int16(stereo_signal * 32767)
    print(f"Scaled int16 range: {np.min(scaled)} to {np.max(scaled)}")
    
    write(filename, samplerate, scaled)
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