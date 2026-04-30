import telebot
from telebot import types
import random
import string
import time
from datetime import datetime, timedelta

# [!] Paing Gyi ရဲ့ Token ကို ဒီမှာ ထည့်ပါ
TOKEN = "8557413081:AAH5eWNAVr9U8TN6M3SywY34O4Ooy7gWJZc"
bot = telebot.TeleBot(TOKEN)

# [!] Paing Gyi ရဲ့ Telegram ID ကို ဒီမှာ ပြောင်းထည့်ပါ
ADMIN_ID = 1000037717 

user_last_claim = {}

def generate_locked_key(device_id, prefix):
    id_part = str(device_id)[-4:] if len(str(device_id)) >= 4 else str(device_id)
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{id_part}-{random_part}"

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    status = "👑 ADMIN" if is_admin(user_id) else "👤 USER"
    design = (
        f"┏━━━━━━━━━━━━━━━━┓\n"
        f"   PAING GYI ULTIMATE V1.0\n"
        f"   STATUS: {status}\n"
        f"┗━━━━━━━━━━━━━━━━┛\n\n"
        f"ID ပေးပြီး Key ထုတ်ယူနိုင်ပါပြီဗျာ။"
    )
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚀 Internet Speed Bypass')
    btn2 = types.KeyboardButton('🔑 Voucher Code Hack')
    btn3 = types.KeyboardButton('👤 Contact Admin')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, design, reply_markup=markup)

# --- Speed Bypass (120 min) ---
@bot.message_handler(func=lambda message: message.text == '🚀 Internet Speed Bypass')
def speed_ask_id(message):
    user_id = message.from_user.id
    if not is_admin(user_id) and user_id in user_last_claim:
        if time.time() - user_last_claim[user_id] < 86400:
            bot.reply_to(message, "⏳ ၂၄ နာရီပြည့်မှ တစ်ခါပြန်ယူလို့ရပါမယ်။")
            return
    msg = bot.send_message(message.chat.id, "🆔 Speed တင်ရန် **Device ID** ပို့ပေးပါဗျ။")
    bot.register_next_step_handler(msg, process_speed_key)

# --- Voucher Hack (30 min သို့ ပြင်ထားသည်) ---
@bot.message_handler(func=lambda message: message.text == '🔑 Voucher Code Hack')
def voucher_ask_id(message):
    user_id = message.from_user.id
    if not is_admin(user_id) and user_id in user_last_claim:
        if time.time() - user_last_claim[user_id] < 86400:
            bot.reply_to(message, "⏳ တစ်ရက်လျှင် တစ်ခါသာ ခွင့်ပြုပါသည်။")
            return
    msg = bot.send_message(message.chat.id, "🆔 Voucher ထုတ်ရန် **Device ID** ပို့ပေးပါဗျ။")
    bot.register_next_step_handler(msg, process_voucher_key)

def process_speed_key(message):
    if message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '👤 Contact Admin', '/start']:
        bot.send_message(message.chat.id, "❌ ID မှားယွင်းနေပါသည်။ ခလုတ်မဟုတ်ဘဲ ID ကိုသာ ပို့ပေးပါ။")
        return
    handle_key_generation(message, "SPEED", 120)

def process_voucher_key(message):
    if message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '👤 Contact Admin', '/start']:
        bot.send_message(message.chat.id, "❌ ID မှားယွင်းနေပါသည်။ ခလုတ်မဟုတ်ဘဲ ID ကိုသာ ပို့ပေးပါ။")
        return
    handle_key_generation(message, "VOUCH", 30) # ဒီနေရာမှာ 30 min ပြင်လိုက်ပါပြီ

def handle_key_generation(message, prefix, minutes):
    device_id = message.text
    user_id = message.from_user.id
    final_key = generate_locked_key(device_id, prefix)
    
    if not is_admin(user_id):
        user_last_claim[user_id] = time.time()
        
    expiry_time = (datetime.now() + timedelta(minutes=minutes)).strftime('%I:%M %p')
    
    result = (
        f"✅ **{prefix} KEY SUCCESS**\n\n"
        f"📱 Device ID: `{device_id}`\n"
        f"🔑 Key: `{final_key}`\n"
        f"⏰ သက်တမ်းကုန်မည့်အချိန်: {expiry_time}\n\n"
        f"©️ Developed by Paing Gyi"
    )
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == '👤 Contact Admin')
def contact(message):
    bot.send_message(message.chat.id, "👨‍💻 Owner: @PaingGyi")

bot.polling()
