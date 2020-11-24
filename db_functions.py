""" Модуль для работы с базой данных. Используется MongoDB """


class BdError(Exception):
    """Класс для исключения при использовании бд"""
    def __init__(self, ex, text, bot_msg):
        self.ex = ex
        self.text = text
        self.bot_msg = bot_msg


def connect():
    """Подключаемся к нашей бд
       Функция возвращает объект, предствляющий базу данных"""
    try:
        import pymongo
        from passwords import mongodb_key
        client = pymongo.MongoClient(mongodb_key)
        db = client['Project_for_coffee_bot']   # Получаем базу данных
        print("Успешное подключение к базе данных")
        return db
    except Exception as ex:
        raise BdError(ex=ex, text="Ошибка подключения к базе данных!",
                      bot_msg="Ошибка подключения к базе данных.\nCтоит обратиться к "
                           "@tatyanagolovina1 или к @danya04. Сейчас можно воспользоваться командой /start")


def add_or_remove_request(name_of_office, call, bot):
    """Функция, которая проверяет есть ли уже заявка от другого человека или нет
       Если заявки нет, то создаётся таковая, иначе ...

    name_of_office - имя офиса (их два пока что); call - объект, с помощью которого мы
    получим id пользователя и его никнейм; bot - для отправки сообщений
    """

    try:
        db = connect()
        quantity_of_requests = db.posts.count({"name_of_office": name_of_office})   # Количество заявок в бд
        assert quantity_of_requests <= 1, "Количество заявок не может быть больше 2-ух"
        if quantity_of_requests == 1:  # Если заявка в данном офисе нашлась
            bot.send_message(call.message.chat.id,
                             "Поздравляю! Вы нашли партнера для перерыва ☕\n"
                             "Вот его контакт: @"
                             +str(db.posts.find_one({'name_of_office': name_of_office})['nickname']) + " 🚶")
            bot.send_message(db.posts.find_one({'name_of_office': name_of_office})['message_chat_id'],
                             "Поздравляю! Вы нашли партнера для перерыва ☕\n"
                             "Вот его контакт: @"+str(call.message.chat.username)+" 🚶")
            db.posts.delete_one({'name_of_office': name_of_office})
        else:
            new_request = {"message_chat_id": call.message.chat.id,
                           "name_of_office": name_of_office,
                           "nickname": call.message.chat.username
                           }
            bot.send_message(call.message.chat.id, "Ваша заявка отправлена!\nКак только сегодня "
                                                   "найдется второй желающий, я сразу сообщу. До связи!🙂\n")
            db.posts.insert_one(new_request)
    except BdError as ex:
        import logging
        logging.error(str(ex.text) + " " + str.capitalize(str(ex.ex)))
        bot.send_message(call.message.chat.id, ex.bot_msg)
    except Exception as ex:
        import logging
        logging.error("\nОшибка в add_or_remove_request! "+ str(ex))
        bot.send_message(call.message.chat.id, "Произошла ошибка, связанная с базой данных,"
                                               " стоит обратиться к @tatyanagolovina1 или к @danya04."
                                               "Сейчас можно воспользоваться командой /start")