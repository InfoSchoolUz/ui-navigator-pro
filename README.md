
# UI Navigator Pro

AI agent that can **see your screen and operate your computer automatically**.

UI Navigator Pro uses **Google Gemini Vision** to analyze screenshots, understand the user interface, plan actions, and execute them using automation tools.

This project demonstrates how **multimodal AI agents can control real desktop environments**.

---

## Demo Workflow

User command  
→ Screenshot capture  
→ Gemini Vision analysis  
→ Action planning  
→ PyAutoGUI execution  
→ Computer interface control  

The AI agent understands what is visible on the screen and performs the required actions.

---

## Features

- Screen understanding using Gemini Vision
- Automatic UI navigation
- Action planning based on visual context
- Desktop automation using PyAutoGUI
- Modular architecture for AI agents
- Real‑time screenshot processing

---

## Architecture

System pipeline:

User Command  
↓  
Desktop Client  
↓  
Screenshot Capture  
↓  
Gemini Vision API  
↓  
Action Planner  
↓  
PyAutoGUI Executor  
↓  
Computer Interface  

The system captures the screen, sends the visual context to Gemini Vision, receives a structured action plan, and executes it automatically.

---

## Tech Stack

- Python
- Google Gemini Vision API
- PyAutoGUI
- FastAPI
- Screenshot automation tools

---

## Installation

Clone the repository:

```
git clone https://github.com/InfoSchoolUz/ui-navigator-pro
cd ui-navigator-pro
```

Create virtual environment:

```
python -m venv .venv
```

Activate environment (Windows):

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run the Project

Start the backend:

```
python main.py
```

The system will begin capturing screenshots and interacting with the Gemini Vision API.

---

## Example Use Case

User command:

> Open the browser and search for AI news

UI Navigator Pro will:

1. Capture the current screen
2. Understand the UI elements
3. Plan the required actions
4. Execute them automatically

---

## Why This Project Matters

Modern AI models can understand images, text, and context.

UI Navigator Pro demonstrates how **multimodal AI agents can move beyond chat interfaces and directly interact with real software environments.**

Potential applications include:

- AI operating systems
- Intelligent assistants
- Automated workflows
- Accessibility tools

---

## Hackathon Submission

This project was built for the **Gemini Live Agent Challenge** and demonstrates how Gemini Vision can power autonomous computer‑use agents.

---

## Future Improvements

- Voice commands
- Real‑time video understanding
- Multi‑application automation
- Google Cloud deployment
- Smarter task‑planning agents

---

## Author

**Azamat**  
Informatics & IT teacher from Uzbekistan  

Building real‑time AI tools for education and intelligent software agents.

GitHub: https://github.com/InfoSchoolUz
