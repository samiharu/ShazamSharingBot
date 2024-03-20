from flask import Flask, request
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.wsgi import WsgiToAsgi
from variables import *

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

# Initialize the Telegram bot
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

async def send_telegram_message(context: ContextTypes.DEFAULT_TYPE, chat_id, text):
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

@app.route('/send-message', methods=['POST'])
async def send_message():
    # Parse the incoming JSON data
    data = request.get_json()
        
    # Extract the fields from the JSON data
    #artwork = data.get('artwork', 'No artwork')
    link = data.get('message', 'No link').split('?')[0]
    username = data.get('username', 'No username')
    location = data.get('location', 'No location')

    telegram_message = f"<b>Track for</b> {username}\n<b>Shazam URL:</b> <a href='{link}'>{link}</a>\n<b>Location:</b> <a href='{location}'>{location}</a>"
        
    # Use the bot to send the message asynchronously
    await send_telegram_message(telegram_app, TELEGRAM_CHAT_ID, telegram_message)
        
    return {"success": True, "message": "Message sent to Telegram group."}

if __name__ == '__main__':
    app.run(debug=True, port=8000)