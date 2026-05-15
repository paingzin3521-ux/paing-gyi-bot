import telebot
import google.generativeai as genai
from telebot import types
import os
from flask import Flask
from threading import Thread

# --- Flask Web Server Setup (Render Free Web Service အတွက် Port အလုပ်လုပ်အောင် လုပ်ခြင်း) ---
app = Flask('')

@app.route('/')
def home():
    return "StarLink AI Bot is Running Successfully!"

def run():
    # Render က ပေးမယ့် Port သို့မဟုတ် ပုံမှန် Port 8080 ကို သုံးမယ်
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- API Keys ---
BOT_TOKEN = '8672537028:AAG0zs5ljD3MGjLaibW2IQpt1Sd5Ci7O0d4'
GEMINI_API_KEY = 'AIzaSyCtwqsq58drKdyxz7Ww100N5XU-F3N6zU8'

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

# ဆဲစာလုံးများ
bad_words = [
    'စောက်', 'လိုး', 'မအေလိုး', 'ဖာသည်', 'ဖာတန်း', 'မိဖာ', 'ဖာخောင်း', 'နှမလိုး', 
    'ဘော', 'ဘောမ', 'စောက်ရူး', 'စောက်ပေါ', 'ငါးလိုး', 'ဂွေး', 'ခွေးမသား', 
    'မျိုးမစစ်', 'မအေဘေး', 'လီး', 'လီးပဲ', 'ပုထွေး', 'စောက်ဖုတ်', 'အဖုတ်', 
    'စောက်ပတ်', 'လိုးမသား', 'အေလိုး', 'မအေလိုးမ', 'လီးလား', 'စောက်ခွက်'
]

def is_user_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['creator', 'administrator']
    except:
        return False

# --- ၁။ လူသစ်ဝင်လာလျှင် ကြိုဆိုခြင်း ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    group_name = message.chat.title if message.chat.title else "ကျွန်တော်တို့ Group"
    for new_user in message.new_chat_members:
        if new_user.id == bot.get_me().id: continue
        
        user_name = new_user.first_name
        user_id = new_user.id
        welcome_text = (
            f"👋 Hello **{user_name}** (ID: `{user_id}`) ရေ...\n"
            f"ကျွန်တော်တို့ **{group_name}** chat Group မှ နွေးထွေးစွာ ကြိုဆိုပါတယ်ဗျ။ ✨\n\n"
            f"📌 Group မှာ သိထားရမှာလေးတွေကတော့ -\n"
            f"❌ မဆဲရ၊ မရိုင်းရပါ။\n"
            f"🤝 Owner နှင့် Admin များကို လေးစားပါ။\n"
            f"⚠️ စည်းကမ်းဖောက်ဖျက်ပါက Group မှ အပြီးအပိုင် Ban ပါမည်။\n\n"
            f"ပျော်ရွှင်စွာ စကားပြောနိုင်ပါပြီခင်ဗျာ။"
        )
        try:
            bot.reply_to(message, welcome_text, parse_mode='Markdown')
        except: pass

