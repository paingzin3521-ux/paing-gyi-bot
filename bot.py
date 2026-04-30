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
# User တွေ ဘယ်အဆင့်ရောက်နေလဲ မှတ်ဖို့ (ID တောင်းနေတာလား စစ်ဖို့)
user_state = {}

def generate_locked_key(device_id, prefix):
    id_part = str(device_id)[-4:] if len(str(device_id)) >= 4 else str(device_id)
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{id_part}-{random_part}"

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_state[user_id] = None # State ကို Clear လုပ်မယ်
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

# --- ခလုတ်များနှိပ်လိုက်လျှင် State သတ်မှတ်ခြင်း ---
@bot.message_handler(func=lambda message: message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack'])
def handle_menu(message):
    user_id = message.from_user.id
    
    # Admin မဟုတ်ရင် ၂၄ နာရီ စစ်မယ်
    if not is_admin(user_id) and user_id in user_last_claim:
        if time.time() - user_last_claim[user_id] < 86400:
            bot.reply_to(message, "⏳ ၂၄ နာရီပြည့်မှ တစ်ခါပြန်ယူလို့ရပါမယ်ဗျ။")
            return

    if message.text == '🚀 Internet Speed Bypass':
        user_state[user_id] = "AWAITING_SPEED_ID"
        bot.send_message(message.chat.id, "🆔 Speed တင်ရန် သင်၏ **Device ID** ကို ရိုက်ပို့ပေးပါဗျ။")
    else:
        user_state[user_id] = "AWAITING_VOUCH_ID"
        bot.send_message(message.chat.id, "🆔 Voucher ထုတ်ရန် သင်၏ **Device ID** ကို ရိုက်ပို့ပေးပါဗျ။")

# --- စာသား (ID) ပို့လာလျှင် စစ်ဆေးပြီး Key ထုတ်ပေးခြင်း ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    state = user_state.get(user_id)

    if state == "AWAITING_SPEED_ID":
        # ID နေရာမှာ ခလုတ်စာသားတွေ ပြန်ဝင်လာရင် ပယ်ချမယ်
        if message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '👤 Contact Admin']:
            bot.send_message(message.chat.id, "❌ ID ပို့ရမည့်နေရာတွင် ခလုတ်နှိပ်၍မရပါ။ ID ကိုသာ ရိုက်ပို့ပါ။")
            return
        
        user_state[user_id] = None # ပြီးသွားရင် State ဖျက်မယ်
        handle_key_generation(message, "SPEED", 120)

    elif state == "AWAITING_VOUCH_ID":
        if message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '👤 Contact Admin']:
            bot.send_message(message.chat.id, "❌ ID ပို့ရမည့်နေရာတွင် ခလုတ်နှိပ်၍မရပါ။ ID ကိုသာ ရိုက်ပို့ပါ။")
            return
        
        user_state[user_id] = None
        handle_key_generation(message, "VOUCH", 30) # 30 min သာ ပေးသည်

    elif message.text == '👤 Contact Admin':
        bot.send_message(message.chat.id, "👨‍💻 Owner: @PaingGyi")
    else:
        bot.send_message(message.chat.id, "💡 မင်္ဂလာပါ! Key ယူလိုပါက အောက်က ခလုတ်ကို အရင်နှိပ်ပါဗျ။")

def handle_key_generation(message, prefix, minutes):
    device_id = message.text
    user_id = message.from_user.id
    final_key = generate_locked_key(device_id, prefix)
    
    if not is_admin(user_id):
        user_last_claim[user_id] = time.time()
        
    expiry_time = (datetime.now() + timedelta(minutes=minutes)).strftime('%I:%M %p')
    
    result = (
        f"✅ **{prefix} HACK SUCCESS**\n\n"
        f"📱 Device ID: `{device_id}`\n"
        f"🔑 Your Key: `{final_key}`\n"
        f"⏰ သက်တမ်းကုန်မည့်အချိန်: {expiry_time} ({minutes} မိနစ်)\n\n"
        f"⚠️ ဤ Key ကို မိမိ ID အတွက်သာ သုံးပါ!"
    )
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

bot.polling()
