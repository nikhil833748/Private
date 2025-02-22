import requests
import telebot
import json
from datetime import datetime

# Telegram bot token
BOT_TOKEN = "7738466078:AAFFSbV6m5VYmnBDjWfwufGvBHH9jya1qX8"

# API URL
API_URL = "https://codex-ml.xyz/api/rc.php?regno="

# Group ID (Replace with your actual group ID)
GROUP_ID = -1002320210604  # Replace with your group ID

bot = telebot.TeleBot(BOT_TOKEN)

# Function to check if user is in the group
def is_user_in_group(user_id):
    try:
        chat_member = bot.get_chat_member(GROUP_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    if is_user_in_group(message.from_user.id):
        bot.reply_to(message, "Welcome! Send a vehicle number to get details. Example: MH43BM9716")
    else:
        bot.reply_to(message, "🚫 To use this bot, you must first join our channel: @RtoVehicle")

# Fetch vehicle details
@bot.message_handler(func=lambda message: True)
def fetch_vehicle_details(message):
    if not is_user_in_group(message.from_user.id):
        bot.reply_to(message, "🚫 To use this bot, you must first join our channel: @RtoVehicle")
        return

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
🎯 Search Results - {regno}
⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚘 Vehicle Details

📋 Basic Details
🔹 Vehicle Number: {vehicle_data.get('registrationNumber', 'N/A')}
🏭 Brand: {full_details.get('maker', 'N/A')}
🚗 Model: {vehicle_data.get('rc_model', 'N/A')}
🎨 Color: {vehicle_data.get('color', 'N/A')}
🛢️ Fuel Type: {vehicle_data.get('rawFuelType', 'N/A')}

_____________________________________________

🔧 Technical Details
🔧 Engine Number: {full_details.get('engineNo', 'N/A')}
🔢 Chassis Number: {full_details.get('chassisNo', 'N/A')}
⚙️ Transmission: {vehicle_data.get('transmission', 'N/A')}
⚖️ Unladen Weight (kg): {vehicle_data.get('unladenWt', 'N/A')}
📅 Manufacturing Year: {vehicle_data.get('manufacturingMonthYr', 'N/A')}

_____________________________________________

📄 Registration Details
🗓️ Registered At: {vehicle_data.get('registeredAt', 'N/A')}
📍 Registered Place: {vehicle_data.get('registeredPlace', 'N/A')}
📄 RC Status: {vehicle_data.get('rcStatus', 'N/A')}
🚦 RTO NOC Issued: {vehicle_data.get('rtoNocIssued', 'N/A')}
🛠️ Fitness Valid Upto: {vehicle_data.get('fitnessUpTo', 'N/A')}
💰 Tax Valid Upto: {vehicle_data.get('taxUpTo', 'N/A')}

_____________________________________________

📜 Insurance Details
📜 Insurance Company: {vehicle_data.get('insuranceCompany', 'N/A')}
📅 Insurance Valid Upto: {vehicle_data.get('insuranceUpTo', 'N/A')}
🔖 Insurance Policy Number: {vehicle_data.get('insurancePolicyNo', 'N/A')}

_____________________________________________

👤 Owner Details
👤 Owner Name: {vehicle_data.get('rc_owner_name_masked', 'N/A')}
🔢 Owner Serial Number: {vehicle_data.get('rc_owner_sr', 'N/A')}
📱 Mobile Number: {full_details.get('mobileNo', 'N/A')}
🏠 Present Address: {full_details.get('presentAddressMasked', 'N/A')}
🏡 Permanent Address: {full_details.get('permanentAddressMasked', 'N/A')}

_____________________________________________

📌 Additional Details
✅ PUC Valid Upto: {vehicle_data.get('pucUpTo', 'N/A')}
📝 PUC Number: {full_details.get('pucNo', 'N/A')}
🚫 Blacklist Status: {full_details.get('blacklistStatus', 'N/A')}
🚛 Permit Type: {full_details.get('permitType', 'N/A')}
📑 NOC Details: {full_details.get('nocDetails', 'N/A')}
"""
            bot.reply_to(message, formatted_text)
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error processing data: {str(e)}")
    else:
        bot.reply_to(message, "⚠️ Error fetching data. Please try again later.")

# Start the bot
bot.polling(none_stop=True)