# --- ၂။ Admin Commands System (/ban, /unban, /mute, /unmute) ---
@bot.message_handler(commands=['ban', 'unban', 'mute', 'unmute'])
def admin_commands(message):
    if message.chat.type == "private": return
    
    if not is_user_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ ဒီ Command ကို သုံးခွင့်ရှိတာ Admin များသာ ဖြစ်ပါတယ်ဗျ။")
        return
        
    command = message.text.split()[0].lower()

    if command == '/unban':
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "⚠️ Ban ပြန်ဖြုတ်ဖို့အတွက် `/unban [သူ့ရဲ့ Telegram ID]` ဟု တွဲရိုက်ပေးပါဗျာ။\nဥပမာ - `/unban 123456789`", parse_mode='Markdown')
            return
        
        target_id = args[1]
        try:
            bot.unban_chat_member(message.chat.id, target_id)
            bot.reply_to(message, f"✅ **Ban ဖြုတ်လိုက်ပြီ!**\n🆔 **User ID:** `{target_id}`\n\nဤ ID ပိုင်ရှင်ကို Group ထဲ ပြန်ဝင်ခွင့် ပြုလိုက်ပါပြီဗျာ။", parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, "❌ Error: ID မှားနေခြင်း (သို့မဟုတ်) Bot မှာ Permission မရှိလို့ ဖြစ်နိုင်ပါတယ်ဗျာ။")
        return

    if not message.reply_to_message:
        bot.reply_to(message, f"⚠️ ဒီ `{command}` Command ကို သုံးဖို့အတွက် အရေးယူချင်တဲ့သူရဲ့စာကို Reply ပြန်ပြီး ရိုက်ပေးပါဗျာ။", parse_mode='Markdown')
        return
        
    target_user = message.reply_to_message.from_user
    t_name = target_user.first_name
    t_id = target_user.id
    
    try:
        if command == '/ban':
            bot.ban_chat_member(message.chat.id, t_id)
            bot.reply_to(message, f"🚨 **Ban လိုက်ပြီ!**\n👤 **Name:** {t_name}\n🆔 **User ID:** `{t_id}`\n\nဒီလူကို Group ထဲကနေ အပြီးအပိုင် မောင်းထုတ် (Ban) လိုက်ပါပြီဗျာ။", parse_mode='Markdown')
            
        elif command == '/mute':
            readonly_perms = types.ChatPermissions(
                can_send_messages=False, can_send_media_messages=False,
                can_send_polls=False, can_send_other_messages=False
            )
            bot.restrict_chat_member(message.chat.id, t_id, permissions=readonly_perms)
            bot.reply_to(message, f"🔇 **Mute လိုက်ပြီ!**\n👤 **Name:** {t_name}\n🆔 **User ID:** `{t_id}`\n\nဒီလူကို စာရိုက်ခွင့် (Mute) ပိတ်လိုက်ပါပြီဗျာ။", parse_mode='Markdown')
            
        elif command == '/unmute':
            normal_perms = types.ChatPermissions(
                can_send_messages=True, can_send_media_messages=True,
                can_send_polls=True, can_send_other_messages=True
            )
            bot.restrict_chat_member(message.chat.id, t_id, permissions=normal_perms)
            bot.reply_to(message, f"🔊 **Mute ဖြုတ်လိုက်ပြီ!**\n👤 **Name:** {t_name}\n🆔 **User ID:** `{t_id}`\n\nဒီလူကို စာပြန်ရိုက်ခွင့် ပြန်ဖွင့်ပေးလိုက်ပါပြီဗျာ။", parse_mode='Markdown')
            
    except Exception as error:
        bot.reply_to(message, f"❌ Error: Bot မှာ Admin Permission မပြည့်စုံသေးလို့ ဖြစ်နိုင်ပါတယ်ဗျာ။")

# --- ၃။ AI & Bad Words Check ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not message.text: return
    
    clean_text = message.text.replace(" ", "").replace("\n", "").lower()
    
    if any(word in clean_text for word in bad_words):
        bot.reply_to(message, "❌ စည်းကမ်းချက်အရ မရိုင်းရပါဘူးဗျ။")
        return

    bot_info = bot.get_me()
    bot_username = bot_info.username.lower() if bot_info.username else "bot"
    
    is_reply_to_bot = False
    if message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id:
        is_reply_to_bot = True

    has_bot_keyword = "bot" in clean_text or bot_username in clean_text
    is_private_chat = message.chat.type == "private"

    if has_bot_keyword or is_reply_to_bot or is_private_chat:
        try:
            user_question = message.text.lower().replace("bot", "").replace(f"@{bot_username}", "").strip()
            if not user_question: 
                user_question = "ဗျာ... ဘာခိုင်းမလို့လဲဗျာ?"
                
            response = model.generate_content(user_question)
            if response.text:
                bot.reply_to(message, response.text)
        except Exception as e:
            print(f"AI Error: {e}")

if __name__ == "__main__":
    print("Starting Web Server Keep-Alive...")
    keep_alive()  # Web server ကို နောက်ကွယ်ကနေ Run ပေးထားခြင်း
    print("Aibot with Web Service Compatibility is running...")
    bot.infinity_polling()
