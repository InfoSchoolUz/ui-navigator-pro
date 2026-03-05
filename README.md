# 🖥️ UI Navigator Pro

> A voice and vision-powered AI agent that sees your screen and controls your computer — just tell it what you want done, powered by **Google Gemini**.

---

## 🌟 What It Does

UI Navigator Pro takes a screenshot of your screen, listens to your spoken or typed intent, and uses Gemini's multimodal AI to generate a precise action plan — then executes it automatically on your machine. No DOM access. No browser extensions. Just pure visual understanding.

**Example commands:**
- *"Open Chrome and go to Gmail"*
- *"Click the search bar and type quarterly report"*
- *"Scroll down and click the Download button"*
- *"Open Settings and find the Wi-Fi option"*

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 👁️ Visual UI Understanding | Reads your screen like a human — no DOM or APIs needed |
| 🎙️ Voice Intent | Speak your goal out loud; AI understands and acts |
| ⌨️ Text Intent | Type your instruction instead of speaking |
| 🤖 Auto Execution | Clicks, types, scrolls, and presses keys automatically |
| 🔁 Retry Logic | If AI output is invalid JSON, retries with stricter prompt |
| 🐳 Docker Ready | Cloud agent is fully containerized |

---

## 🏗️ Architecture

```
┌─────────────────────┐        ┌──────────────────────┐
│   Desktop Client    │◄──────►│    Cloud Agent        │
│   (PyQt6 UI)        │  HTTP  │    (FastAPI + Gemini) │
│   - Screenshot      │        │    - Vision analysis  │
│   - Audio capture   │        │    - Action planning  │
│   - Action executor │        │    - JSON response    │
└─────────────────────┘        └──────────────────────┘
```

The system is split into two components:
- **Cloud Agent** — receives screenshot + intent, calls Gemini, returns a JSON action plan
- **Desktop Client** — captures screen & audio, sends to agent, executes the returned actions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Google Gemini 2.5 Flash (multimodal) |
| Cloud Agent | Python · FastAPI · Docker |
| Desktop Client | Python · PyQt6 · PyAutoGUI |
| Communication | REST API (HTTP/JSON) |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Docker (for cloud agent)
- A Gemini API key

---

### 🌐 Cloud Agent Setup

```bash
cd cloud_agent
```

Create a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
PLANNER_MODEL_ID=gemini-2.5-flash
```

**Run with Docker:**
```bash
docker build -t ui-navigator-agent .
docker run -p 8000:8000 --env-file .env ui-navigator-agent
```

**Or run directly:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

### 🖥️ Desktop Client Setup

```bash
cd desktop_client
pip install -r requirements.txt
python main.py
```

**Or on Windows, run:**
```bash
START_ALL.bat
```

---

## 🎮 How to Use

1. Start the **cloud agent** (Docker or direct)
2. Launch the **desktop client**
3. In the UI:
   - Type your intent **or** click the microphone to speak
   - Click **"Navigate"**
4. The AI takes a screenshot, analyzes your screen, and executes the actions automatically
5. Watch your cursor move and actions happen in real time

---

## 📁 Project Structure

```
ui-navigator-pro/
├── cloud_agent/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── gemini_client.py # Gemini multimodal planner
│   │   ├── prompts.py       # System instructions
│   │   └── schemas.py       # Request/response models
│   ├── Dockerfile
│   └── requirements.txt
├── desktop_client/
│   ├── app/
│   │   ├── main.py          # PyQt6 entry point
│   │   ├── ui.py            # Desktop UI
│   │   ├── executor.py      # Action executor (click, type, scroll)
│   │   ├── screen_capture.py
│   │   └── audio_recorder.py
│   └── requirements.txt
├── START_ALL.bat            # Windows quick start
└── docs/
```

---

## 🔌 API Reference

### `POST /plan`

Accepts a screenshot and user intent, returns an executable action plan.

**Request:**
```json
{
  "intent": "Open Chrome and navigate to gmail.com",
  "screenshot_b64": "<base64 PNG>",
  "screenshot_width": 1920,
  "screenshot_height": 1080,
  "audio_wav_b64": "<optional base64 WAV>"
}
```

**Response:**
```json
{
  "goal": "Open Chrome and go to Gmail",
  "actions": [
    { "type": "click", "x": 45, "y": 1050, "reason": "Click Chrome taskbar icon" },
    { "type": "press", "key": "CTRL+L", "reason": "Focus address bar" },
    { "type": "type", "text": "gmail.com", "reason": "Enter URL" },
    { "type": "press", "key": "ENTER", "reason": "Navigate" }
  ],
  "confidence": 0.92,
  "notes": ""
}
```

---

## 🔮 Future Roadmap

- [ ] Cross-platform support (macOS, Linux)
- [ ] Multi-step task memory (chained actions)
- [ ] Voice feedback / text-to-speech responses
- [ ] Action history and undo support
- [ ] Browser extension mode

---

## ⚠️ Safety Notice

UI Navigator Pro controls your mouse and keyboard. Always keep your cursor near a screen corner to trigger PyAutoGUI's failsafe and stop execution if needed.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
