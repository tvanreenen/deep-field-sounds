import numpy as np
from scipy.io.wavfile import write
import os

def generate_colored_noise(alpha, duration_sec=5, sample_rate=44100):
    """
    Generate colored noise with a given spectral exponent alpha.
    
    Parameters:
        alpha (float): Spectral exponent (0 = white, 1 = pink, 2 = brown)
        duration_sec (int): Duration in seconds
        sample_rate (int): Sampling rate in Hz  
    
    Returns:
      numpy.ndarray: 16-bit PCM formatted noise.
    """
    n_samples = int(duration_sec * sample_rate)
    
    # Generate white noise in time domain
    white = np.random.normal(0, 1, n_samples)
    
    # Transform to frequency domain
    spectrum = np.fft.rfft(white)
    
    # Get frequencies for the FFT
    freqs = np.fft.rfftfreq(n_samples, d=1/sample_rate)
    
    # Avoid division by zero and limit the scaling for very low frequencies
    min_freq = 20.0  # 20 Hz minimum
    freqs = np.maximum(freqs, min_freq/sample_rate)
    
    # Create a smoother power law scaling
    # Base scaling factor that increases with alpha
    base_scale = 1.0
    
    # For alpha > 1.0, gradually reduce the scaling to prevent too much low-frequency dominance
    if alpha > 1.0:
        # Reduce the effective alpha for higher values to prevent extreme low-frequency dominance
        effective_alpha = alpha * (1.0 - 0.25 * (alpha - 1.0))
    else:
        effective_alpha = alpha
    
    # Apply the power law scaling
    spectrum *= base_scale / (freqs ** (effective_alpha/2))
    
    # Add a high-pass filter to remove DC and very low frequencies
    highpass = freqs > (20.0/sample_rate)  # 20 Hz cutoff
    spectrum *= highpass
    
    # Debug print for spectrum values
    print(f"Spectrum magnitude range: {np.min(np.abs(spectrum[1:])):.2e} to {np.max(np.abs(spectrum[1:])):.2e}")
    
    # Transform back to time domain
    signal = np.fft.irfft(spectrum, n=n_samples)
    
    # Debug print for signal before normalization
    print(f"Signal range before normalization: {np.min(signal):.2e} to {np.max(signal):.2e}")
    
    # Add a small amount of white noise to ensure there's always some variation
    signal += np.random.normal(0, 0.001, n_samples)
    
    # Normalize RMS (Root Mean Square) to a target value
    target_rms = 0.1  # Adjust this value to control overall volume
    current_rms = np.sqrt(np.mean(signal**2))
    print(f"Current RMS before normalization: {current_rms:.2e}")
    
    if current_rms > 0:
        signal *= (target_rms / current_rms)
    
    # Ensure no clipping
    max_val = np.max(np.abs(signal))
    if max_val > 1.0:
        signal /= max_val
    
    # Debug print for final signal
    print(f"Final signal range: {np.min(signal):.2e} to {np.max(signal):.2e}")
    print(f"Final RMS: {np.sqrt(np.mean(signal**2)):.2e}")
    
    return signal

def save_wav(signal, filename, sample_rate=44100):
    """
    Scale the normalized signal to 16-bit PCM format and writes it to a WAV file.
    
    Parameters:
        signal (numpy.ndarray): Normalized signal array with values between -1 and 1
        filename (str): Output filename for the WAV file
        sample_rate (int): Sampling rate in Hz (default: 44100)
    """
    scaled = np.int16(signal * 32767)
    # Debug print for scaled values
    print(f"Scaled int16 range: {np.min(scaled)} to {np.max(scaled)}")
    write(filename, sample_rate, scaled)

if __name__ == '__main__':
    noise_colors = {
        0.0: 'white',
        0.3: 'silver',
        0.6: 'pearl',
        1.0: 'pink',
        1.3: 'coral',
        1.6: 'copper',
        2.0: 'brown'
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for alpha, name in noise_colors.items():
        print(f"\nGenerating {name} noise (α={alpha}):")
        filename = os.path.join(script_dir, f"colored_noise_{name}.wav")
        noise = generate_colored_noise(alpha)
        save_wav(noise, filename)

    print("\nDone! All files saved.")