import os.path
import requests
from vk_config import group_token_vk, user_token_vk, V
from function_base import *

class VK_USER:
    def __init__(self, group_token_vk, user_token_vk, id):
        self.group_token_vk = group_token_vk
        self.user_token_vk = user_token_vk
        self.id = id
        self.name_city = []
        self.sex = []
        self.bdate = []
        self.relation = []
        self.city = []
        self.id_users = []


    def request_parameters_user(self, id):  # сбор информации о пользователе ВК
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': group_token_vk, 'user_ids': id, 'fields': 'bdate,city,sex,relation', 'v': V}
        response = requests.get(url=url, params=params)
        link_load = response.json()
        for link in link_load['response']:
            self.relation = link['relation']
            self.city = link['city']['id']
            self.name_city = link['city']['title']
            if link['sex'] == '1':
                self.sex = '2'
            else:
                self.sex = '1'
            a = link['bdate']
            b = a.split('.')
            self.bdate = 2022 - int(b[2])
        if os.path.exists('VKinder.db'):
            delete_table1()
            delete_table2()

        else:
            create_table()
        zapolnenie_table1(id, self.name_city, self.relation, self.bdate)

    def request_users(self):  # поиск пользователей по параметрам пользователя ВК
        url = 'https://api.vk.com/method/users.search'
        params = {'access_token': user_token_vk, 'sort': '0', 'has_photo': '1', 'count': '5', 'city': self.city,
                  'sex': self.sex, 'status': self.relation, 'age_from': '20', 'age_to': self.bdate, 'v': V}
        response = requests.get(url=url, params=params)
        link_load = response.json()
        for link in link_load['response']['items']:
            if link['can_access_closed'] == True:
                self.id_users.append(link['id'])





    def users_foto_vk(self):  # получение топ-3 фотографий найденых пользователей
        for id_users in self.id_users:
            link_user = f'vk.com/id{id_users}'
            temporary_sizes = []
            temporary_url = []
            comments_user = []
            likes_user = []
            url = 'http://api.vk.com/method/photos.get'
            params = {'album_id': 'profile', 'extended': '1', 'photo_sizes': '1',
                      'owner_id': id_users, 'access_token': user_token_vk, 'v': V}
            response = requests.get(url=url, params=params)
            link_load = response.json()

            for link in link_load['response']['items']:  # создание списков  url
                max_dpi = 0
                element_url = 0
                element_type = 0
                b = 0
                c = 0
                for s, likes in link['likes'].items():
                    b += likes
                likes_user.append(b)
                for s, likes in link['comments'].items():
                    c += likes
                comments_user.append(c)
                for sizes in link['sizes']:
                    if sizes['height'] > 0 and sizes['height'] > 0:
                        dpi = sizes['height'] * sizes['height']
                        if dpi > max_dpi:
                            max_dpi = dpi
                            element_url = sizes['url']
                    elif sizes['type'] == 'x':
                        temporary_url.append(sizes['url'])
                temporary_url.append(element_url)
                temporary_sizes.append(element_type)

            likes_comments = [x + y for x, y in zip(comments_user, likes_user)]  # подсчитывание лайков и комментариев
            list_1 = list(zip(temporary_url, likes_comments))
            sorted_q = sorted(list_1, key=lambda x: x[1])

            if len(sorted_q) > 2:  # Заполнение таблицы 'Результаты поиска'
                value1 = list(sorted_q[-1])
                value2 = list(sorted_q[-2])
                value3 = list(sorted_q[-3])
                foto1 = value1[0]
                foto2 = value2[0]
                foto3 = value3[0]
                zapolnenie_table2(id_users, link_user, foto1, foto2, foto3)
            elif len(sorted_q) <= 2:
                importance = sorted_q[0]
                foto1 = importance[0]
                zapolnenie_table2(id_users, link_user, foto1, 'Фотография отсутствует', 'Фотография отсутствует')
