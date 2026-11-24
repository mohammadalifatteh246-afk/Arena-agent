---
name: audio-synthesis-and-mastering
description: Use when generating, humanizing, testing, tuning pitch/volume, or mastering voiceover and procedural audio for YouTube videos according to the -14 LUFS standard and zero-copyright-strike invariants.
---

# Audio Synthesis, Humanization & YouTube Mastering Engine

## Overview
Audio is 50% of the video experience. Viewers will tolerate a low-resolution sketch, but they will click off instantly if the voiceover sounds robotic, muddy, piercing, or quiet.

This skill governs:
1. **TTS Voice Humanization & Prosody Tuning** (SSML, non-verbal cues, breath pauses, emphasis).
2. **Audio Quality Evaluation & Regeneration Loop** (detecting unnatural cadences and iteratively re-synthesizing).
3. **Procedural Background Sound Design** (100% royalty-free algorithmic music and SFX via Python).
4. **YouTube Mastering Standard** (**-14 Integrated LUFS**, **-1.0 dBTP True Peak**).

---

## 1. The Voice Humanization Protocol

Neural TTS models default to robotic monotony if fed raw, unpunctuated text. Apply these four layers before audio rendering:

### Layer A: SSML & Non-Verbal Tokens
Inject breathing spaces and dynamic pauses:
```xml
<speak>
  <prosody rate="98%" pitch="-1st">
    In 1440, two brothers arrived at the castle gates.
  </prosody>
  <break time="450ms"/>
  [breath]
  <emphasis level="strong">Neither of them</emphasis> knew what was waiting behind those doors.
</speak>
```

### Layer B: Inflection & Cadence Rules
- **Question Lifts:** Questions must end with a rising pitch contour (`+2st` to `+4st`).
- **Dramatic Drops:** Climax reveals drop pitch slightly (`-2st`) and slow down by 10% to convey gravitas.
- **Micro-Breaks:** Replace standard commas with `<break time="250ms"/>` to avoid rushed clauses.

---

## 2. Audio Quality Evaluation & Regeneration Loop

```
  ┌───────────────┐
  │ Generated WAV │
  └───────┬───────┘
          │
          ▼
  ┌──────────────────────────────────┐
  │ Run Acoustic Clarity & Cadence   │
  │ Check (Word Duration / Silence)  │
  └───────┬──────────────────────────┘
          │
      Fail? ────► [Adjust SSML rate/pitch tags & re-synthesize]
          │
      Pass!
          ▼
  ┌──────────────────────────────────┐
  │ Normalize to -14 LUFS / -1.0 dBTP│
  └──────────────────────────────────┘
```

### Regeneration Triggers:
1. **Unnatural Word Rushes:** If average syllable duration drops below 80ms, the engine flagged an unnatural rush -> inject `<break>` tag and regenerate.
2. **Monotone Flatness:** If pitch variance across an emotional clause is < 5%, add `<prosody pitch="+/-3st">` tags and regenerate.
3. **Clipping:** If True Peak exceeds -0.5 dBFS, lower gain by 3dB and re-evaluate.

---

## 3. Algorithmic Procedural Audio Synthesis (Zero Copyright Risk)

To eliminate any chance of YouTube Content ID strikes, synthesize background soundscapes directly using Python's standard `wave` and `math` libraries:

```python
import math
import struct
import wave

def synthesize_tension_riser(output_path: str, duration_sec: float = 6.0, sample_rate: int = 44100):
    """Synthesizes an exponential cinematic tension riser with zero external audio assets."""
    num_samples = int(sample_rate * duration_sec)
    samples = []
    phase = 0.0
    start_freq, end_freq = 60.0, 480.0

    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration_sec
        # Exponential frequency curve
        freq = start_freq * math.pow(end_freq / start_freq, progress)
        phase += 2 * math.pi * freq / sample_rate
        
        # Exponential volume swell
        envelope = math.pow(progress, 1.8)
        val = math.sin(phase) * envelope * 0.8
        clamped = max(-32767, min(32767, int(val * 32767)))
        samples.append(clamped)

    with wave.open(output_path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(struct.pack(f"<{len(samples)}h", *samples))
```

---

## 4. YouTube Audio Mastering Standards

| Parameter | Mandatory Value | Purpose |
| :--- | :--- | :--- |
| **Integrated Loudness** | **-14.0 LUFS** (±1.0 LUFS) | Matches YouTube Loudness Normalization. Prevents YouTube turning down audio or sounding weak. |
| **Max True Peak** | **-1.0 dBTP** | Leaves headroom for lossy transcoding (Opus/AAC) to eliminate inter-sample digital distortion. |
| **Dialogue Sitting** | **-18 to -14 LUFS** | Voiceover remains clearly intelligible over background beds at all times. |
| **Music Bed Ducking** | **-6 dB to -10 dB** | When voiceover is active, background music dips by 6-10dB automatically. |

---

## Audio Production Checklist

- [ ] Voiceover contains no robotic glitches or unnatural word rushing.
- [ ] Breathing sounds and micro-pauses inserted at natural punctuation points.
- [ ] Background music beds synthesized algorithmically or verified 100% royalty-free.
- [ ] Final mix mastered to -14 LUFS with True Peak ≤ -1.0 dBTP.
