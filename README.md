🧠 ORA — Personal AI Assistant (FYP Project)

A local, voice-enabled Personal AI Assistant powered by Groq LLaMA-3.1-70B, Retrieval-Augmented Generation (RAG), and a custom Python GUI.

📌 Introduction

ORA is a Personal AI Assistant developed as a Final Year Project (FYP), designed to provide intelligent, context-aware responses using modern Large Language Models and Retrieval-Augmented Generation (RAG).

The system supports:

Natural language conversations

Speech-to-text (STT)

Text-to-speech (TTS)

Local knowledge retrieval

Desktop GUI interaction

ORA combines LLM reasoning, intent detection, and context retrieval to deliver accurate, personalized answers — all running locally with Groq inference.

✨ Key Features

🚀 Groq-powered LLM using llama-3.1-70b

🧠 RAG Architecture

Detects user intent

Retrieves relevant context from local data

Generates grounded responses

🎙️ Speech Support

Speech-to-Text (STT)

Text-to-Speech (TTS)

🖥️ Desktop GUI (Pure Python)

Built with PyQt5

📂 Local knowledge base

⚡ Fast inference via Groq API

🔐 Environment-based configuration (.env)

🧩 Modular backend/frontend structure

🏗️ Project Architecture
FYP-main/
│
├── Backend/        # Core AI logic (LLM, RAG, orchestration)
├── Frontend/       # PyQt5 GUI
├── Data/           # Local knowledge / documents
│
├── Main.py         # Application entry point
├── .env            # Environment variables (not committed)
└── README.md

🧠 Orchestration-Based Multi-Model Agent Architecture

ORA is designed as an orchestration-driven multi-agent system, where a central reasoning component (“Brain”) dynamically routes user queries to specialized AI agents based on intent classification and task requirements.

Instead of relying on a single model, ORA operates as a coordinated network of agents, each optimized for a specific capability.

This architecture enables modularity, scalability, and intelligent task delegation.

🔗 Core Concept

At the heart of the system is an Orchestration Brain that:

Interprets user input

Classifies intent

Selects the appropriate agent(s)

Manages context flow

Aggregates responses

Returns a unified output to the user

This allows ORA to behave like an intelligent system controller rather than a simple chatbot.

🤖 Agents in the System
🧠 Orchestration Brain (Controller Agent)

The central coordinator responsible for:

User intent classification

Agent selection

Prompt orchestration

Context injection (RAG)

Response aggregation

Acts as the decision-making layer of the assistant.

💬 General Chat Agent

Handles:

Casual conversation

General knowledge queries

Reasoning-based questions

Powered by:

llama-3.1-70b (Groq)

🛠 Automation Agent

Responsible for system-level tasks such as:

File handling

Application control

Local operations

Workflow automation

Triggered when user intent matches automation patterns.

🌐 Real-Time Search Agent

Used when queries require up-to-date information, such as:

Current events

Live data

Recent developments

This agent retrieves external information and feeds it back into the Brain for final response synthesis.

🖼 Image Generation Agent

Handles:

Image creation requests

Visual content generation

Activated when user intent involves creative or visual tasks.

🧠 RAG Context Agent

Retrieves relevant knowledge from:

Local documents

Stored data

Project knowledge base

Provides grounded context to the LLM to avoid hallucinations.

🔄 System Workflow (Agent Orchestration Flow)

Below is the logical flow of the system:

User Input (Text / Voice)
        |
        v
Speech-to-Text (if voice)
        |
        v
-------------------------
|  Orchestration Brain |
-------------------------
        |
        v
Intent Classification
        |
        +-------------------+-------------------+-------------------+
        |                   |                   |
        v                   v                   v
Chat Agent         Automation Agent     Real-Time Search Agent
        |                   |                   |
        +---------+---------+---------+---------+
                  |
                  v
          RAG Context Injection
                  |
                  v
        LLaMA-3.1-70B (Groq Inference)
                  |
                  v
         Response Aggregation Layer
                  |
                  v
Text Output → GUI → Text-to-Speech

🖥️ GUI Implementation

The interface is built entirely in Python (PyQt5) and includes:

Chat window

Animated assistant

Input field

Voice interaction

Dynamic layouts

Core GUI libraries:

PyQt5.QtWidgets
PyQt5.QtGui
PyQt5.QtCore

📸 GUI Preview

<img width="1342" height="763" alt="GUI" src="https://github.com/user-attachments/assets/3ed1e7a2-c4a6-442c-8eef-9e2c5de031ea" />

🛠️ Setup Instructions (Python 3.10.10)
✅ Prerequisites

Python 3.10.10

Git

Groq API Key

1️⃣ Create Virtual Environment (Windows)
python -m venv .venv
.venv\Scripts\activate


Verify:

python --version


Should show:

Python 3.10.10

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Environment Variables

Create a .env file in root:

GROQ_API_KEY=your_groq_api_key_here

ASSISTANT_NAME=ORA
INPUT_LANGUAGE=en
VOICE=en-CA-LiamNeural


⚠️ Never commit .env to GitHub.

4️⃣ Run Application
python Main.py

🚀 Future Improvements

Planned upgrades:

🌐 Web version (Django / FastAPI backend)

⚛️ React frontend

☁️ Cloud deployment

📄 PDF / document ingestion

🧠 Memory persistence

👤 Multi-user profiles

🔍 Advanced vector databases (FAISS / Chroma)

🐳 Docker support

📱 Mobile interface
