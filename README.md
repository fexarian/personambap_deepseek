# Mbap Bot - Multi AI Provider

Telegram bot with **OpenRouter, GLM-5, and Local Ollama** support.

## Features
- 🔄 Switch providers on the fly
- 🤖 Local LLM (Gemma 2B via Ollama)
- ☁️ Cloud models via OpenRouter & GLM-5
- 📚 RAG with local knowledge base (optional)

## Quick Start
```bash
cp .env.example .env
# Edit .env with your API keys
pip install -r requirements.txt
python bot.py
```

## Commands
| Command | Action |
|---------|--------|
| `/provider` | Show active AI |
| `/switch_openrouter` | Use OpenRouter |
| `/switch_glm5` | Use GLM-5 |
| `/switch_ollama` | Use local Ollama |

## Environment Variables
```env
TELEGRAM_BOT_TOKEN=xxx
OPENROUTER_API_KEY=xxx
GLM_API_KEY=xxx
OLLAMA_HOST=http://localhost:11434
```

## With Docker
```bash
docker-compose up -d
```

Original RAG files (`rag_engine.py`, `kb.json`) preserved for compatibility.