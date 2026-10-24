
# AI Agent 3.0

A locally running AI-powered personal assistant developed using Python, Ollama, Streamlit, Playwright, and Faster Whisper.

The project combines conversational AI, voice commands, browser automation, file management, and persistent memory without requiring paid AI APIs.

## Features

- AI-powered conversational chat
- Voice-to-text commands
- Multi-step task execution
- Browser automation using Playwright
- Permanent memory using JSON
- Automatic memory saving and updating
- File and folder management
- Date and time utilities
- Streamlit web interface
- Error handling

## Technologies Used

- Python
- Streamlit
- Ollama (llama3.2:1b)
- Faster Whisper
- Playwright
- JSON

## Installation

1. Install Python and Ollama.
2. Clone this repository.
3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate it on Windows:

```bash
.venv\Scripts\activate
```

5. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

6. Download the Ollama model:

```bash
ollama pull llama3.2:1b
```

7. Install Playwright Chromium:

```bash
python -m playwright install chromium
```

## Run the Project

Start Ollama if it is not already running:

```bash
ollama serve
```

In another terminal, start Streamlit:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Project Structure

```text
Ai-Agent-3.0/
    app.py
    agent.py
    agent_router.py
    browser_automation.py
    memory_manager.py
    tools.py
    agent_memory.json
    agent_workspace/
    requirements.txt
    README.md
```

## Developer

Akshay Krishnan

Developed as a Python and AI automation portfolio project.
