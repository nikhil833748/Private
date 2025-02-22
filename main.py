import requests import telebot import json from datetime import datetime from flask import Flask, request

Telegram bot token

BOT_TOKEN = "7738466078:AAFFSbV6m5VYmnBDjWfwufGvBHH9jya1qX8"

API URL

API_URL = "https://codex-ml.xyz/api/rc.php?regno="

Group ID (Replace with your actual group ID)

GROUP_ID = -1002320210604

bot = telebot.TeleBot(BOT_TOKEN) app = Flask(name)

@app.route('/') def home(): return "Bot is running!"

@app.route('/webhook', methods=['POST']) def webhook(): update = request.get_json() if update: bot.process_new_updates([telebot.types.Update.de_json(update)]) return "OK", 200

Function to check if user is in the group

def is_user_in_group(user_id): try: chat_member = bot.get_chat_member(GROUP_ID, user_id) return chat_member.status in ["member", "administrator", "creator"] except: return False

@bot.message_handler(commands=['start']) def start(message): if is_user_in_group(message.from_user.id): bot.reply_to(message, "Welcome! Send a vehicle number to get details. Example: MH43BM9716") else: bot.reply_to(message, "\ud83d\udeab To use this bot, you must first join our channel: @RtoVehicle")

@bot.message_handler(func=lambda message: True) def fetch_vehicle_details(message): if not is_user_in_group(message.from_user.id): bot.reply_to(message, "\ud83d\udeab To use this bot, you must first join our channel: @RtoVehicle") return

regno = message.text.strip().upper()
response = requests.get(API_URL + regno)

if response.status_code == 200:
    try:
        data = response.json()
        if not data or "error" in data or not data.get("data") or not data['data'].get('detail'):
            bot.reply_to(message, f"\u274c Error: {data.get('error', 'No data found.')}")
            return

        vehicle_data = data['data']['detail']
        full_details = json.loads(vehicle_data.get('full_details', '{}'))

        formatted_text = f"""

\ud83c\udfaf Search Results - {regno} ⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚘 Vehicle Details

📋 Basic Details 🔹 Vehicle Number: {vehicle_data.get('registrationNumber', 'N/A')} 🏭 Brand: {full_details.get('maker', 'N/A')} 🚗 Model: {vehicle_data.get('rc_model', 'N/A')} 🎨 Color: {vehicle_data.get('color', 'N/A')} 🛢️ Fuel Type: {vehicle_data.get('rawFuelType', 'N/A')}

... (same formatting for remaining details) ... """ bot.reply_to(message, formatted_text) except Exception as e: bot.reply_to(message, f"⚠️ Error processing data: {str(e)}") else: bot.reply_to(message, "⚠️ Error fetching data. Please try again later.")

if name == "main": # Set webhook WEBHOOK_URL = "https://your-app-name.onrender.com/webhook"  # Change this to your Render URL bot.remove_webhook() bot.set_webhook(url=WEBHOOK_URL)

# Run Flask server
app.run(host="0.0.0.0", port=10000)
