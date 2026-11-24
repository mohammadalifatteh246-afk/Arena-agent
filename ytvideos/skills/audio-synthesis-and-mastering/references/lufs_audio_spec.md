# YouTube Audio Mastering Specification: ITU-R BS.1770-4 & -14 LUFS Standard

## 1. Mathematical Loudness Model
YouTube normalizes all video sound according to the **ITU-R BS.1770-4 / EBU R128** standard.
The Integrated Loudness $L_K$ in Loudness Units Full Scale (LUFS) is computed by passing the signal through a pre-filter (simulating human head acoustic diffraction) followed by a RLB weighting filter (high-pass filter modeling human ear sensitivity):

$$y_i[n] = (x_i * h_{\text{pre}} * h_{\text{RLB}})[n]$$

Mean square energy across channels is accumulated with a dual-gating threshold (absolute gate at -70 LKFS, relative gate at -10 LKFS):

$$z_i = \frac{1}{T} \sum_{n=0}^{N-1} y_i^2[n]$$
$$L_K = -0.691 + 10 \log_{10} \sum_{i} G_i \cdot z_i$$

---

## 2. Invariants for YouTube Video Production

| Criterion | Target Requirement | Consequence of Violation |
|---|---|---|
| **Integrated Loudness** | **-14.0 LUFS** (±1.0 LUFS) | If > -13 LUFS, YouTube applies gain reduction (attenuation). If < -16 LUFS with low peaks, video sounds dangerously quiet against competing uploads. |
| **Max True Peak** | **-1.0 dBTP** | Transcoding to Opus / AAC codecs introduces inter-sample reconstruction overshoots. A ceiling of -1.0 dBTP prevents digital harsh clipping. |
| **Dialogue Anchor** | **-18 to -14 LUFS** | Speech must remain the loudest, most intelligible component in the mix. |
| **Background Music Bed** | **-24 to -22 LUFS** | Music must sit 8–10 dB below dialogue when narration is active. |
| **Music Ducking** | **-6 dB to -10 dB** | Instantaneous sidechain ducking triggers upon voice detection with 50ms attack and 350ms release. |
