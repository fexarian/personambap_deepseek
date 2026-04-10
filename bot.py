import os, logging, requests
from dotenv import load_dotenv
from telegram import Update,.ext
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Multi-provider config
PROVIDERS = {
    "openrouter": {"url": "https://openrouter.ai/api/v1/chat/completions", "key": os.getenv("OPENROUTER_API_KEY"), "model": os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")},
    "glm5": {"url": "https://api.us-west-2.modal.direct/v1/chat/completions", "key": os.getenv("GLM_API_KEY"), "model": "zai-org/GLM-5.1-FP8"},
    "ollama": {"url": f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/generate", "key": None, "model": os.getenv("OLLAMA_MODEL", "gemma2:2b")}
}
current = "openrouter"

async def start(upd, ctx):
    await upd.message.reply_text("🤖 Mbap Bot Active!\nMulti-provider: OpenRouter, GLM-5, Ollama\nGunakan /provider")

async def provider(upd, ctx):
    await upd.message.reply_text(f"Active: {current}\nModel: {PROVIDERS[current]['model']}")

async def switch(upd, ctx, name):
    global current
    if name in PROVIDERS and (PROVIDERS[name].get("key") or name == "ollama"):
        current = name
        await upd.message.reply_text(f"✅ Switched to {name}")
    else:
        await upd.message.reply_text(f"❌ {name} not available (check API key)")

async def chat(upd, ctx):
    msg = upd.message.text
    await upd.message.chat.send_action("typing")
    try:
        p = PROVIDERS[current]
        if current == "ollama":
            resp = requests.post(p["url"], json={"model": p["model"], "prompt": msg, "stream": False}, timeout=60)
            reply = resp.json().get("response", "No response")
        else:
            resp = requests.post(p["url"], headers={"Authorization": f"Bearer {p['key']}", "Content-Type": "application/json"},
                                json={"model": p["model"], "messages": [{"role": "user", "content": msg}], "max_tokens": 500}, timeout=60)
            reply = resp.json()["choices"][0]["message"]["content"]
        await upd.message.reply_text(reply[:4000])
    except Exception as e:
        await upd.message.reply_text(f"Error: {str(e)[:100]}\nCoba /switch ke provider lain")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("provider", provider))
    app.add_handler(CommandHandler("switch_openrouter", lambda u,c: switch(u,c,"openrouter")))
    app.add_handler(CommandHandler("switch_glm5", lambda u,c: switch(u,c,"glm5")))
    app.add_handler(CommandHandler("switch_ollama", lambda u,c: switch(u,c,"ollama")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ Bot with multi-provider running!")
    app.run_polling()

if __name__ == "__main__": main()
