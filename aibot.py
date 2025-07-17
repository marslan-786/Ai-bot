import logging
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    CommandHandler,
    filters,
)
import re

# 🔐 اپنی OpenAI API key یہاں لگائیں
openai.api_key = "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"

# 🔐 اپنا Telegram Bot Token یہاں ڈالیں
BOT_TOKEN = "8051814176:AAEZhLo7ZXPTT4dezcvoyIn51Ns13YyRZMM"

# 📜 لاگنگ سیٹ اپ
logging.basicConfig(level=logging.INFO)

# 🟢 /start command پر خوش آمدید پیغام
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

# 🟢 Greetings (Hi, Hello, etc.)
async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(f"👋 Hi {name}, I'm ready to write code scripts for you!")

# 🧠 Handle all code/script requests
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text or ""

    # اگر greet ہو تو الگ ہینڈل کریں
    if re.match(r"(?i)^(hi|hello|salam|hey|aslam o alaikum|how are you)$", user_msg.strip()):
        return await handle_greeting(update, context)

    prompt = f"""You are a professional code generator assistant. The user is asking for a code snippet or a script. 
Only reply with the requested code script without any explanation or intro. Supported languages: Python, JavaScript, C++, Bash, Telegram bot, etc.

User Request: {user_msg}
    
Your Reply (only script):"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You only generate clean scripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        script = response.choices[0].message.content.strip()
        await update.message.reply_text(f"```\n{script}\n```", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await update.message.reply_text("❌ OpenAI API سے جواب حاصل نہیں ہو سکا، دوبارہ کوشش کریں۔")

# 🔁 Bot runner
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"(?i)^(hi|hello|salam|hey|aslam o alaikum|how are you)$"), handle_greeting))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 AI Script Generator Bot is running...")
    app.run_polling()