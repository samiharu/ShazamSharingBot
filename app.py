from flask import Flask, request
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.wsgi import WsgiToAsgi
from variables import *


app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

# Initialize the Telegram bot
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

async def send_telegram_message(context: ContextTypes.DEFAULT_TYPE, chat_id, text):
    await context.bot.send_message(chat_id=chat_id, text=text)

@app.route('/send-message', methods=['POST'])
async def send_message():
    # Parse the incoming JSON data
    data = request.get_json()
        
    # Extract the 'message' field from the JSON data
    message_text = data.get('message', 'Default message if key not found')
        
    # Use the bot to send the message asynchronously
    await send_telegram_message(telegram_app, TELEGRAM_CHAT_ID, message_text)
        
    return {"success": True, "message": "Message sent to Telegram group."}

if __name__ == '__main__':
    app.run(debug=True, port=5000)