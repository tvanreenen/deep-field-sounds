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
    # Get frequencies for the FFT (real-valued signal)
    freqs = np.fft.rfftfreq(n_samples, d=1/sample_rate)
    freqs[0] = 1e-6  # Avoid division by zero at f = 0
    # Create amplitude scaling for a specified exponent (sqrt of PSD scaling)
    amplitude = 1 / (freqs ** (alpha / 2.0))
    # Randomize phase to simulate white noise properties before filtering
    phases = np.exp(2j * np.pi * np.random.rand(len(freqs)))
    spectrum = amplitude * phases
    # Transform back to the time domain using inverse FFT
    signal = np.fft.irfft(spectrum, n=n_samples)
    signal = np.real(signal)
    # Normalize the signal to have a maximum absolute value of 1
    signal /= np.max(np.abs(signal))
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
        filename = os.path.join(script_dir, f"colored_noise_{name}.wav")
        print(f"Generating noise with α={alpha} and writing to {filename}...")
        noise = generate_colored_noise(alpha)
        save_wav(noise, filename)

    print("Done! All files saved.")