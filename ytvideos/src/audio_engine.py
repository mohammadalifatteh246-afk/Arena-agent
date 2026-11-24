"""
Algorithmic Python Audio Synthesis Engine for BeyondSumi YouTube Automation.
Generates 100% royalty-free, procedural soundscapes using Python standard library (wave, math, struct).
Zero external dependencies, zero copyright strike risk.
"""

import math
import struct
import wave
from pathlib import Path


class ProceduralAudioEngine:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def generate_ambient_drone(self, duration_sec: float = 10.0, base_freq: float = 65.4) -> bytes:
        """Generates deep, subtle ambient sci-fi / emotional drone (C2 chord + low harmonics)."""
        num_samples = int(self.sample_rate * duration_sec)
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            # Dual oscillator with slow frequency modulation (LFO)
            lfo = 1.0 + 0.05 * math.sin(2 * math.pi * 0.2 * t)
            osc1 = math.sin(2 * math.pi * base_freq * lfo * t)
            osc2 = 0.5 * math.sin(2 * math.pi * (base_freq * 1.5) * t)
            osc3 = 0.25 * math.sin(2 * math.pi * (base_freq * 2.0) * t)
            
            # Gentle fade in / fade out envelope
            env = 1.0
            fade_samples = int(self.sample_rate * 1.0)
            if i < fade_samples:
                env = i / fade_samples
            elif i > num_samples - fade_samples:
                env = (num_samples - i) / fade_samples

            val = (osc1 + osc2 + osc3) / 1.75 * env
            # Clamp to 16-bit PCM integer
            clamped = max(-32767, min(32767, int(val * 24000)))
            samples.append(clamped)
        return struct.pack(f"<{len(samples)}h", *samples)

    def generate_attention_whoosh(self, duration_sec: float = 1.5, start_freq: float = 120.0, end_freq: float = 880.0) -> bytes:
        """Generates spatial attention transition whoosh (exponential frequency sweep)."""
        num_samples = int(self.sample_rate * duration_sec)
        samples = []
        phase = 0.0
        for i in range(num_samples):
            t = i / self.sample_rate
            progress = t / duration_sec
            current_freq = start_freq * math.pow(end_freq / start_freq, progress)
            phase += 2 * math.pi * current_freq / self.sample_rate
            
            # Smooth bell curve envelope
            env = math.sin(math.pi * progress)
            val = math.sin(phase) * env
            clamped = max(-32767, min(32767, int(val * 28000)))
            samples.append(clamped)
        return struct.pack(f"<{len(samples)}h", *samples)

    def generate_flash_click(self, duration_sec: float = 0.2) -> bytes:
        """Generates sharp acoustic / high-tech memory tile click."""
        num_samples = int(self.sample_rate * duration_sec)
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            decay = math.exp(-35.0 * t)
            val = math.sin(2 * math.pi * 1800.0 * t) * decay
            clamped = max(-32767, min(32767, int(val * 30000)))
            samples.append(clamped)
        return struct.pack(f"<{len(samples)}h", *samples)

    def save_wav(self, raw_pcm: bytes, filepath: Path):
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(filepath), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(raw_pcm)
        return filepath


if __name__ == "__main__":
    engine = ProceduralAudioEngine()
    drone = engine.generate_ambient_drone(5.0)
    out = engine.save_wav(drone, Path("test_drone.wav"))
    print(f"Generated test audio: {out}")
