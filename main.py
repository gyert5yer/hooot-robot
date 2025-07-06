import logging
from telegram import Bot, Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from datetime import datetime
import random
import os

# إعداد البوت
BOT_TOKEN = '8053107448:AAHs_Kb3m2_RGgJ9EDgNe-0375TSJMoP4Gs'

# معرف القنوات (استخدم @username أو ID)
SOURCE_CHANNEL_ID = -1002516462566   # ID أو @username للقناة المصدر
TARGET_CHANNEL_ID = -1002805490166   # ID أو @username للقناة الهدف

# الصورة الثابتة
IMAGE_PATH = 'photo.jpg'

# إعداد اللوجات
logging.basicConfig(level=logging.INFO)

# تنسيق الرسائل
def format_message(message_text: str) -> str:
    lines = message_text.splitlines()
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
    except Exception as e:
        logging.error(f"❌ خطأ أثناء تنسيق الرسالة: {e}")
        return None

# وظيفة التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()

    if "put" in text or "call" in text:
        formatted = format_message(message.text)
        if formatted:
            await context.bot.send_photo(
                chat_id=TARGET_CHANNEL_ID,
                photo=InputFile(IMAGE_PATH),
                caption=formatted
            )
            logging.info("✅ تم إرسال توصية.")

    elif "win" in text:
        await context.bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text="📊 نتيجه الصفقه :\n✅ انتهـت الصـفقه بــربح ✅"
        )
        with open("results.txt", "a", encoding="utf-8") as file:
            file.write("WIN ✅ - " + str(datetime.now()) + "\n")

    elif "loss" in text:
        await context.bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text="📊 نتيجه الصفقه :\n❎ انتهـت الصـفقه بخســـاره ❎"
        )
        with open("results.txt", "a", encoding="utf-8") as file:
            file.write("LOSS ❎ - " + str(datetime.now()) + "\n")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Chat(SOURCE_CHANNEL_ID) & filters.TEXT, handle_message))
    print("🚀 البوت يعمل الآن على مدار الساعة باستخدام Bot Token...")
    app.run_polling()
