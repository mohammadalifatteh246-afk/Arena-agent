# BeyondSumi Visual Style Prompting Matrix & Token Lexicon

This reference guide maps narrative moods directly into LMArena prompt tokens to guarantee stylistic consistency across multi-scene productions.

---

## 1. Style Matrix Mapping

| Narrative Mood | Target Art Style | Recommended FPS | LMArena Modifier Signature |
|---|---|---|---|
| **Inspirational, High-Concept, Deep Tech** | `sumi_original` | 16 - 24 FPS | `vibrant Japanese digital anime, Makoto Shinkai atmosphere, luminous particle lighting, vivid colors, cinematic 16:9` |
| **Childhood, Innocence, Morals, Bedtime** | `sumi_light` | 8 - 12 FPS | `soft pencil sketch rendering, charcoal hatching on handmade paper, pastel watercolor wash, nostalgic storybook, warm light` |
| **Horror, Crime, Dystopia, High Mystery** | `sumi_dark` | 12 - 16 FPS | `traditional Japanese Sumi-e brush ink wash, stark chiaroscuro, heavy ink splatters, crimson accents, atmospheric fog` |
| **Mathematics, Neural Architecture, Code** | `svg_code` | 16 - 24 FPS | `pure vector geometric paths, neon cybernetic accents, mathematical grid, clean SVG rendering` |

---

## 2. Character Consistency Invariant
When carrying an animated character across multiple scenes:
1. Define **3 immutable anchors**:
   - Primary garment (e.g., *"faded indigo kimono with frayed collar"*).
   - Hair silhouette (e.g., *"disheveled jet-black spiky hair with a white streak across right temple"*).
   - Eye color and expression (e.g., *"piercing amber eyes with focused gaze"*).
2. Never alter the anchor string between scene prompts. Append dynamic context *after* the immutable anchors.
