import requests
import json
import sys

from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("API_GROQ")


# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

# Responder a cualquier texto que no sea comando
def obtener_respuestaIA(msg_usuario: str) -> str:

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        
        }
    
    data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {"role": "user", "content": msg_usuario}
            ]
        }

    r = requests.post(url, headers=headers, json=data)
    r_json = r.json()

    respuesta = r_json["choices"][0]["message"]["content"] if "choices" in r_json and r_json["choices"] else "Sin respuesta"
    return respuesta

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message back to them."""
    prompt = update.message.text
    respuesta = obtener_respuestaIA(prompt)
    await update.message.reply_text(respuesta)

# Función principal
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Agregar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot iniciado.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
