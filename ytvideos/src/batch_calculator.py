#!/usr/bin/env python3
"""
Dynamic 24 FPS Batch & Frame Calculator for Arena Agent Mode.
Allows Arena to automatically calculate frames, batches, timestamps, and storage
for any arbitrary duration in seconds.
"""

import math
import json
import argparse


def calculate_video_specs(seconds: float, fps: int = 24, batch_size: int = 6) -> dict:
    """
    Core Mathematical Formulas:
      Total Frames (T_frames)  = Seconds * FPS
      Batches Per Second (B_ps)= FPS / Batch_Size
      Total Batches (N_batch)  = ceil(T_frames / Batch_Size)
      Time per Batch           = Batch_Size / FPS (e.g. 6 / 24 = 0.25s)
      Time per Frame           = 1 / FPS (e.g. 1 / 24 = 0.04167s)
    """
    total_frames = int(math.ceil(seconds * fps))
    batches_per_sec = fps / batch_size
    total_batches = int(math.ceil(total_frames / batch_size))
    time_per_batch = round(batch_size / fps, 4)
    time_per_frame = round(1.0 / fps, 5)

    # Storage estimates
    raw_png_mb = round((total_frames * 28.0) / 1024.0, 2)
    lossless_webp_mb = round((total_frames * 9.2) / 1024.0, 2)
    size_savings_pct = round(((raw_png_mb - lossless_webp_mb) / max(0.01, raw_png_mb)) * 100, 1)

    # Batch timeline preview (first 4 and last 2)
    sample_schedule = []
    for k in range(1, min(5, total_batches + 1)):
        start_t = round((k - 1) * time_per_batch, 2)
        end_t = round(k * time_per_batch, 2)
        start_f = (k - 1) * batch_size + 1
        end_f = min(total_frames, k * batch_size)
        sample_schedule.append({
            "batch_id": k,
            "time_window": f"{start_t:05.2f}s - {end_t:05.2f}s",
            "frame_range": f"Frame {start_f:04d} to {end_f:04d}",
            "image_count": end_f - start_f + 1
        })

    return {
        "inputs": {
            "duration_seconds": seconds,
            "target_fps": fps,
            "batch_size_limit": batch_size
        },
        "formulas": {
            "total_frames": f"{seconds} * {fps} = {total_frames}",
            "total_batches": f"ceil({total_frames} / {batch_size}) = {total_batches}",
            "batches_per_second": f"{fps} / {batch_size} = {batches_per_sec}",
            "seconds_per_batch": f"{batch_size} / {fps} = {time_per_batch}s (250 ms)",
            "seconds_per_frame": f"1 / {fps} = {time_per_frame}s (41.67 ms)"
        },
        "totals": {
            "total_frames": total_frames,
            "total_batches": total_batches,
            "batches_per_second": batches_per_sec
        },
        "storage_budget": {
            "raw_png_estimated_mb": raw_png_mb,
            "lossless_webp_optimized_mb": lossless_webp_mb,
            "bandwidth_saved_pct": f"{size_savings_pct}%"
        },
        "first_batches_preview": sample_schedule
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate 24 FPS Batches for any Video Duration")
    parser.add_argument("--seconds", type=float, default=60.0, help="Duration in seconds")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    parser.add_argument("--batch-size", type=int, default=6, help="Images per Arena batch")
    args = parser.parse_args()

    specs = calculate_video_specs(args.seconds, args.fps, args.batch_size)
    print(json.dumps(specs, indent=2))


if __name__ == "__main__":
    main()
