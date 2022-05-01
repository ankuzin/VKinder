from vk_config import group_token_vk, user_token_vk
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from function_vk import VK_USER
import sqlite3 as sql

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), })

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=group_token_vk)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)

        if event.to_me:
            # Сообщение от пользователя
            request = event.text
            # Каменная логика ответа
            if len(request) == 10 or len(request) == 11:
                ya = VK_USER(group_token_vk=group_token_vk, user_token_vk=user_token_vk, id=request)
                ya.request_parameters_user(id=request)
                ya.request_users()
                ya.users_foto_vk()
                connection = sql.connect('VKinder.db')
                with connection:
                    cur = connection.cursor()
                    value1 = (cur.execute("SELECT * FROM 'searching_results'").fetchall())
                    write_msg(event.user_id, f'Показываю пользователей которые вам подходят')
                    for value2 in value1:
                        for value3 in value2:
                            write_msg(event.user_id, {value3})
                connection.commit()
                cur.close()
            else:
                write_msg(event.user_id, "Для подбора пользователей введите свой id")
