""" Скрипт, предназначенный для запуска в конце рабочего дня и удаления неактуальных заявок """


def delete_irrelevant_requests():
    """Функция, которая удаляет неактуальные заявки и информирует от этом.
       Запускается сервером в конце рабочего дня"""

    import telebot
    import passwords
    bot = telebot.TeleBot(passwords.key)
    from db_functions import connect
    try:
        db = connect()
        for instance in db.posts.find({}):
            bot.send_message(instance['message_chat_id'], "🌃 Увы, сегодня вам не нашлось пары 🌃\n"
                                                          "🌅 Отправь новую заявку завтра! (/start) 🌅")
            db.posts.delete_one(instance)
    except Exception as ex:
        import logging
        logging.error("Ошибка удаления:" + str(ex))


delete_irrelevant_requests()
