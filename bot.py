#!/usr/bin/env python3
"""
Mbap Telegram Bot - RAG Lightweight Version
Uses keyword-based search (no heavy ML dependencies)
"""
import os
import re
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import local modules
from rag_engine import search_kb
from persona import apply_mbap_style

# Try to import LLM engine (optional)
try:
    from llm_engine import answer_question as llm_answer
    HAS_LLM = True
except:
    HAS_LLM = False

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

# Bot username for mention detection
BOT_USERNAME = "@mbapdickybot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "Mbap Bot aktif. Mention untuk bertanya.\n"
        "Gunakan: @MbapDickyBot pertanyaan anda"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "Cara menggunakan:\n"
        f"1. Mention bot: {BOT_USERNAME} pertanyaan\n"
        "2. Contoh: @MbapDickyBot apa itu keraton Boko?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages in groups"""
    message = update.message
    text = message.text or ""
    chat = message.chat
    
    # Only respond in groups
    if chat.type not in ['group', 'supergroup']:
        return
    
    # Check if bot is mentioned
    entities = message.entities or []
    mentioned = False
    
    for entity in entities:
        if entity.type == "mention":
            mentioned = True
            break
    
    # Also check if bot username in text
    if BOT_USERNAME.lower() in text.lower():
        mentioned = True
    
    if not mentioned:
        return
    
    # Remove mention from text
    clean_query = re.sub(r'@\w+\s*', '', text).strip()
    
    if not clean_query:
        return
    
    logger.info(f"Query: {clean_query[:50]}...")
    
    # Use LLM if available
    if HAS_LLM:
        try:
            response = llm_answer(clean_query)
        except Exception as e:
            logger.error(f"LLM error: {e}")
            results = search_kb(clean_query, top_k=1)
            response = results[0] if results else "Mbap belum menelusuri lebih lanjut..."
    else:
        # Fallback to keyword search
        results = search_kb(clean_query, top_k=1)
        response = results[0] if results else "Mbap belum menelusuri lebih lanjut..."
    
    # Apply Mbap persona style
    response = apply_mbap_style(response)
    
    # Send reply
    await message.reply_text(response)


def main():
    """Start the bot"""
    logger.info("Starting Mbap Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS,
            handle_message
        )
    )
    
    # Start polling
    logger.info("Bot started! Waiting for messages...")
    application.run_polling(allowed_updates=[Update.MESSAGE])


if __name__ == "__main__":
    main()