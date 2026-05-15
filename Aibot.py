Import telebot
import google.generativeai as genai
from telebot import types
import time

# --- API Keys ---
BOT_TOKEN = '8672537028:AAG0zs5ljD3MGjLaibW2IQpt1Sd5Ci7O0d4'
GEMINI_API_KEY = 'AIzaSyCtwqsq58drKdyxz7T5NLElvCKg_LGpHZY'

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

# ဆဲစာလုံးများ
bad_words = [
    'စောက်', 'လိုး', 'မအေလိုး', 'ဖာသည်', 'ဖာတန်း', 'မိဖာ', 'ဖာခေါင်း', 'နှမလိုး', 
    'ဘော', 'ဘောမ', 'စောက်ရူး', 'စောက်ပေါ', 'ငါးလိုး', 'ဂွေး', 'ခွေးမသား', 
    'မျိုးမစစ်', 'မအေဘေး', 'လီး', 'လီးပဲ', 'ပုထွေး', 'စောက်ဖုတ်', 'အဖုတ်', 
    'စောက်ပတ်', 'လိုးမသား', 'အေလိုး', 'မအေလိုးမ', 'လီးလား', 'စောက်ခွက်'
]

# --- ၁။ လူသစ်ဝင်လာလျှင် ကြိုဆိုခြင်း ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    group_name = message.chat.title if message.chat.title else "ကျွန်တော်တို့ Group"
    for new_user in message.new_chat_members:
        user_name = new_user.first_name
        welcome_text = (
            f"👋 Hello **{user_name}** ရေ...\n"
            f"ကျွန်တော်တို့ **{group_name}** chat Group မှ นွေးထွေးစွာ ကြိုဆိုပါတယ်ဗျ။ ✨\n\n"
            f"📌 ကျွန်တော်တို့ Group မှာ သိထားရမှာလေးတွေကတော့ -\n"
            f"❌ မဆဲရ၊ မရိုင်းရပါ။\n"
            f"🤝 Owner နှင့် Admin များကို လေးစားပါ။\n"
            f"⚠️ စည်းကမ်းဖောက်ဖျက်ပါက Group မှ အပြီးအပိုင် Ban ပါမည်။\n\n"
            f"ပျော်ရွှင်စွာ စကားပြောနိုင်ပါပြီခင်ဗျာ။"
        )
        try:
            bot.reply_to(message, welcome_text, parse_mode='Markdown')
        except: pass

# --- ၂။ AI & Bad Words Check ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not message.text: return
    clean_text = message.text.replace(" ", "").replace("\n", "").lower()
    
    if any(word in clean_text for word in bad_words):
        bot.reply_to(message, "❌ စည်းကမ်းချက်အရ မရိုင်းရပါဘူးဗျ။")
        return

    try:
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
    except Exception as e:
        print(f"AI Error: {e}")

if __name__ == "__main__":
    print("Aibot is running on Render...")
    bot.infinity_polling()
