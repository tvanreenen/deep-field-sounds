"""
# Binaural Parameters

    base_freq (float): Base frequency (Hz) for the binaural tone. Determines the left ear’s tone.

        • 80 - 120 Hz   - Good for Delta with deep, warm, soft vibe.
        • 120 - 180 Hz  - Good for Theta with natural, mellow, round vibe.
        • 180 - 250 Hz  - Good for Alpha with clear, smooth, balanced vibe.
        • 250 - 400 Hz  - Good for Beta with bright, buzzy, alert vibe.

    beat_freq (float): Frequency difference (Hz) between the tones delivered to each ear.

        • 0.5 - 4 Hz   - Delta. Deep sleep, subconscious.
        • 4 - 8 Hz     - Theta. Meditation, lucid dreaming.
        • 8 - 12 Hz    - Alpha. Relaxation, calm focus, pre-sleep wind down.
        • 12 - 30 Hz   - Beta. Lower end for concentration; higher end for alertness.

    tone_volume (float): Controls the loudness of the binaural tones.

        • 0.0  - No tone (only colored noise plays); useful for testing.
        • 0.3  - Soft, ambient tone; blends with noise (good for sleep).
        • 0.5  - Balanced mix of tone and noise.
        • 0.7  - Dominant tone; suitable for focus or guided listening.
        • 1.0  - Maximum tone prominence.

# Colored Noise Parameters

    noise_exponent (float): Exponent for colored noise, controlling its spectral shape.

        • 0.0 - White noise (flat spectrum).
        • 1.0 - Pink noise (1/f noise).
        • 2.0 - Brown noise (1/f² noise).

    noise_volume (float): Controls the loudness of the colored noise layer.

        • 0.0  - No noise (pure tones only; may sound harsh or sterile).
        • 0.3  - Light ambient noise; tones remain dominant.
        • 0.5  - Balanced mix; clean and suitable for sleep/focus.
        • 0.7  - Noise-dominant; creates a warm, immersive, calming effect (tones feel more “embedded”).
        • 1.0  - Full-on noise; tones may be masked (ideal for deep ambient/sleep).

# Other

    samplerate (int): Determines the number of samples per second used to represent the audio waveform.

        • 44100 Hz - CD quality audio; the standard for most music and audio.
        • 48000 Hz - Commonly used in video, film, and broadcast audio.
        • 96000+ Hz - Used in professional audio production (often overkill for basic use).

"""
import numpy as np
import soundfile as sf
from tqdm import tqdm

def generate_sine_chunk(frequency, duration, samplerate, phase_offset):
    """
    Generate a sine wave chunk with continuous phase ensuring that each generated chunk continues smoothly from the last one, avoiding jumps or pops.

    Parameters:
        frequency (float): Frequency of the sine wave in Hz.
        duration (float): Duration of the chunk in seconds.
        samplerate (int): Number of audio samples per second.
        phase_offset (float): The current phase offset from the previous chunk (in radians).
        
    Returns:
        tuple:
            - signal (np.ndarray): The generated sine wave chunk as a NumPy array.
            - new_phase_offset (float): Updated phase offset to pass into the next chunk.
    """
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    phase = 2 * np.pi * frequency * t + phase_offset
    signal = np.sin(phase)
    # Calculate new phase offset
    phase_increment = (2 * np.pi * frequency * duration) % (2 * np.pi)
    new_phase_offset = (phase_offset + phase_increment) % (2 * np.pi)
    return signal, new_phase_offset

def generate_binaural_beats(base_freq, beat_freq, duration, samplerate):
    """
    Generate binaural beats by creating two sine tones with a frequency difference.
    
    Parameters:
        base_freq (float): Base frequency for the left channel (Hz).
        beat_freq (float): Difference to add for the right channel (Hz).
        duration (float): Duration in seconds.
        samplerate (int): Samples per second.
      
    Returns:
        tuple: (left_channel, right_channel) as numpy.ndarrays.
    """
    left = generate_sine_tone(base_freq, duration, samplerate)
    right = generate_sine_tone(base_freq + beat_freq, duration, samplerate)
    return left, right

def generate_colored_noise(duration, samplerate, exponent):
    """
    Generate colored noise using an FFT-based method.
    
    The power spectrum is scaled as 1/f^(exponent). Typical exponent values:
        - 0.0: White noise (flat spectrum)
        - 1.0: Pink noise (1/f noise)
        - 2.0: Brown noise (1/f² noise)

    Parameters:
        duration (float): Duration in seconds.
        samplerate (int): Samples per second.
        exponent (float): Controls the noise color.
    
    Returns:
        numpy.ndarray: Normalized time-domain noise.
    """
    N = int(duration * samplerate)
    freqs = np.fft.rfftfreq(N, d=1/samplerate)
    freqs[0] = 1.0  # Prevent division by zero
    phases = np.random.uniform(0, 2 * np.pi, len(freqs))
    amplitude = 1 / (freqs ** (exponent / 2))
    spectrum = amplitude * (np.cos(phases) + 1j * np.sin(phases))
    noise = np.fft.irfft(spectrum, n=N)
    return noise / np.max(np.abs(noise))

