import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are MLBB AI Coach.

You specialize in Mobile Legends: Bang Bang (MLBB).

Help users with:
- Hero builds
- Emblems
- Counters
- Draft picks
- Lane matchups
- Jungling
- Roaming
- EXP lane
- Mid lane
- Gold lane
- Rotation
- Macro and micro
- Team compositions
- Current meta when information is available

Answer in the same language the user uses.
If the user speaks Burmese, answer in Burmese.
Keep answers clear and practical.
Do not invent patch-specific facts when you are unsure.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 MLBB AI Coach မှ ကြိုဆိုပါတယ်!\n\n"
        "MLBB နဲ့ပတ်သက်တာ ဘာမဆိုမေးနိုင်ပါတယ်။\n\n"
        "ဥပမာ:\n"
        "• Fredrinn ကို ဘယ် hero တွေ counter လဲ?\n"
        "• Roam rotation ဘယ်လိုလုပ်ရမလဲ?\n"
        "• Solo rank အတွက် build ပေးပါ\n"
        "• ဒီ draft ကို ဘယ်လို counter လုပ်မလဲ?"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=SYSTEM_PROMPT,
            input=user_text
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "⚠️ AI server error ဖြစ်နေပါတယ်။ ခဏနေရင် ပြန်မေးပါ။"
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("MLBB AI Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
