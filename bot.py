import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from google import genai

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

print("=== BOT TEKSHIRUVI ===")
print("TELEGRAM TOKEN:", "BOR" if TOKEN else "YO'Q")
print("GEMINI KEY:", "BOR" if GEMINI_KEY else "YO'Q")

if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN topilmadi!")

if not GEMINI_KEY:
    raise Exception("GEMINI_API_KEY topilmadi!")

client = genai.Client(api_key=GEMINI_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "Men Gemini AI botman 🤖\n"
        "Savolingizni yozing."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.8-flash",
            contents=update.message.text
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        print("GEMINI XATOSI:", repr(e))
        await update.message.reply_text(
            "❌ Gemini xatosi yuz berdi."
        )


def main():
    print("=== BOT ISHLAYAPTI ===")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("=== TELEGRAM POLLING BOSHLANDI ===")
    app.run_polling()


if __name__ == "__main__":
    main()
