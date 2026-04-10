# Mbap Telegram Bot

RAG-based Telegram bot that responds as Mbap (Dicky Zainal Arifin) using local knowledge base.

## Requirements

- Python 3.8+
- Telegram Bot Token

## Installation

```bash
# Clone repository
git clone https://github.com/ganikurniabagja-byte/mbap_bot.git
cd mbap_bot

# Install dependencies
pip install -r requirements.txt
```

## Setup

### 1. Get Telegram Bot Token

1. Open Telegram, chat with @BotFather
2. Use /newbot to create new bot
3. Save the token

### 2. Add Bot to Group

1. Add @YourBotUsername to your group
2. Make sure bot has permission to read messages

### 3. Configure Knowledge Base

Edit `kb.json` to add your knowledge base:

```json
[
  {"text": "Content chunk 1..."},
  {"text": "Content chunk 2..."}
]
```

## Running

```bash
# Set bot token
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Run bot
python bot.py
```

## Usage

In group:
- Mention bot: `@MbapDickyBot pertanyaan Anda`
- Bot will respond using knowledge base

## Knowledge Base

The bot uses `kb.json` for responses. Add more content to improve responses.

## Files

| File | Description |
|------|-------------|
| `bot.py` | Main bot entry point |
| `rag_engine.py` | Search engine |
| `persona.py` | Persona enforcement |
| `kb.json` | Knowledge base |
| `requirements.txt` | Python dependencies |

## License

MIT