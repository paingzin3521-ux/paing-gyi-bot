import telebot
from telebot import types
import random
import string
from datetime import datetime, timedelta

# [!] Token ကို ဒီမှာ အမှန်အတိုင်း ထည့်ပါ
TOKEN = "8557413081:AAH5eWNAVr9U8TN6M3SywY34O4Ooy7gWJZc"
bot = telebot.TeleBot(TOKEN)

# [!] Paing Gyi ရဲ့ Telegram ID ကို ဒီမှာ ထည့်ပါ
ADMIN_ID = 1000037717 

# Key ထုတ်ပေးတဲ့ Function
def generate_locked_key(device_id, prefix):
    id_part = str(device_id)[-4:] if len(str(device_id)) >= 4 else str(device_id)
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{id_part}-{random_part}"

@bot.message_handler(commands=['start'])
def start(message):
    status = "👑 ADMIN" if message.from_user.id == ADMIN_ID else "👤 USER"
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚀 Internet Speed Bypass')
    btn2 = types.KeyboardButton('🔑 Voucher Code Hack')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, f"🌟 **PAING GYI VIP KEY BOT**\nSTATUS: {status}\n\nအောက်က ခလုတ်တစ်ခုခုကို နှိပ်ပါဗျ။", reply_markup=markup, parse_mode="Markdown")

# --- ခလုတ်များ နှိပ်လိုက်လျှင် ---
@bot.message_handler(func=lambda message: message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack'])
def ask_for_id(message):
    prefix = "SPEED" if "Speed" in message.text else "VOUCH"
    msg = bot.send_message(message.chat.id, f"🆔 {message.text} အတွက် **Device ID** ကို ရိုက်ပို့ပေးပါဗျ။")
    
    # ID ပို့လာရင် လက်ခံဖို့ စောင့်မယ်
    bot.register_next_step_handler(msg, process_id, prefix)

def process_id(message, prefix):
    device_id = message.text
    
    # ခလုတ်စာသားတွေ မှားဝင်လာရင် ပယ်ချမယ်
    if device_id in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '/start']:
        bot.send_message(message.chat.id, "❌ ID မှားနေပါတယ်။ ခလုတ်ကို မနှိပ်ဘဲ ID ကို ရိုက်ပို့ပေးပါဗျ။")
        return

    # သက်တမ်းသတ်မှတ်ချက်
    minutes = 120 if prefix == "SPEED" else 30
    final_key = generate_locked_key(device_id, prefix)
    expiry_time = (datetime.now() + timedelta(minutes=minutes)).strftime('%I:%M %p')

    result = (
        f"✅ **{prefix} HACK SUCCESS**\n\n"
        f"📱 Device ID: `{device_id}`\n"
        f"🔑 Key: `{final_key}`\n"
        f"⏰ သက်တမ်း: {minutes} မိနစ် ({expiry_time} အထိ)\n\n"
        f"©️ Developed by Paing Gyi"
    )
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

print("Paing Gyi Bot is active...")
bot.polling(none_stop=True)
