---
name: storytelling-and-retention
description: Use when writing, refining, or auditing scripts for automated YouTube videos to guarantee high audience retention, emotional resonance, and viral storytelling over raw animation complexity.
---

# Storytelling and Audience Retention: The BeyondSumi Narrative Engine

## Overview
Viewers do not watch YouTube videos for rendering engines or ray-tracing. They watch for **emotional engagement, tension, and narrative closure**. The BeyondSumi framework proved that even minimalist pencil sketches and code-generated SVGs achieve viral status and full monetization when driven by powerful emotional storytelling.

Use this skill whenever generating video scripts, voiceover narrations, or retention hooks.

---

## The 5 Laws of Viral Scriptwriting

### 1. The Curiosity Gap Hook (0:00 - 0:05)
Never summarize the video at the start. Open with a contradiction, a high-stakes mystery, or an unanswered question that demands closure:
- ❌ *Weak:* "Today we will explore how transformers and attention mechanisms work in machine learning."
- ✅ *Strong:* "In 1440, two Scottish princes were invited to dinner at Edinburgh Castle. They never walked out alive."
- ✅ *Strong:* "A single token enters a 70-billion parameter neural network. In 8 milliseconds, it will either find its context... or be erased forever."

### 2. Story Over Graphics Axiom
If an idea cannot be told compellingly around a campfire with zero visuals, it will fail as a video. The narration script must carry full dramatic momentum independently.

### 3. Pacing & Word Economy
- Standard YouTube conversational speed: **130 to 155 words per minute** (WPM).
- Sentences must vary in length:
  - 1 long sentence (15-20 words) establishing context.
  - 2 short, punchy sentences (4-7 words) delivering impact.
  - Example: *"As the context window expanded to a million tokens, the Softmax denominator diluted the signal. The numbers collapsed. Darkness took over."*

### 4. Humanizing Voiceover Phrasing (Banning AI Clichés)
AI voice models sound robotic primarily because LLMs write with recognizable corporate academic tropes. **Strictly eliminate the following patterns:**

| Banned AI Phrasing | Natural Human Phrasing |
|---|---|
| "In conclusion / In summary..." | "And that's why..." or "Here's the truth:" |
| "It is important to remember that..." | "Look at this:" or "Notice what happened:" |
| "Delve into the fascinating realm of..." | "Let's crack open..." or "Watch how..." |
| "A testament to human ingenuity..." | "It completely changed the game." |
| "Tapestry / beacon / pivotal / paramount" | Everyday concrete nouns & verbs. |

### 5. The Emotional Rollercoaster Curve
Alternate tension and relief every 20-30 seconds:
```
Tension  ▲          [Conflict Spike]                 [Climax]
Level    │               /\                            /\
         │  [Hook]      /  \        [Relief]          /  \
         │   /\        /    \          /\            /    \   [Payoff]
         │  /  \______/      \________/  \__________/      \___________
         └─────────────────────────────────────────────────────────────► Time
```

---

## Practical Script Generation Recipe

When authoring a script for `ytvideos`:

```python
def structure_beyondsumi_script(niche: str, premise: str, target_duration_sec: int) -> dict:
    """
    Constructs a calibrated high-retention script manifest.
    Target WPM: 140 (approx 2.3 words/second).
    """
    total_words = int(target_duration_sec * 2.3)
    
    return {
        "hook_words": int(total_words * 0.12),      # First 5-8 seconds
        "escalation_words": int(total_words * 0.40),# Context & rising stakes
        "climax_words": int(total_words * 0.30),    # Peak conflict/reveal
        "payoff_words": int(total_words * 0.18),    # Resolution & punchline
        "retention_rules": [
            "No greeting or introductory padding",
            "Insert non-verbal breath tokens before emotional reveals",
            "End on a thought-provoking loop rather than a generic subscribe plea"
        ]
    }
```

---

## Anti-Patterns

- **Anti-Pattern 1: The Encyclopedic Readout.** Listing technical specifications or historical dates without emotional stakes. Transform specs into drama (e.g., instead of "HBM bandwidth is 2TB/s", use "Memory was choking so fast the GPU had to freeze and wait").
- **Anti-Pattern 2: Monotone Pacing.** Writing 10 consecutive sentences of identical word length. Break rhythm deliberately to keep the human ear attentive.
