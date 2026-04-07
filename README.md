<div align="center">

# 🤖 ORA
### Orchestration Based Retrieval Agent

*A real-time, voice-driven AI assistant for intelligent automation, web intelligence, and multimodal generation*

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Edge TTS](https://img.shields.io/badge/Edge_TTS-Voice-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)


</div>

---

## Overview

Modern AI assistants stop at conversation. **ORA goes further.**

ORA is a fully voice-driven, desktop AI assistant engineered for real-time reasoning, system automation, web intelligence retrieval, and multimodal generation — all through natural conversation. Built with a production-style modular architecture, it demonstrates applied AI engineering, orchestration logic, and real-world automation in a single cohesive system.

---

<img width="1344" height="765" alt="image" src="https://github.com/user-attachments/assets/3b897051-f0ee-4cea-a9b6-8cd76f6f71bb" />


---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER (Voice Input)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    SpeechRecognition                         │
│            Google Speech API  ·  PyAudio  ·  mtranslate      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Decision Model  (Groq · llama-3.1-8b)           │
│         Query Classification  ·  Tool Routing  ·  Context    │
└──────┬──────────┬──────────┬──────────┬───────────┬─────────┘
       │          │          │          │           │
       ▼          ▼          ▼          ▼           ▼
  ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
  │ General │ │Automation│ │  Web   │ │ Image  │ │Realtime  │
  │ Chatbot │ │& System  │ │Search  │ │  Gen   │ │ Search   │
  │ (Groq)  │ │(AppOpen) │ │(DDGS)  │ │ (HF)   │ │(Scraper) │
  └────┬────┘ └────┬─────┘ └───┬────┘ └───┬────┘ └────┬─────┘
       └──────────┴────────────┴──────────┴───────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Response Formatting                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Edge-TTS  ·  pygame  ·  PyQt5 GUI              │
│                     (Voice + Visual Output)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Capabilities

| Module | Capability | Technology |
|--------|-----------|------------|
| 🎤 **Voice Input** | Continuous listening, multilingual support, ambient noise calibration | `SpeechRecognition`, `PyAudio`, `mtranslate` |
| 🧠 **Decision Engine** | Query classification, tool routing, context-aware orchestration | `Groq` · `llama-3.1-8b-instant` |
| 💬 **General Chat** | Conversational AI with persistent session memory | `Groq`, `Cohere` |
| 🌐 **Web Intelligence** | Live search, dynamic content extraction, browser automation | `DDGS`, `BeautifulSoup`, `Selenium` |
| 🖥️ **System Automation** | Open/close apps, YouTube, Google search, volume, reminders | `AppOpener`, `pywhatkit`, `keyboard` |
| 🖼️ **Image Generation** | Prompt-based image generation and processing | `Hugging Face API`, `Pillow` |
| 🔊 **Voice Output** | Natural, low-latency speech synthesis | `edge-tts`, `pygame` |
| 🖼️ **GUI** | Real-time chat display, status indicators | `PyQt5` |

---

## Project Structure

```
ORA/
│
├── Frontend/
│   └── GUI.py                  # PyQt5 interface & status rendering
│
├── Backend/
│   ├── Model.py                # Groq decision-making & query classification
│   ├── Chatbot.py              # General conversational AI
│   ├── RealTimeSearchEngine.py # Live web search & content extraction
│   ├── Automation.py           # System automation & app control
│   ├── SpeechToText.py         # Voice capture & recognition pipeline
│   ├── TextToSpeech.py         # Edge-TTS synthesis & playback
│   └── ImageGeneration.py      # Hugging Face image generation
│
├── Data/
│   ├── ChatLog.json            # Persistent conversation history
│   └── speech.mp3              # TTS audio buffer
│
├── Frontend/Files/             # Runtime status & IPC data files
├── Main.py                     # Orchestration entry point
├── .env                        # Secrets & configuration
└── requirements.txt
```

---

## Setup & Installation

### Prerequisites
- Python 3.10 (recommended)
- A microphone
- API keys for Groq and Hugging Face

### 1. Clone the Repository
```bash
git clone https://github.com/waqas-404/Personal-AI-Asistant
```

### 2. Create Virtual Environment
```bash
py -3.10 -m venv .venv
```
```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r Requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
CohereAPIKey = "Your cohere API key"
Username = Waqas Kareem #You can set any user name 
Assistantname = ORA
GroqAPIKey = "Your Groq API key"
InputLanguage = en
AssistantVoice = en-CA-LiamNeural
HuggingFaceAPIKey = "Enter you hugging face API key"
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)
> Get your Hugging Face key at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 5. Run ORA
```bash
python Main.py
```

Speak naturally — ORA handles the rest.

---

## Tech Stack

### AI & Inference
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![Cohere](https://img.shields.io/badge/Cohere-39594C?style=flat-square&logoColor=white)

### Voice Stack
![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-4285F4?style=flat-square&logo=google&logoColor=white)
![EdgeTTS](https://img.shields.io/badge/Edge_TTS-0078D4?style=flat-square&logo=microsoft&logoColor=white)
![PyAudio](https://img.shields.io/badge/PyAudio-3776AB?style=flat-square&logo=python&logoColor=white)

### Automation & Web
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-3776AB?style=flat-square&logo=python&logoColor=white)
![AppOpener](https://img.shields.io/badge/AppOpener-gray?style=flat-square)

### Interface
![PyQt5](https://img.shields.io/badge/PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-376F9F?style=flat-square&logo=python&logoColor=white)

---

## Engineering Highlights

- **Sub-second decision routing** via `llama-3.1-8b-instant` on Groq — classification latency under 0.5s
- **Eliminated browser-based STT** — replaced Selenium/Chrome Web Speech API with direct Google Speech API calls, reducing STT latency from ~34s to ~2s
- **Persistent pygame mixer** — initialized once at startup rather than per TTS call, eliminating ~3s overhead per response
- **Single persistent asyncio event loop** for TTS generation — no per-call loop creation/destruction overhead
- **Modular tool-routing architecture** — clean separation of concerns across all AI modules
- **Environment-based secure API management** — no hardcoded credentials

---

## Roadmap

- [ ] Wake-word activation
- [ ] Persistent long-term memory
- [ ] Cross-platform packaging (Windows installer / macOS app)
- [ ] Multi-agent orchestration layer
- [ ] Performance profiling dashboard
- [ ] Cloud deployment support

---

## Author

**Waqas Kareem**
*AI/ML Engineer · Automation Developer · Software Engineer*

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/waqas-404)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/waqas-kareem-mlengineer/)

---

<div align="center">
<sub>Built with ❤️ — ORA is open to contributions, feedback, and collaboration.</sub>
</div>
