# 🎧 Binaural + Brown Noise Generator

Generate high-quality stereo audio tracks that combine **binaural beats** with **brown noise** for use in sleep, meditation, focus, or relaxation content (e.g., YouTube, personal projects, sound design).

---

## 🧠 What Are Binaural Beats?

Binaural beats are an auditory illusion perceived when two slightly different frequencies are played separately in each ear. The brain interprets the difference as a rhythmic "beat," which may influence brainwave activity.

> ⚠️ **Headphones are required** to experience the intended effect.

---

## 🚀 How It Works

This script generates:
- 🎵 A left ear tone at a base frequency
- 🎵 A right ear tone at base + beat frequency
- 🌊 Brown noise mixed equally in both channels
- 🧪 Output as a stereo `.wav` file, normalized and ready for post-processing or publishing

---

## 🛠️ Parameters You Can Customize

| Parameter        | Description |
|------------------|-------------|
| `base_freq`      | Base frequency for the left channel (Hz). Lower = deeper tone. |
| `beat_freq`      | Frequency difference between left/right ears. Controls the binaural beat. |
| `duration`       | Length of the track in seconds. |
| `brown_volume`   | Volume (0.0–1.0) of brown noise layer. |
| `tone_volume`    | Volume (0.0–1.0) of the binaural sine tones. |
| `filename`       | Output file name (e.g. `"delta_sleep.wav"`). |

---

## 🧘‍♀️ Brainwave States

| Beat Frequency | Brainwave | Effect |
|----------------|-----------|--------|
| 0.5 – 4 Hz     | Delta     | Deep sleep, unconscious states 💤 |
| 4 – 8 Hz       | Theta     | Meditation, lucid dreaming 🌙 |
| 8 – 12 Hz      | Alpha     | Relaxation, stress relief 🌤️ |
| 12 – 30 Hz     | Beta      | Alertness, focus ⚡ |
| 30 – 100 Hz    | Gamma     | High-level cognition 🧠 |

---

## 🔧 Examples

### Deep Sleep (Delta)
```python
generate_binaural_brown_mix(
    base_freq=100,
    beat_freq=1.5,
    duration=1800,
    brown_volume=0.6,
    tone_volume=0.4,
    filename="delta_sleep.wav"
)