import os
import random
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, filters, CommandHandler
)

BOT_TOKEN = '8053107448:AAHs_Kb3m2_RGgJ9EDgNe-0375TSJMoP4Gs'
SOURCE_CHANNEL_ID = -1002516462566  # معرف القناة المصدر
TARGET_CHANNEL_ID = -1002805490166  # معرف القناة الهدف
IMAGE_PATH = 'photo.jpg'

WEBHOOK_URL = 'https://telegram_robot.up.railway.app'

# تنسيق الرسالة
def format_message(text):
    lines = text.splitlines()
    try:
        pair = lines[0].replace("💳", "").strip()
        raw_time_24 = lines[2].replace("⌛", "").strip()
        raw_direction = lines[3].lower()

        if "put" in raw_direction:
            direction = "Down"
        elif "call" in raw_direction:
            direction = "Up"
        else:
            direction = "غير معروف"

        random_profit = f"{random.randint(90, 99)}%"

        return f"""
📉 اسم الــزوج  : {pair}
🎯 توقيـــت الدخــول : {raw_time_24}
↕️ اتجــاه الصفقــــه : {direction}
🕒 مــده الصفقـــه : 2MIN

• نسبه الربح المتوقعة {random_profit} ❇️
• للتواصل معي @ALPASHMO7ASB ⚡️
        """.strip()
    except:
        return None

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    print("📥 رسالة مستلمة من القناة المصدر:")
    print(message.text)  # عرض محتوى الرسالة في اللوج

    text = message.text.lower()
    formatted = format_message(message.text)

    if "put" in text or "call" in text:
        if formatted:
            await context.bot.send_photo(
                chat_id=TARGET_CHANNEL_ID,
                photo=InputFile(IMAGE_PATH),
                caption=formatted
            )

    elif "win" in text:
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text="📊 نتيجه الصفقه :\n✅ انتهـت الصـفقه بــربح ✅")
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write("WIN ✅ - " + str(datetime.now()) + "\n")

    elif "loss" in text:
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text="📊 نتيجه الصفقه :\n❎ انتهـت الصـفقه بخســـاره ❎")
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write("LOSS ❎ - " + str(datetime.now()) + "\n")

# أمر /start للتأكد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت يعمل بنظام Webhook!")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Chat(SOURCE_CHANNEL_ID) & filters.TEXT, handle_message))

    print("🚀 البوت يعمل الآن باستخدام Webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        webhook_url=WEBHOOK_URL
    )
