import os import requests import telebot import json from flask import Flask, request from datetime import datetime

Load Environment Variables

BOT_TOKEN = os.getenv("7738466078:AAFFSbV6m5VYmnBDjWfwufGvBHH9jya1qX8") API_URL = "https://codex-ml.xyz/api/rc.php?regno=" GROUP_ID = int(os.getenv("GROUP_ID", "-1002320210604"))  # Default group ID

Initialize Flask & Telebot

bot = telebot.TeleBot(BOT_TOKEN) app = Flask(name)

Function to check if user is in the group

def is_user_in_group(user_id): try: chat_member = bot.get_chat_member(GROUP_ID, user_id) return chat_member.status in ["member", "administrator", "creator"] except: return False

Start command

@bot.message_handler(commands=['start']) def start(message): if is_user_in_group(message.from_user.id): bot.reply_to(message, "👋 Welcome! Send a vehicle number to get details. Example: MH43BM9716") else: bot.reply_to(message, "🚫 To use this bot, you must first join our channel: @RtoVehicle")

Fetch vehicle details

@bot.message_handler(func=lambda message: True) def fetch_vehicle_details(message): if not is_user_in_group(message.from_user.id): bot.reply_to(message, "🚫 To use this bot, you must first join our channel: @RtoVehicle") return

regno = message.text.strip().upper()
response = requests.get(API_URL + regno)

if response.status_code == 200:
    try:
        data = response.json()

        if not data or "error" in data or not data.get("data") or not data['data'].get('detail'):
            bot.reply_to(message, f"❌ Error: {data.get('error', 'No data found.')}")
            return

        vehicle_data = data['data']['detail']
        full_details = json.loads(vehicle_data.get('full_details', '{}'))

        formatted_text = f"""

🎯 Search Results - {regno} ⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚘 Vehicle Details 📋 Basic Details 🔹 Vehicle Number: {vehicle_data.get('registrationNumber', 'N/A')} 🏭 Brand: {full_details.get('maker', 'N/A')} 🚗 Model: {vehicle_data.get('rc_model', 'N/A')} 🎨 Color: {vehicle_data.get('color', 'N/A')} 🛢️ Fuel Type: {vehicle_data.get('rawFuelType', 'N/A')}

📄 Registration Details 🗓️ Registered At: {vehicle_data.get('registeredAt', 'N/A')} 📍 Registered Place: {vehicle_data.get('registeredPlace', 'N/A')} 📄 RC Status: {vehicle_data.get('rcStatus', 'N/A')} 🛠️ Fitness Valid Upto: {vehicle_data.get('fitnessUpTo', 'N/A')} 💰 Tax Valid Upto: {vehicle_data.get('taxUpTo', 'N/A')} """ bot.reply_to(message, formatted_text) except Exception as e: bot.reply_to(message, f"⚠️ Error processing data: {str(e)}") else: bot.reply_to(message, "⚠️ Error fetching data. Please try again later.")

Flask Webhook Setup

@app.route("/set_webhook") def set_webhook(): bot.remove_webhook() bot.set_webhook(url=os.getenv("WEBHOOK_URL"))  # Set in Render env variables return "Webhook set successfully!", 200

@app.route("/webhook", methods=["POST"]) def webhook(): if request.method == "POST": update = telebot.types.Update.de_json(request.get_data().decode("utf-8")) bot.process_new_updates([update]) return "OK", 200

Run Flask App

if name == "main": port = int(os.environ.get("PORT", 10000))  # Render assigns PORT automatically app.run(host="0.0.0.0", port=port)

