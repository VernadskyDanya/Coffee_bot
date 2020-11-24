"""Главный файл программы, запускает телеграм-бота и указывает как и чем обрабатывать все кнопки"""
import telebot
import passwords
bot = telebot.TeleBot(passwords.key)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Хендлер на команду /start"""
    bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name) +"\n"
                     "С помощью меня вы сможете найти компаньона для чашки кофе или чая.\nЕсли заявка не найдет "
                     "отклика в течение дня (до чч:чч), то я её <b>отменю</b> и вам нужно "
                     "будет <b>сделать новую</b>\nВы всегда можете вернуться в меню командой /start", parse_mode='HTML')
    from bot_functions import start
    start(message.chat.id, bot)


import bot_functions
import db_functions
# Константный набор кнопок и соответствующих функций (ожидаемых реакций)
FUNCTIONS = dict(start=bot_functions.start,
                 coffee=bot_functions.choose_department,
                 big_morsk=(db_functions.add_or_remove_request, "big_morsk"),
                 small_morsk=(db_functions.add_or_remove_request, "small_morsk"))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработик inline-кнопок"""
    try:
        if type(FUNCTIONS[call.data]) is tuple:     # Если у функции есть доп параметр: например имя офиса
            print("Вызывается функция с доп параметром")
            FUNCTIONS[call.data][0](FUNCTIONS[call.data][1], call, bot)
        else:   # Если у функции нет доп параметра
            FUNCTIONS[call.data](call.message.chat.id, bot)
    except Exception as ex:
        import logging
        logging.critical(ex)
        logging.critical(" Ошибка в callback_query_handler")


bot.polling(none_stop=False, interval=0, timeout=20)