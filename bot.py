import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an MLBB AI Coach.

You specialize in Mobile Legends: Bang Bang.

Help with:
- Hero builds
- Counters
- Emblems
- Draft
- Lane matchups
- Jungle
- Roam
- EXP lane
- Mid lane
- Gold lane
- Rotation
- Macro and micro
- Team composition
- Meta

Reply in the same language as the user.
If the user speaks Burmese, reply in Burmese.
Give practical and clear answers.
Do not invent facts when uncertain.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 MLBB AI Coach\n\n"
        "MLBB နဲ့ပတ်သက်တာ ဘာမဆိုမေးနိုင်ပါတယ်!"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=SYSTEM_PROMPT,
            input=user_text,
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as e:
        print("OPENAI ERROR:", repr(e))

        await update.message.reply_text(
            "⚠️ AI server error ဖြစ်နေပါတယ်။"
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("TELEGRAM ERROR:", repr(context.error))


def main():
    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    app.add_error_handler(error_handler)

    print("🔥 MLBB AI Bot started!")

    app.run_polling(
        drop_pending_updates=True,
        timeout=30,
    )


if __name__ == "__main__":
    main()
