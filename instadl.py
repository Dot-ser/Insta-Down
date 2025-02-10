import telebot
import requests
from flask import Flask, request
import threading
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://api-aswin-sparky.koyeb.app/api/downloader/igdl?url="

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me an Instagram post link, and I'll download it for you.")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download_instagram_media(message):
    url = message.text
    response = requests.get(API_URL + url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'data' in data and data['data']:
            for media in data['data']:
                media_url = media['url']
                media_type = media['type']
                
                if media_type == 'video':
                    bot.send_video(message.chat.id, media_url)
                elif media_type == 'image':
                    bot.send_document(message.chat.id, media_url)
        else:
            bot.reply_to(message, "No media found. Please check the link.")
    else:
        bot.reply_to(message, "Failed to fetch media. Try again later.")

def run_bot():
    bot.polling()

t = threading.Thread(target=run_bot)
t.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
