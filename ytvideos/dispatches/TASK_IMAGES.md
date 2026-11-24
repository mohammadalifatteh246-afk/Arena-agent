# 🎨 ARENA AGENT SESSION 1: 24 FPS VISUAL FRAME & IMAGE ENGINE

- **Dispatched By:** Google Antigravity (`ytvideos` engine)
- **Target Branch:** `arena/ytvideo-api-backend-images`
- **Execution Target:** Arena Cloud Agent Sandbox (`arena.ai/agent`)
- **Mission:** High-Resolution Frame Generation & Lossless Compression
- **Frame Rate:** 24 Frames Per Second (FPS)

---

## 🎯 Production Objective
Generate the visual scene illustrations for "How The Internet ACTUALLY Works: APIs & Backends". 
After generating the frames, run **Lossless Image Optimization** (`lossless WebP` or `optimized PNG level 9`) to reduce total payload size by 30-50% with **zero visual quality loss**.

---

## 🖼️ Scene Visual Directives

### Scene 1: The Invisible Messenger [0:00 - 0:08]
- **Target File:** `ytvideos/assets/images/scene_01_api_hook.png`
- **Art Style:** `sumi_dark` (Traditional Japanese ink brush with vibrant neon cyan accents)
- **Prompt:**
  ```
  A glowing smartphone screen floating in dark void, a hand tapping an illuminated 'Order Pizza' button,
  electric cyan and magenta light data pulses bursting out from the screen into a planetary fiber-optic highway,
  traditional Japanese Sumi-e ink wash background, dynamic chiaroscuro, cinematic composition, 8k resolution --ar 16:9
  ```

### Scene 2: Restaurant Dining Room vs Cybernetic Kitchen [0:08 - 0:24]
- **Target File:** `ytvideos/assets/images/scene_02_backend_kitchen.png`
- **Art Style:** `sumi_original` (Vibrant anime digital aesthetic, Studio Ghibli style)
- **Prompt:**
  ```
  A split-screen cross-section illustration: on the left a warm quiet luxury restaurant dining table with a menu,
  on the right an energetic high-tech cybernetic kitchen filled with glowing database vaults, server racks,
  and holographic order tickets, Makoto Shinkai vibrant lighting, atmospheric particles, highly detailed, masterpiece --ar 16:9
  ```

### Scene 3: REST vs GraphQL vs WebSockets in Action [0:24 - 0:44]
- **Target File:** `ytvideos/assets/images/scene_03_protocols_action.png`
- **Art Style:** `svg_code` & digital vector anime
- **Prompt:**
  ```
  A kinetic technical diagram rendered in high-end vector anime style: a glowing JSON data envelope traveling between client and server,
  transitioning into a pulsing real-time radar screen tracking a live delivery bike, clean cybernetic typography, neon accents, crisp 8k --ar 16:9
  ```

### Scene 4: The Intelligent Global Engine [0:44 - 1:00]
- **Target File:** `ytvideos/assets/images/scene_04_global_engine.png`
- **Art Style:** `sumi_dark` transitioning to vivid anime
- **Prompt:**
  ```
  A wide-angle cinematic view of a solitary illuminated microchip expanding into a vast interconnected glowing global server constellation,
  intricate motherboard traces resembling city streets, dramatic atmospheric perspective, 8k resolution, cinematic lighting --ar 16:9
  ```

---

## ⚡ Lossless Image Compression Directive
After generating the high-res frames:
1. Run the local lossless compression utility:
   ```bash
   python ytvideos/src/image_optimizer.py --input-dir ytvideos/assets/images --mode lossless
   ```
2. Verify that image dimensions (1920x1080) and pixel sharpness are 100% preserved.
3. Commit compressed assets to `arena/ytvideo-api-backend-images` and open a PR to `master`.
