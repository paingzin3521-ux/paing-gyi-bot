import telebot
from telebot import types
import random
import string
from datetime import datetime, timedelta

# [!] Paing Gyi ရဲ့ Token ကို ဒီမှာ ထည့်ပါ
TOKEN = "8557413081:AAH5eWNAVr9U8TN6M3SywY34O4Ooy7gWJZc"
bot = telebot.TeleBot(TOKEN)

# [!] Paing Gyi ရဲ့ Telegram ID ကို ဒီမှာ ထည့်ပါ
ADMIN_ID = 1000037717 
# Admin နာမည်အသစ်
ADMIN_NAME = "Pᴀɪɴɢ Zɪɴ Aᴜɴɢ X"

def generate_locked_key(device_id, prefix):
    id_part = str(device_id)[-4:] if len(str(device_id)) >= 4 else str(device_id)
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{id_part}-{random_part}"

@bot.message_handler(commands=['start'])
def start(message):
    status = "👑 Admin" if message.from_user.id == ADMIN_ID else "👤 User"
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚀 Internet Speed Bypass')
    btn2 = types.KeyboardButton('🔑 Voucher Code Hack')
    markup.add(btn1, btn2)
    
    welcome = (
        f"🌟 **PAING GYI VIP KEY BOT**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Admin: {ADMIN_NAME}\n"
        f"💎 Status: {status}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Key ယူလိုပါက အောက်က ခလုတ်ကို နှိပ်ပါဗျ။"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack'])
def ask_for_id(message):
    prefix = "SPEED" if "Speed" in message.text else "VOUCH"
    msg = bot.send_message(message.chat.id, f"🆔 {message.text} အတွက် **Device ID** ကို ပို့ပေးပါဗျ။")
    bot.register_next_step_handler(msg, process_id, prefix)

def process_id(message, prefix):
    device_id = message.text
    
    # ခလုတ်စာသားတွေ မှားဝင်လာရင် ပယ်ချမယ်
    if device_id in ['🚀 Internet Speed Bypass', '🔑 Voucher Code Hack', '/start']:
        bot.send_message(message.chat.id, "❌ ID မှားယွင်းနေပါသည်။ ခလုတ်မဟုတ်ဘဲ ID ကိုသာ ရိုက်ပို့ပေးပါဗျ။")
        return

    # Speed ဆိုရင် ၁၂၀ မိနစ်၊ Voucher ဆိုရင် ၃၀ မိနစ်
    minutes = 120 if prefix == "SPEED" else 30
    final_key = generate_locked_key(device_id, prefix)
    expiry_time = (datetime.now() + timedelta(minutes=minutes)).strftime('%I:%M %p')

    result = (
        f"🔐 **{prefix} HACK SUCCESS**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Device ID: `{device_id}`\n"
        f"🔑 Your Key: `{final_key}`\n\n"
        f"⏰ သက်တမ်း: {minutes} မိနစ် ({expiry_time} အထိ)\n"
        f"⚠️ ဤ Key ကို မိမိ ID အတွက်သာ သုံးပါ!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 Admin: {ADMIN_NAME}"
    )
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

print(f"Bot started by {ADMIN_NAME}")
bot.polling(none_stop=True)
