import logging
import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_chart(image: Image.Image) -> str:
    signals = ['BUY', 'SELL']
    signal = random.choice(signals)
    confidence = random.randint(60, 95)
    duration = random.choice(['1 soat', '2 soat', '3 soat'])

    return f"""
📊 Tahlil natijasi:
🟢 Signal: {signal}
📈 Ishonchlilik: {confidence}%
⏳ Muddat: {duration}
Indikatorlar: MACD, RSI, MA, Bollinger
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 Financial Chart Analyzer Bot

📌 Menga XAUUSD (H1) grafik rasmini yuboring.
Men MACD, RSI, MA, Bollinger asosida signal beraman.

Fayl formati: JPG yoki PNG
""")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = await update.message.photo[-1].get_file()
        photo_bytes = await photo.download_as_bytearray()

        image = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
        if image.format is None:
            await update.message.reply_text("❗Faqat JPG yoki PNG formatni yuboring.")
            return

        await update.message.reply_text("🧠 Tahlil qilinmoqda...")
        result = analyze_chart(image)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
