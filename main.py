import telebot
import requests

# ------ بياناتك الأساسية (لا تغيرها) ------
TOKEN = "8035809373:AAFkp1i0ONNcZhB-D7zaBCqkP64w5Zi_GBY"  # توكن بوتك
FOX_API_KEY = "0l6cjrz8ujku49lp2slw"  # مفتاح API من fox-tg
# ------------------------------------------

bot = telebot.TeleBot(TOKEN)

# ----- تحسينات الأمان والأداء -----
def fetch_fox_api(action, params=None):
    try:
        url = f"https://api.fox-tg.com?apiKay={FOX_API_KEY}&action={action}"
        if params:
            for key, value in params.items():
                url += f"&{key}={value}"
        response = requests.get(url, timeout=10)  # مهلة 10 ثواني
        return response.json() if response.status_code == 200 else None
    except:
        return None

# ------ الأوامر الرئيسية ------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = """
مرحبًا بك في البوت! 🚀
الأوامر المتاحة:
/balance - رصيدك الحالي
/countries - الدول المتاحة
"""
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['balance'])
def get_balance(message):
    data = fetch_fox_api("getBalance")
    if data:
        bot.reply_to(message, f"💰 الرصيد: {data.get('balance', 'غير متاح')}")
    else:
        bot.reply_to(message, "❌ فشل في جلب الرصيد")

@bot.message_handler(commands=['countries'])
def get_countries(message):
    data = fetch_fox_api("getCountrys")
    if data and 'countries' in data:
        countries_list = "\n".join(data['countries'])
        bot.reply_to(message, f"🌍 الدول المتاحة:\n{countries_list}")
    else:
        bot.reply_to(message, "❌ فشل في جلب القائمة")

# ------ تشغيل البوت ------
print("✅ البوت يعمل الآن! اضغط STOP لإيقافه.")
bot.polling()
