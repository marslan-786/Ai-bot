import logging
import sys
sys.path.append("Real-ESRGAN")
import os
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder, MessageHandler,
    ContextTypes, CommandHandler, filters
)
from PIL import Image
import torch
import cv2
import numpy as np
import subprocess

# لاگنگ آن کریں
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = "8051814176:AAEZhLo7ZXPTT4dezcvoyIn51Ns13YyRZMM"

# ESRGAN ماڈل انسٹال کریں اگر نہ ہو تو
if not os.path.exists("experiments/pretrained_models/RealESRGAN_x4plus.pth"):
    subprocess.run(["python3", "install_model.py"])

# 🚀 تصویر کو enhance کرنے والا فنکشن
def enhance_image(input_path: str, output_path: str):
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer

    model = RRDBNet(num_in_ch=3, num_out_ch=3, nf=64, nb=23,
                    gc=32, sf=4)
    upsampler = RealESRGANer(
        scale=4,
        model_path='experiments/pretrained_models/RealESRGAN_x4plus.pth',
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False
    )

    image = cv2.imread(input_path, cv2.IMREAD_COLOR)
    output, _ = upsampler.enhance(image, outscale=4)
    cv2.imwrite(output_path, output)

# 📩 تصویر آنے پر پروسیس
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    await update.message.reply_text("🔧 Enhancing your image... please wait.")
    
    input_path = "input.jpg"
    output_path = "output.jpg"
    
    await file.download_to_drive(input_path)
    enhance_image(input_path, output_path)

    await update.message.reply_photo(InputFile(output_path), caption="✅ Done! Here's your enhanced image.")

# 🚀 /start کمانڈ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me a photo and I’ll enhance it to HD for you!")

# 🎯 مین فنکشن
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()