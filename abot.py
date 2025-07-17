import logging
import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Logging
logging.basicConfig(level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"👋 Hello {user.first_name}!\n\n"
        f"🤖 *Welcome to Impossible AI Chat Bot!*\n"
        f"This bot is for scripting only.\n\n"
        f"🧠 Supported Languages:\n"
        f"`Python`, `JavaScript`, `C++`, `Bash`, `HTML`, `Telegram Bots`\n\n"
        f"👑 Owner: [@{user.username}](tg://user?id={user.id})\n\n"
        f"💬 Just type your request like:\n"
        f"`Make me a telegram bot to ban users`"
    )
    await update.message.reply_text(welcome_msg, parse_mode="Markdown")

# Handle greeting
async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👋 Hi {user.first_name}, I'm ready to write scripts for you!")

# Handle general messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Greeting filter
    if re.match(r"(?i)^(hi|hello|salam|hey|aslam o alaikum|how are you)$", text):
        return await handle_greeting(update, context)

    prompt = f"""You are a professional code generator assistant. The user is asking for a code snippet or a script. 
Only reply with the requested code script without any explanation or intro. Supported languages: Python, JavaScript, C++, Bash, Telegram bot, etc.

User Request: {text}

Your Reply (only script):"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You only generate clean scripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        code = response.choices[0].message.content.strip()
        await update.message.reply_text(f"```\n{code}\n```", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"❌ OpenAI Error: {e}")
        await update.message.reply_text(f"❌ OpenAI API سے جواب حاصل نہیں ہو سکا:\n\n{e}")

# Run bot
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN environment variable not set.")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"(?i)^(hi|hello|salam|hey|aslam o alaikum|how are you)$"), handle_greeting))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 AI Script Generator Bot is running...")
    app.run_polling()