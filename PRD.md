# Mbap Telegram Bot (RAG Lightweight) - PRD

## Project Overview

**Name:** Mbap Telegram Bot
**Type:** Standalone Telegram Bot with RAG
**Purpose:** Respond as Mbap (Dicky Zainal Arifin) in Telegram groups using knowledge base

---

## Requirements

### Dependencies (Minimal)
```python
python-telegram-bot>=20.0
```
Optional (skip for now): `sentence-transformers`

### Data Source
- **Knowledge Base:** `/root/.openclaw/workspace/dicky_knowledge.json`
- **Format:** `[{"text": "..."}]`
- **Chunks:** 25 chunks from YouTube Ratu Boko

---

## Project Structure

```
mbap_bot/
├── bot.py          # Main Telegram bot entry point
├── kb.json         # Knowledge base (copy from existing)
├── rag_engine.py   # Simple keyword-based search
├── persona.py     # Mbap persona enforcement
├── requirements.txt
└── README.md
```

---

## Components

### 1. bot.py
- Initialize Telegram bot with python-telegram-bot
- Listen to messages in groups
- Detect mention (@MbapDickyBot)
- Pass query → rag_engine → persona → reply

### 2. rag_engine.py
```python
def search(query, kb, top_k=3):
    # Keyword matching
    # Return relevant chunks
    
def get_context(query):
    # Load KB, search, return top results
```

### 3. persona.py
```python
def apply_mbap_style(text):
    # Remove: "saya", "aku", "gue"
    # No questions at end
    # Direct, firm tone
```

### 4. kb.json
- Copy from existing `dicky_knowledge.json`

### 5. requirements.txt
```
python-telegram-bot>=20.0
```

---

## Flow

```
User mentions @MbapDickyBot
    ↓
bot.py receives message
    ↓
rag_engine.search(query, kb)
    ↓
Get relevant chunks
    ↓
persona.apply_mbap_style(response)
    ↓
Send reply to group
```

---

## Constraints

| Constraint | Implementation |
|-----------|---------------|
| No web search | Just local KB |
| No LLM | Keyword matching |
| Strict persona | persona.py filter |
| Lightweight | Minimal deps |

---

## Expected Behavior

| Input | Output |
|-------|--------|
| "Mbap apa itu keraton Boko?" | Answer from KB |
| Question not in KB | "Mbap belum menelusuri lebih lanjut..." |
| Any input without mention | No reply |

---

## Running

```bash
# Install deps
pip install -r requirements.txt

# Set token
export TELEGRAM_BOT_TOKEN="your_token"

# Run
python bot.py
```

---

## Acceptance Criteria

- [ ] Bot responds to mentions in group
- [ ] Uses ONLY knowledge base (no web)
- [ ] No "saya/aku/gue" in responses  
- [ ] "Mbap belum menelusuri lebih lanjut..." when no info
- [ ] Runs standalone (not in OpenClaw)