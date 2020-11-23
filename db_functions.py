""" Модуль для работы с базой данных. Используется MongoDB """


def connect():
    """Подключаемся к нашей бд
       Функция возвращает объект, предствляющий базу данных"""
    try:
        import pymongo
        from passwords import mongodb_key
        client = pymongo.MongoClient(mongodb_key)
        db = client['PROJECT_FOR_COFFEE_BOT']   # Получаем базу данных
        print("Успешное подключение к базе данных")
        return db
    except Exception as ex:
        import logging
        logging.error(ex)


def add_or_remove_request(name_of_office, call, bot):
    """Функция, которая проверяет есть ли уже заявка от другого человека или нет
       Если заявки нет, то создаётся таковая, иначе ...

    name_of_office - имя офиса (их два пока что); call - объект, с помощью которого мы
    получим id пользователя и его никнейм; bot - для отправки сообщений
    """

    try:
        db = connect()
        #for instance in db.posts.find({}):
         #   print(instance)
        # a = db.posts.count({"name_of_office": name_of_office})
        # print(a)
        print(db.posts.count({"name_of_office": name_of_office}), " <- amount requests")
        if not (db.posts.count({"name_of_office": name_of_office})):  # Если заявка в данном офисе нашлась
            bot.send_message(call.message.chat.id, "Поздравляю! Ты нашёл партнера для перерыва")
            # bot.send_message(element_in_db("message_chat_id"), "Поздравляю! Ты нашёл партнера для перерыва")
            # db.posts.delete_one(element_in_db)
        else:
            new_request = {"message_chat_id": call.message.chat.id,
                           "name_of_office": name_of_office,
                           "leader_name": call.message.chat.username
                           }
            print("Вставляем заявку")
            db.posts.insert_one(new_request)
    except Exception as ex:
        import logging
        logging.error("\nОшибка в add_or_remove_request! "+ str(ex))