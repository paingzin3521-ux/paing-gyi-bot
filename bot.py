import telebot
from telebot import types
import random
import string
from datetime import datetime, timedelta

TOKEN = "8557413081:AAH5eWNAVr9U8TN6M3SywY34O4Ooy7gWJZc"
bot = telebot.TeleBot(TOKEN)

ADMIN_NAME = "Pᴀɪɴɢ Zɪɴ Aᴜɴɢ X"

def generate_locked_key(device_id, prefix):
    id_part = str(device_id)[-4:] if len(str(device_id)) >= 4 else str(device_id)
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{id_part}-{random_part}"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚀 Internet Speed Bypass')
    btn2 = types.KeyboardButton('🔑 Voucher Code Hack')
    btn3 = types.KeyboardButton('👤 Contact Admin')
    markup.add(btn1, btn2, btn3)
    
    header = (
        f"╔════════════════════╗\n"
        f"     PAING GYI VIP TOOL\n"
        f"     DEVELOPER: {ADMIN_NAME}\n"
        f"╚════════════════════╝\n\n"
        f"Key ယူရန် အောက်က ခလုတ်ကို နှိပ်ပါဗျ။"
    )
    bot.send_message(message.chat.id, header, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack'])
def ask_for_id(message):
    prefix = "SPEED" if "Speed" in message.text else "VOUCH"
    msg = bot.send_message(message.chat.id, f"🆔 {message.text} အတွက် **Device ID** ကို ပို့ပေးပါဗျ။")
    bot.register_next_step_handler(msg, process_id, prefix)

def process_id(message, prefix):
    if message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '👤 Contact Admin', '/start']:
        bot.send_message(message.chat.id, "❌ ID မှားယွင်းနေပါသည်။ ID ကိုသာ ရိုက်ပို့ပေးပါဗျ။")
        return

    # [!] ဒီနေရာမှာ Voucher ကို 30 min အတိအကျ ပြင်လိုက်ပါပြီ
    if prefix == "SPEED":
        minutes = 120
    else:
        minutes = 30  # Voucher Hack အတွက် 30 မိနစ်

    final_key = generate_locked_key(message.text, prefix)
    expiry_time = (datetime.now() + timedelta(minutes=minutes)).strftime('%I:%M %p')

    result = (
        f"🔐 **{prefix} HACK SUCCESS**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Device ID: `{message.text}`\n"
        f"🔑 Your Key: `{final_key}`\n\n"
        f"⏰ Status: Active ({minutes} min)\n"
        f"⌛ Expiry: {expiry_time}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 Admin: {ADMIN_NAME}"
    )
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == '👤 Contact Admin')
def contact(message):
    bot.send_message(message.chat.id, f"👨‍💻 Developer: {ADMIN_NAME}\nTelegram: @PaingGyi")

bot.polling(none_stop=True)
