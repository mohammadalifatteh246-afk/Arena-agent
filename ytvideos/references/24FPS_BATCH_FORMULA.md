# 📐 24 FPS Frame & Micro-Batching Formula Specification

> **Official Mathematical Standard for Arena Cloud Multi-Agent Video Generation**  
> Enables dynamic calculation of frames, micro-batches, timestamps, and storage for any video duration.

---

## 1. Mathematical Formulas

Let:
- $S$ = Total video duration in seconds (float or integer).
- $F$ = Frame rate = **24 Frames Per Second (FPS)**.
- $B_{\text{size}}$ = Micro-batch size limit for Arena Agent = **6 images per batch** (guaranteeing zero timeout under Arena's 10-image ceiling).

### Core Equations:
1. **Total Frames ($T_{\text{frames}}$):**
   $$T_{\text{frames}} = S \times F = 24 \times S$$

2. **Total Micro-Batches ($N_{\text{batches}}$):**
   $$N_{\text{batches}} = \left\lceil \frac{T_{\text{frames}}}{B_{\text{size}}} \right\rceil = \frac{24 \times S}{6} = 4 \times S$$
   *(Golden Rule: Every 1 second of video maps to exactly 4 batches of 6 images).*

3. **Time Duration per Batch ($t_{\text{batch}}$):**
   $$t_{\text{batch}} = \frac{B_{\text{size}}}{F} = \frac{6}{24} = 0.25 \text{ seconds (250 ms)}$$

4. **Time Duration per Frame ($t_{\text{frame}}$):**
   $$t_{\text{frame}} = \frac{1}{F} = \frac{1}{24} \approx 0.04167 \text{ seconds (41.67 ms)}$$

---

## 2. Dynamic Batch Timeline Mapping

For any arbitrary batch index $k \in [1, N_{\text{batches}}]$:

$$\text{Start Frame}(k) = (k - 1) \times 6 + 1$$
$$\text{End Frame}(k) = \min(T_{\text{frames}}, \ k \times 6)$$
$$\text{Start Time}(k) = (k - 1) \times 0.25 \text{ s}$$
$$\text{End Time}(k) = k \times 0.25 \text{ s}$$

### Example Timeline Matrix:
- **Batch 001:** Frames 0001 to 0006 → `00.00s - 00.25s`
- **Batch 002:** Frames 0007 to 0012 → `00.25s - 00.50s`
- **Batch 003:** Frames 0013 to 0018 → `00.50s - 00.75s`
- **Batch 004:** Frames 0019 to 0024 → `00.75s - 01.00s`
- **Batch 005:** Frames 0025 to 0030 → `01.00s - 01.25s`

---

## 3. Multi-Duration Scalability Table

| Duration ($S$) | Total Frames ($24 \times S$) | Batches ($4 \times S$) | Raw PNG Est. | Lossless WebP (67% Cut) | Compiled MP4 (H.264) |
|---|---|---|---|---|---|
| **15 Seconds** | 360 Frames | 60 Batches | 9.8 MB | **3.2 MB** | **~4 MB** |
| **30 Seconds** | 720 Frames | 120 Batches | 19.7 MB | **6.5 MB** | **~8 MB** |
| **60 Seconds** | 1,440 Frames | 240 Batches | 39.4 MB | **13.0 MB** | **~16 MB** |
| **90 Seconds** | 2,160 Frames | 360 Batches | 59.1 MB | **19.4 MB** | **~24 MB** |
| **120 Seconds** (2m) | 2,880 Frames | 480 Batches | 78.8 MB | **26.0 MB** | **~32 MB** |
| **180 Seconds** (3m) | 4,320 Frames | 720 Batches | 118.1 MB | **38.9 MB** | **~48 MB** |
| **300 Seconds** (5m) | 7,200 Frames | 1,200 Batches | 197.0 MB | **65.0 MB** | **~75 MB** |

---

## 4. Execution Tool

The formula is implemented programmatically in:
[`ytvideos/src/batch_calculator.py`](../src/batch_calculator.py)

```bash
# Calculate batches and storage for any duration:
python ytvideos/src/batch_calculator.py --seconds 90
```
