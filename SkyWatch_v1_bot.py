import os
import telebot
from telebot import types
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')
POLLING_TIMEOUT = None
bot = telebot.TeleBot(BOT_TOKEN)

# دیکشنری برای ذخیره اطلاعات زیرمجموعه‌ها
user_subscribers = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
    ارسال پیام خوشامدگویی و دکمه‌های شیشه‌ای برای دسترسی به امکانات مختلف
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    # دکمه‌ها
    button_weather = types.KeyboardButton(text="آب و هوا")
    button_about = types.KeyboardButton(text="درباره ربات")
    button_zir = types.KeyboardButton(text="حساب کاربری من")
    button_poshtiban = types.KeyboardButton(text="پشتیبانی")
    button_invite = types.KeyboardButton(text="معرفی به دوستان")

    # افزودن دکمه‌ها به کیبورد
    markup.add(button_weather, button_about, button_zir, button_poshtiban, button_invite)

    # ارسال پیام خوشامدگویی و کیبورد
    bot.send_message(message.chat.id, 'سلام به ربات SkyWatch خوش آمدید! '
                                      'لطفاً یکی از گزینه‌ها را انتخاب کنید:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "حساب کاربری من")
def user_account(message):
    '''
    نمایش اطلاعات حساب کاربری و تعداد زیرمجموعه‌ها
    '''
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.username

    account_message = f"""
    🔑 اطلاعات حساب کاربری شما:
    - نام کاربری: {first_name} {last_name if last_name else ''}
    - شناسه کاربری تلگرام: @{user_name if user_name else 'بدون نام کاربری'}
    - آیدی تلگرام: {user_id}
    """

    # ارسال اطلاعات حساب کاربری به کاربر
    bot.send_message(message.chat.id, account_message)


@bot.message_handler(func=lambda message: message.text == "بازگشت")
def back_to_main(message):
    '''
    بازگشت به منوی اصلی
    '''
    send_welcome(message)  # نمایش دوباره منوی اصلی


@bot.message_handler(func=lambda message: message.text == "درباره ربات")
def about(message):
    '''
    ارسال اطلاعات درباره ربات
    '''
    about_message = """
    این ربات به شما کمک می‌کند تا وضعیت آب و هوا را بر اساس موقعیت مکانی خود مشاهده کنید.
    لطفاً یک موقعیت مکانی وارد کنید تا اطلاعات آب و هوا برای آن مکان دریافت شود.

    برای ارتباط با توسعه‌دهنده، به این لینک مراجعه کنید: 
    [GitHub](https://github.com/arshiakia/SkyWatch_bot)


    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_back = types.KeyboardButton(text="بازگشت")
    markup.add(button_back)

    # ارسال پیام درباره ربات و دکمه بازگشت
    bot.send_message(message.chat.id, about_message, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text == "معرفی به دوستان")
def invite(message):
    '''
    ارسال لینک دعوت اختصاصی به کاربر
    '''
    user_id = message.from_user.id
    invite_link = f"https://t.me/SkyWatch_v1_bot?start={user_id}"

    invite_message = f"""
    🎉 ربات SkyWatch به شما کمک می‌کند تا وضعیت آب و هوا را بر اساس موقعیت مکانی خود مشاهده کنید!

    🌍 برای استفاده از ربات، روی لینک زیر کلیک کنید و دوستان خود را هم به این ربات دعوت کنید:

    👉 [دعوت به ربات SkyWatch](https://t.me/SkyWatch_v1_bot?start={user_id})

    با دعوت از دوستان خود، می‌توانید از ویژگی‌های ویژه‌تر ربات بهره‌مند شوید. 🌟
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_back = types.KeyboardButton(text="بازگشت")
    markup.add(button_back)

    # ارسال پیام لینک دعوت و دکمه بازگشت
    bot.send_message(message.chat.id, invite_message, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text == "پشتیبانی")
def support(message):
    '''
    ارسال لینک پشتیبانی تلگرام و گیت‌هاب به کاربر
    '''
    support_message = """
    برای ارتباط با پشتیبانی، به یکی از لینک‌های زیر مراجعه کنید:

    - پشتیبانی در تلگرام: [تلگرام](https://t.me/Arshia_kia1)
    - پشتیبانی در گیت‌هاب: [گیت‌هاب](https://github.com/arshiakia)
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_back = types.KeyboardButton(text="بازگشت")
    markup.add(button_back)

    # ارسال پیام پشتیبانی و دکمه بازگشت
    bot.send_message(message.chat.id, support_message, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda message: message.text == "آب و هوا")
def send_weather_options(message):
    '''
    ارسال گزینه‌ها برای انتخاب آب و هوا (ارسال لوکیشن یا انتخاب شهر)
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    # دکمه‌ها
    button_location = types.KeyboardButton(text="موقعیت مکانی هوشمند")
    button_city = types.KeyboardButton(text="انتخاب شهر به صورت دستی")
    button_back = types.KeyboardButton(text="بازگشت")

    # افزودن دکمه‌ها به کیبورد
    markup.add(button_location, button_city, button_back)

    # ارسال پیام با دکمه‌های جدید
    bot.send_message(message.chat.id, "لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)


bot.infinity_polling()
