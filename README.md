# 🎧 Sound Generator

Generate high-quality audio tracks including **colored noise** and **binaural beats** for use in sleep, meditation, focus, or relaxation content (e.g., YouTube, personal projects, sound design).

## Project Setup

1. Install the correct Python version
```
pyenv install $(cat .python-version)
pyenv local $(cat .python-version)
```

2. Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies
```
pip install -r requirements.txt
```

## 🎨 Colored Noise Generator

The colored noise generator creates a spectrum of noise types with different frequency characteristics, from bright white noise to deep brown noise.

### What is Colored Noise?

Colored noise refers to random signals with specific power spectral density characteristics. The "color" refers to how the power is distributed across frequencies:

- **White Noise (α=0.0)**: Equal power at all frequencies
- **Pink Noise (α=1.0)**: Equal power per octave (1/f)
- **Brown Noise (α=2.0)**: Power increases with decreasing frequency (1/f²)

Between these primary colors, we've created intermediate colors:
- **Silver Noise (α=0.3)**: Between white and pink
- **Pearl Noise (α=0.6)**: Closer to pink than white
- **Coral Noise (α=1.3)**: Between pink and brown
- **Copper Noise (α=1.6)**: Closer to brown than pink

### Understanding Frequency Distribution

In audio, an octave is a doubling of frequency. For example:
- 20 Hz to 40 Hz is one octave
- 40 Hz to 80 Hz is another octave
- 80 Hz to 160 Hz is another octave

Different colored noises distribute power across these octaves in distinct ways:

#### White Noise (α=0.0)
- Has equal power at each individual frequency
- The power at 20 Hz equals the power at 40 Hz equals the power at 80 Hz
- However, since there are twice as many frequencies in each higher octave, the total power in each octave doubles as frequency increases
- This makes white noise sound very bright and harsh
- Mathematical relationship: Power(f) = constant

#### Pink Noise (α=1.0)
- Has equal total power in each octave
- The power in the 20-40 Hz octave equals the power in the 40-80 Hz octave equals the power in the 80-160 Hz octave
- To achieve this, the power at individual frequencies must decrease as frequency increases
- This matches how human hearing perceives sound (roughly logarithmic)
- Mathematical relationship: Power(f) = constant / f
- Often described as "1/f noise" - power is inversely proportional to frequency

#### Brown Noise (α=2.0)
- Power increases with decreasing frequency
- Has even more low-frequency content than pink noise
- Creates a deep, rumbling sound
- Mathematical relationship: Power(f) = constant / f²

### How the Script Works

The generator uses a sophisticated approach to create colored noise:

1. **Start with White Noise**: Generate random samples in the time domain
2. **Transform to Frequency Domain**: Use FFT to get the frequency spectrum
3. **Apply Power Law Scaling**: Modify the spectrum according to the desired color
4. **Transform Back to Time Domain**: Use inverse FFT to get the final signal
5. **Normalize for Consistent Volume**: Ensure all colors have similar perceived loudness

### Power Law Scaling Formula

For colors with α > 1.0 (pink to brown), we use a non-linear scaling formula to gradually reduce the effective alpha for darker colors (> 1.0) to prevent them from becoming too quiet:

```
effective_alpha = alpha * (1.0 - 0.25 * (alpha - 1.0))
```

Example scaling:
```
Original α    Effective α    Result
0.0  →  0.0  (white noise - unchanged)
0.3  →  0.3  (silver noise - unchanged)
0.6  →  0.6  (pearl noise - unchanged)
1.0  →  1.0  (pink noise - unchanged)
1.3  →  1.23 (coral noise - slightly reduced)
1.6  →  1.45 (copper noise - moderately reduced)
2.0  →  1.5  (brown noise - significantly reduced)
```

### Interpreting Debug Output

The script includes debug print statements that help you understand what's happening at each stage of the noise generation process. Here's how to interpret them:

```
Generating pink noise (α=1.0):
Spectrum magnitude range: 1.23e-01 to 2.45e+00
Signal range before normalization: -3.45e+00 to 3.67e+00
Current RMS before normalization: 1.23e+00
Final signal range: -8.12e-01 to 8.34e-01
Final RMS: 1.00e-01
Scaled int16 range: -26623 to 27341
```

#### What Each Line Means:

1. **Spectrum magnitude range**: Shows the range of values in the frequency domain after applying the power law scaling. Higher values indicate more power in certain frequency bands.

2. **Signal range before normalization**: Shows the min/max values of the time-domain signal before any normalization. These values can vary widely depending on the noise color.

3. **Current RMS before normalization**: The Root Mean Square value of the signal before normalization. RMS is a measure of the average power of the signal.

4. **Final signal range**: The min/max values after normalization. These should be between -1.0 and 1.0, with values closer to ±1.0 indicating a more dynamic signal.

5. **Final RMS**: The target RMS value (0.1) that all signals are normalized to for consistent volume.

6. **Scaled int16 range**: The final values scaled to 16-bit PCM format (range: -32768 to 32767). Values closer to ±32767 indicate a louder signal.

#### What to Look For:

- **White noise** typically has a wider spectrum magnitude range and more uniform distribution.
- **Pink noise** shows a gradual decrease in spectrum magnitude as frequency increases.
- **Brown noise** shows a steeper decrease in spectrum magnitude, with most power concentrated in lower frequencies.
- If the **Final RMS** is significantly lower than 0.1, the signal might be too quiet.
- If the **Scaled int16 range** doesn't approach ±32767, the signal might be too quiet.

## 🧠 Binaural Beats

Binaural beats are an auditory illusion perceived when two slightly different frequencies are played separately in each ear. The brain interprets the difference as a rhythmic "beat," which may influence brainwave activity.

> ⚠️ **Headphones are required** to experience the intended effect.

### How It Works

This script generates:
- 🎵 A left ear tone at a base frequency
- 🎵 A right ear tone at base + beat frequency
- 🌊 Brown noise mixed equally in both channels
- 🧪 Output as a stereo `.wav` file, normalized and ready for post-processing or publishing

### Brainwave States

| Beat Frequency | Brainwave | Effect |
|----------------|-----------|--------|
| 0.5 – 4 Hz     | Delta     | Deep sleep, unconscious states 💤 |
| 4 – 8 Hz       | Theta     | Meditation, lucid dreaming 🌙 |
| 8 – 12 Hz      | Alpha     | Relaxation, stress relief 🌤️ |
| 12 – 30 Hz     | Beta      | Alertness, focus ⚡ |
| 30 – 100 Hz    | Gamma     | High-level cognition 🧠 |