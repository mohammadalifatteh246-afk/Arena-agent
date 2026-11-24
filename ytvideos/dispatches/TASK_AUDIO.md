# 🎙️ ARENA AGENT SESSION 2: VOICEOVER NARRATION & AUDIO MASTERING

- **Dispatched By:** Google Antigravity (`ytvideos` engine)
- **Target Branch:** `arena/ytvideo-api-backend-audio`
- **Execution Target:** Arena Cloud Agent Sandbox (`arena.ai/agent`)
- **Mission:** Humanized Voice Synthesis & -14 LUFS Audio Mastering
- **Audio Standards:** ITU-R BS.1770-4 (-14.0 Integrated LUFS, -1.0 dBTP True Peak)

---

## 🎯 Production Objective
Generate the complete humanized voiceover tracks and procedural soundscape for "How The Internet ACTUALLY Works: APIs & Backends".
Avoid robotic monotony by strictly applying the SSML prosody tags, natural breath pauses, and cadence modulation below.

---

## 🗣️ Humanized Voiceover Script (With SSML & Breath Tokens)

### Scene 1: The Hook [0:00 - 0:08]
- **Target File:** `ytvideos/assets/audio/voice_01_hook.wav`
- **SSML Blueprint:**
  ```xml
  <speak>
    <prosody rate="102%" pitch="+1st">
      Every time you tap <emphasis level="strong">'Order Pizza'</emphasis> on your phone,
    </prosody>
    <break time="200ms"/>
    [breath]
    <prosody rate="98%" pitch="-1st">
      an invisible messenger sprints across the planet in forty milliseconds.
    </prosody>
    <break time="250ms"/>
    <prosody rate="95%" pitch="-2st">
      That messenger... <emphasis level="moderate">is an API.</emphasis>
    </prosody>
  </speak>
  ```

### Scene 2: The Restaurant & Kitchen [0:08 - 0:24]
- **Target File:** `ytvideos/assets/audio/voice_02_anatomy.wav`
- **SSML Blueprint:**
  ```xml
  <speak>
    <prosody rate="100%">
      Think of your app like a luxury restaurant.
      The screen you touch is just the dining room.
    </prosody>
    <break time="300ms"/>
    [breath]
    <prosody rate="98%">
      But deep behind the soundproof doors is the Backend kitchen —
      where databases store your data, and servers execute the business logic.
    </prosody>
  </speak>
  ```

### Scene 3: The Protocols [0:24 - 0:44]
- **Target File:** `ytvideos/assets/audio/voice_03_protocols.wav`
- **SSML Blueprint:**
  ```xml
  <speak>
    <prosody rate="103%">
      How do they talk? Through protocols!
    </prosody>
    <break time="250ms"/>
    <prosody rate="100%">
      When you request a menu, you send a <emphasis level="moderate">REST GET</emphasis> request.
      When you pay, you send a <emphasis level="moderate">POST request</emphasis> with encrypted JSON.
    </prosody>
    <break time="300ms"/>
    [breath]
    <prosody rate="100%">
      And when you track the driver live on the map?
      That's <emphasis level="strong">WebSockets</emphasis> — a continuous open pipe keeping you synchronized.
    </prosody>
  </speak>
  ```

### Scene 4: Climax & Loop [0:44 - 1:00]
- **Target File:** `ytvideos/assets/audio/voice_04_payoff.wav`
- **SSML Blueprint:**
  ```xml
  <speak>
    <prosody rate="98%">
      Without a backend, an app is just an empty drawing. With one, it's an intelligent engine.
    </prosody>
    <break time="400ms"/>
    [breath]
    <prosody rate="95%" pitch="-1st">
      So next time your favorite app freezes, ask yourself:
      did the waiter drop the tray... <break time="500ms"/> or is the kitchen on fire?
    </prosody>
  </speak>
  ```

---

## 🎚️ Mastering & Procedural Sound Design Tasks
1. Generate procedural background soundscapes using `python ytvideos/src/audio_engine.py`.
2. Mix voiceover with -6dB music ducking.
3. Master to **-14.0 LUFS** and verify **True Peak ≤ -1.0 dBTP**.
4. Commit audio files to `arena/ytvideo-api-backend-audio` and open a PR to `master`.
