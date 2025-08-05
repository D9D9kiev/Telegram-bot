import telebot
from telebot import types
from routes import routes
from flask import Flask
from threading import Thread

TOKEN = '8038235760:AAHd3KiFuRitaT4LtLgFhxfeXTuVVr12h_E'
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# === Flask сервер для keep-alive ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === Меню ===
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🗺 Маршрути"))
    return markup

def back_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup

# === Обробка команд ===
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 Вітаю! Оберіть, що хочете переглянути:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "🗺 Маршрути")
def show_routes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in routes.keys():
        markup.add(types.KeyboardButton(name))
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "🚌 Доступні маршрути:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_menu(message):
    bot.send_message(message.chat.id, "🔙 Повертаємось в головне меню:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text in routes)
def route_info(message):
    data = routes[message.text]
    if isinstance(data, dict) and "details" in data:
        bot.send_message(message.chat.id, data["details"], reply_markup=back_menu())
    elif isinstance(data, list):
        message_text = "🚍 *{}*\n\n".format(message.text) + "\n".join(data)
        bot.send_message(message.chat.id, message_text, reply_markup=back_menu())
    else:
        bot.send_message(message.chat.id, "⚠️ Дані маршруту не знайдено.", reply_markup=back_menu())

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(message.chat.id, "⚠️ Не розумію запит. Скористайтесь меню.", reply_markup=main_menu())

# === Запуск ===
keep_alive()
bot.polling()