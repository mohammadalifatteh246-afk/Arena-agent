# Video Assembly & Kinetic Subtitle Specifications

## 1. Kinetic Caption Guidelines
- **Cognitive Load Minimization:** Only 3 to 5 words displayed on screen simultaneously.
- **Visual Position:** Centered horizontally, vertically positioned at $y = 80\%$ (safe zone for mobile cards, shorts buttons, and UI chrome).
- **Active Word Highlighting:**
  - Inactive Words: `#FFFFFF` (White) with 2px `#000000` outline shadow.
  - Active Word (hit by speech beat): `#FACC15` (Vibrant Amber/Yellow) or `#22D3EE` (Electric Cyan) with $1.1\times$ scale pop.

---

## 2. Audio-Visual Sidechain Ducking
- When dialogue waveform is detected above $-35 \text{ dBFS}$, background audio bed must automatically duck by $-6 \text{ dB}$ to $-10 \text{ dB}$.
- Attack Time: $40 \text{ ms}$ (smooth fade without clicking).
- Release Time: $350 \text{ ms}$ (natural musical return).
