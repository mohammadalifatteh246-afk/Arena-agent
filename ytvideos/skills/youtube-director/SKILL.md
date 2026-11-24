---
name: youtube-director
description: Use when directing, choreographing, or orchestrating an end-to-end automated YouTube video production, coordinating storytelling, visuals, audio synthesis, and editing into a unified viral retention arc.
---

# YouTube Director: Automated Production & Storyboard Orchestration

## Core Invariant
**Story & Retention > Raw Visual Splendor.** A video with basic pencil sketches or code-generated SVGs and an irresistible emotional hook will outperform hyper-realistic 3D animations with a boring narrative every single time.

The Director agent never writes isolated prompts or generates detached assets. Every single frame, sound effect, and narration syllable must be synchronized against the **Audience Retention Curve**.

---

## The 4-Act Retention Framework

```
0:00        0:05                  0:30                       0:50               1:00+
 ┌────────────┬─────────────────────┬──────────────────────────┬──────────────────┐
 │ 3s Hook    │ Context & Tension   │ The Mid-Point Climax     │ Resolution & Payoff
 │ High LUFS  │ Building Stems      │ Maximum Sensory Contrast │ Clean De-escalation
 └────────────┴─────────────────────┴──────────────────────────┴──────────────────┘
```

### 1. Act I: The 0-3s Visceral Hook
- **Visual:** Instant motion, high contrast (Sumi Dark or vivid Sumi Original). No slow fade-ins.
- **Voiceover:** First sentence under 10 words, presenting an urgent paradox or curiosity gap.
- **Audio:** High short-term LUFS (-13 LUFS), immediate punchy SFX (attention whoosh or impact), no silent pauses in the first 3 seconds.

### 2. Act II: Context & Escalating Stakes (3s - 30s)
- **Visual:** Pacing switches to rhythmic sequence (12-16 fps).
- **Voiceover:** Conversational explanation with relatable metaphors.
- **Audio:** Sub-bass ambient drone beds (`base_freq ~ 65Hz`). Voice sits clear at -16 LUFS.

### 3. Act III: The Sensory Climax (30s - 50s)
- **The Pattern Interrupt:** At the 30-40s mark, audience attention naturally drops. The Director **must** enforce an audio/visual pattern interrupt (e.g., cutting background music to absolute silence for 1.2s before a voiceover punchline, or sudden switch from light sketch to dark ink brush).
- **Visual:** Climax frame or rapid sequence.

### 4. Act IV: The Payoff & Loop / CTA (50s - End)
- **Voiceover:** Insight delivery without generic "Like & Subscribe" begging.
- **Audio:** Gentle decay, leading naturally back into the first sentence for Shorts (infinite loop retention).

---

## Production Storyboard Manifest Schema

The Director produces a unified production manifest consumed by the downstream skills:

```json
{
  "project_title": "The Day a Single Token Awoke",
  "target_platform": "youtube_shorts_or_longform",
  "aspect_ratio": "16:9",
  "target_fps": 16,
  "master_lufs": -14.0,
  "max_true_peak_dbtp": -1.0,
  "scenes": [
    {
      "scene_index": 1,
      "timecode": "[0:00 - 0:05]",
      "duration_sec": 5.0,
      "narrative_phase": "hook",
      "art_style": "sumi_dark",
      "visual_prompt": "Haunting Japanese Sumi-e ink wash, a lone glowing vector flickering in total black void, stark contrast, cinematic",
      "voiceover_text": "What happens in the exact microsecond an AI model reads your prompt?",
      "voice_prosody": {"rate": "105%", "pitch": "+5%", "emphasis": ["exact microsecond", "your prompt"]},
      "sound_design": {
        "primary_sfx": "attention_whoosh",
        "bg_bed": "ambient_drone",
        "music_ducking_db": -6.0
      }
    }
  ]
}
```

---

## Director Pre-Flight Checklist

Before approving any production run, verify:
- [ ] First 3 seconds contain no introductory fluff ("Hello guys", "In this video").
- [ ] At least one pattern interrupt exists within every 35-second block.
- [ ] Visual art style matches the emotional tone of the scene (Light for innocence, Dark for tension/mystery).
- [ ] Voiceover and SFX have explicit millisecond timestamps so visual transitions hit on the beat.

---

## Anti-Patterns & Rationalizations

| Rationalization | Reality |
|---|---|
| "The visual is so pretty, we can let it hold for 10 seconds without narration." | Viewer retention plummets after 3.5 seconds of static visual motion. Cut or animate. |
| "Let's put the channel intro logo at 0:02." | 45% of viewers swipe away when an intro logo appears. Hook first, logo never. |
| "The audio can just be a stock YouTube lo-fi track." | Monotonous background music causes auditory fatigue. Procedural audio with dynamic ducking maintains engagement. |
