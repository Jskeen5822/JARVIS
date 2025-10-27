<h1 align="center">🤖 JARVIS</h1>
<p align="center">
  <i>A personal AI assistant that listens, speaks, and takes action — built by Jonathon Skeen.</i>
</p>

---

## 🧠 Overview
OU-JARVIS is a **voice-controlled AI assistant** that bridges the gap between code and the physical world.
It combines **Python**, **OpenAI**, and **Raspberry Pi** to automate everyday tasks with natural speech and real-time hardware feedback.

> “Jarvis, open VS Code and turn on my desk lamp.” — You, channeling Tony Stark 😎

---

## ✨ Features
- Voice recognition using `SpeechRecognition` or Whisper API
- Natural responses with `pyttsx3` or ElevenLabs voices
- ChatGPT integration for intelligent conversation
- IoT hardware control via Raspberry Pi or Arduino
- Custom skill modules — add your own commands easily
- Optional local dashboard to monitor and trigger events

---

## 🧩 Tech Stack
| Component | Technology |
|-----------|------------|
| 🧠 Intelligence | OpenAI GPT API |
| 🎙️ Voice Input | Whisper / SpeechRecognition |
| 🔊 Voice Output | pyttsx3 / ElevenLabs |
| ⚡ Hardware | Raspberry Pi, Arduino |
| 🌐 Interface | Flask, JavaScript Dashboard |
| 💾 Language | Python |

---

## ⚙️ Installation

```bash
git clone https://github.com/JonathonSkeen/JARVIS.git
cd JARVIS
pip install -r requirements.txt
python main.py
```

---

## 🚀 Quickstart

1. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY` (and `ELEVENLABS_API_KEY` if needed).
2. (Optional) Configure microphone settings in `.env` or set `ENABLE_MICROPHONE=false` to stick with text input.
3. Install dependencies: `pip install -r requirements.txt`.
4. Launch the assistant: `python main.py`.
5. Say "quit" or press `Ctrl+C` to stop.

> **Note:** `pyaudio` may require platform-specific wheels. On Windows, install from [PyAudio releases](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) if `pip` fails.

---

## 🗂️ Project Structure

```
JARVIS/
├─ main.py
├─ requirements.txt
├─ .env.example
└─ src/jarvis/
  ├─ config.py
  ├─ core/assistant.py
  ├─ integrations/openai_client.py
  ├─ io/voice_listener.py
  ├─ io/voice_responder.py
  ├─ hardware/controller.py
  └─ skills/
```

---

## 🛠️ Configuration

- `OPENAI_API_KEY` (required) powers GPT responses.
- `ENABLE_MICROPHONE` toggles live speech capture; set to `false` for terminal text input.
- Set `USE_WHISPER_API=true` to stream audio to Whisper; otherwise SpeechRecognition handles transcription locally.
- Choose `VOICE_ENGINE=pyttsx3` (local), `VOICE_ENGINE=elevenlabs` (cloud), or `VOICE_ENGINE=text` to keep everything in the terminal.
- On Raspberry Pi, toggle `ENABLE_GPIO=true` and add device registration in `hardware/controller.py`.

The assistant fails fast if a critical secret is missing, keeping setup issues obvious.

---

## 🧠 Skills & Routing

- **System Control:** Launch Visual Studio Code or open a terminal.
- **Lighting:** Toggle the demo `desk_lamp` device (GPIO or simulated).
- **Fallback Chat:** When no skill matches, GPT keeps the conversation flowing.

Add new skills under `src/jarvis/skills/`, subclass `Skill`, and register them in `core/assistant.py`.

---

## 🔌 Hardware Integration

- `HardwareController` registers GPIO actions and includes a simulated LED for development.
- Use `attach_example_led(pin=17, name="desk_lamp")` as a template before wiring real hardware.
- When running outside Raspberry Pi, simulated outputs keep flows testable.

---

## 🧱 Roadmap Ideas

- Web dashboard (Flask + Socket.IO) to monitor conversations and trigger commands.
- Home automation bridges (Home Assistant, Philips Hue, smart plugs).
- Persistent memory layer for task context.
- Streaming responses to cut latency between hearing and speaking.
