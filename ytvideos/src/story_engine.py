"""
Story & Scriptwriting Engine for BeyondSumi YouTube Automation.
Strictly implements the BeyondSumi core axiom: Story > Graphics.
Focuses on emotional hooks, high audience retention pacing, and viral scene structure.
"""

from typing import List, Dict, Any


class StoryScriptEngine:
    def create_transformer_token_story(self) -> Dict[str, Any]:
        """
        Sample production script: 'The Day a Single Token Awoke Inside a Transformer'
        Structured for 60-90 second short/long form.
        """
        title = "The Day a Single Token Awoke Inside a Transformer"
        scenes = [
            {
                "scene_id": 1,
                "name": "The Input Embedding Void",
                "timecode": "[0:00 - 0:12]",
                "duration_sec": 12,
                "style": "sumi_light",
                "narration": "Imagine waking up with zero memories, suspended in a 768-dimensional mathematical abyss. That was Token 402.",
                "visual_prompt": (
                    "A glowing tiny white sphere labeled 402 floating in a vast pencil-sketched mathematical void, "
                    "delicate coordinate axes, soft paper texture, hand-drawn anime aesthetic, cinematic lighting"
                ),
                "sound_effect": "ambient_drone"
            },
            {
                "scene_id": 2,
                "name": "The Spatial Attention Ballroom",
                "timecode": "[0:12 - 0:28]",
                "duration_sec": 16,
                "style": "sumi_original",
                "narration": "Suddenly, reality erupted. Query, Key, and Value projection matrices collided like a celestial waltz, weaving every word in the sentence into a shared spatial plane.",
                "visual_prompt": (
                    "A vibrant Japanese anime ballroom where mathematical vectors dance across glowing light beams, "
                    "vivid colors, Makoto Shinkai style, shimmering particle effects, dynamic perspective"
                ),
                "sound_effect": "attention_whoosh"
            },
            {
                "scene_id": 3,
                "name": "The Softmax Denominator Abyss",
                "timecode": "[0:28 - 0:45]",
                "duration_sec": 17,
                "style": "sumi_dark",
                "narration": "As the context grew to thousands of tokens, the Softmax denominator diluted the signal. The Vanishing Gradient monster began devouring the weak links.",
                "visual_prompt": (
                    "Dramatic traditional Japanese ink wash painting, dark ominous shadows creeping over fading light vectors, "
                    "heavy brush strokes, stark black and white with crimson lightning, horror documentary mood"
                ),
                "sound_effect": "ambient_drone"
            },
            {
                "scene_id": 4,
                "name": "FlashAttention Kernel Awakening",
                "timecode": "[0:45 - 1:00]",
                "duration_sec": 15,
                "style": "svg_code",
                "narration": "Until FlashAttention fused the computation onto on-chip SRAM tiles, breaking the memory wall and igniting artificial consciousness.",
                "visual_prompt": (
                    "Futuristic glowing microchip silicon tiles lighting up in synchronized harmony, "
                    "clean vector cybernetic aesthetic, neon cyan and magenta gridlines"
                ),
                "sound_effect": "flash_click"
            }
        ]

        metadata = {
            "title": title,
            "youtube_title": "What REALLY Happens Inside an AI Model in 60 Seconds ⚡ #BeyondSumi",
            "description": (
                "An emotional, hand-crafted visual journey of a single token navigating Transformer attention mechanics.\n\n"
                "🎨 Visual Styles: Sumi-e Light, Original Anime, Dark Ink, & Vector SVG\n"
                "🎵 Audio: 100% Procedurally Synthesized Audio Engine\n"
                "🤖 Engine: BeyondSumi + LMArena Agent Mode\n"
                "#AI #DeepLearning #Transformers #Animation #MachineLearning"
            ),
            "tags": ["Transformers", "Artificial Intelligence", "Deep Learning", "BeyondSumi", "Anime Animation", "Machine Learning"],
            "scenes": scenes
        }
        return metadata