def mix_signals(signal1, volume1, signal2, volume2):
    """
    Mix two signals with specified volume multipliers.
    
    Parameters:
        signal1 (numpy.ndarray): First signal.
        volume1 (float): Volume multiplier for the first signal.
        signal2 (numpy.ndarray): Second signal.
        volume2 (float): Volume multiplier for the second signal.
      
    Returns:
        numpy.ndarray: The mixed signal.
    """
    return volume1 * signal1 + volume2 * signal2

def stack_channels(left, right):
    """
    Stack left and right channels into a stereo signal.
    
    Parameters:
        left (numpy.ndarray): Left channel signal.
        right (numpy.ndarray): Right channel signal.
      
    Returns:
        numpy.ndarray: 2D stereo signal.
    """
    return np.stack((left, right), axis=-1)

def apply_fade(signal, samplerate, fade_time=0.02):
    """
    Apply a short fade-in and fade-out to a stereo signal.

    Parameters:
        signal (np.ndarray): 2D array with shape (samples, channels).
        samplerate (int): Number of samples per second.
        fade_time (float): Duration of the fade (in seconds).

    Returns:
        np.ndarray: The faded signal.
    """
    fade_samples = int(samplerate * fade_time)
    fade_in = np.linspace(0, 1, fade_samples)[:, np.newaxis] 
    fade_out = np.linspace(1, 0, fade_samples)[:, np.newaxis]
    
    signal[:fade_samples] *= fade_in
    signal[-fade_samples:] *= fade_out
    return signal

def normalize_signal(signal):
    """
    Normalize a signal to ensure its maximum amplitude is 1.
    
    Parameters:
        signal (numpy.ndarray): Input signal.
    
    Returns:
        numpy.ndarray: Normalized signal.
    """
    max_val = np.max(np.abs(signal))
    return signal if max_val == 0 else signal / max_val

def generate_filename(base_freq, beat_freq, noise_exponent, tone_volume, noise_volume, duration):
    """
    Generate a unique filename based on key parameters.
    
    Returns a string of the form:
        layered_mix_<base_freq>Hz_<beat_freq>Hz_exp<noise_exponent>_tv<tone_volume>_nv<noise_volume>_<duration>s.wav
    """
    return (f"layered_mix_{base_freq}Hz_{beat_freq}Hz_exp{noise_exponent}_"
            f"tv{tone_volume}_nv{noise_volume}_{duration}s.wav")

def write_wav_file(filename, samplerate, stereo_signal):
    """
    Write a stereo signal to a WAV file in 16-bit PCM format.
    
    Parameters:
        filename (str): Output filename.
        samplerate (int): Samples per second.
        stereo_signal (numpy.ndarray): 2D array with shape (samples, 2).
    """
    signal_int16 = (stereo_signal * 32767).astype(np.int16)
    write(filename, samplerate, signal_int16)
    print(f"Exported '{filename}'.")

def generate_layered_binaural_noise_chunked(
    base_freq,
    beat_freq,
    tone_volume,
    noise_exponent,
    noise_volume,
    duration,
    samplerate=44100,
    chunk_duration=10,
    filename=None
):
    """
    Generate a layered stereo mix of binaural beats and colored noise in chunks, and write it to a WAV file using soundfile.
    
    Parameters:
        base_freq (float): Base frequency (Hz) for the binaural tone.
        beat_freq (float): Frequency difference (Hz) between ears.
        tone_volume (float): Volume multiplier for the binaural tones.
        noise_exponent (float): Exponent for colored noise.
        noise_volume (float): Volume multiplier for the colored noise.
        duration (float): Total track length in seconds.
        samplerate (int): Sample rate (default 44100).
        chunk_duration (float): Duration (in seconds) for each chunk.
        filename (str): Output filename. If None, it will be generated.
    """
    if filename is None:
        filename = generate_filename(base_freq, beat_freq, noise_exponent, tone_volume, noise_volume, duration)
    
    chunk_size = int(samplerate * chunk_duration)
    total_chunks = int(duration / chunk_duration)

    # Phase offsets for smooth sine continuity
    phase_offset_left = 0.0
    phase_offset_right = 0.0
    
    with sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=2, format='WAV') as f:
        for _ in tqdm(range(total_chunks), desc="Generating Audio", unit="chunk"):
            left_tone, phase_offset_left = generate_sine_chunk(base_freq, chunk_duration, samplerate, phase_offset_left)
            right_tone, phase_offset_right = generate_sine_chunk(base_freq + beat_freq, chunk_duration, samplerate, phase_offset_right)
            colored_noise = generate_colored_noise(chunk_duration, samplerate, noise_exponent)
            left_channel = mix_signals(left_tone, tone_volume, colored_noise, noise_volume)
            right_channel = mix_signals(right_tone, tone_volume, colored_noise, noise_volume)
            stereo_chunk = stack_channels(left_channel, right_channel)
            stereo_chunk = apply_fade(stereo_chunk, samplerate, fade_time=0.02)
            stereo_chunk = normalize_signal(stereo_chunk)
            f.write(stereo_chunk)
    
    print(f"Exported '{filename}'.")

if __name__ == '__main__':
    generate_layered_binaural_noise_chunked(
        base_freq=100, 
        beat_freq=2, 
        tone_volume=0.06, 
        noise_exponent=2, 
        noise_volume=0.8, 
        duration=43200, 
        samplerate=44100, 
        chunk_duration=10
    )
