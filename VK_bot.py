import datetime
from random import randrange
from pprint import pprint
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from pprint import pprint
from config import user_token, group_token

class Vk:
    def __init__(self):
        self.token = group_token
        self.user_token = user_token
        print('Bot was created')
        self.vk_user = vk_api.VkApi(
            token=user_token)  # Создаем переменную сессии, авторизованную личным токеном пользователя.
        self.vk_user_got_api = self.vk_user.get_api()  # # переменную сессии vk_user подключаем к api списку методов.
        self.vk_group = vk_api.VkApi(token=group_token)  # Создаем переменную сесии, авторизованную токеном сообщества.
        self.vk_group_got_api = self.vk_group.get_api()  # переменную сессии vk_group подключаем к api списку методов.
        self.longpoll = VkLongPoll(self.vk_group)  # переменную сессии vk_group_got_api подключаем к Long Poll API,
        # позволяет работать с событиями из вашего сообщества в реальном времени.

    def send_msg(self, user_id, message):
        """method for sending messages"""
        self.vk_group_got_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7)
        )

    def get_info_user(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.token,
            'user_ids': user_id,
            'fields': 'sex, bdate, city',
            'v': '5.131'
        }
        result_info_user = requests.get(url, params).json()
        for item in result_info_user['response']:
            first_name = item['first_name']
            last_name = item['last_name']
            city = item['city']['title']
            sex = item['sex']
            if sex == 1:
                sex = 'м'
            else:
                sex = 'ж'
            bdate = item['bdate'].split('.')
            if len(bdate) == 3:
               date_now = datetime.date.today()
               age = date_now.year - int(bdate[2]) - ((date_now.month, date_now.day) < (int(bdate[1]), int(bdate[0])))
            else:
                bdate = None
                age = None
            link = 'https://vk.com/' + user_id
            self.send_msg(user_id,
                          f'   Кароче. Бот ищет людей вашего возраста, но в ваших настройках профиля установлен пункт "Показывать только месяц и день рождения"! \n'
                          f'   Поэтому, введите возраст поиска, на пример от 21 года и до 35 лет, в формате : 21-35 (или 21 конкретный возраст 21 год).'
                          )

            return first_name, last_name, city, sex, age, link
    

    def get_photo_user(self, user_id):
        url = 'https://api.vk.com/method/photos.getAll'
        params = {
            'access_token': self.user_token,
            'owner_id': user_id,
            'extended': '1',
            'v': '5.131'
        }
        result_photo_user = requests.get(url, params).json()
        photos = {}
        all_photo = result_photo_user['response']['items']
        for photo in all_photo:
            id_photo = photo['id']
            likes_photo = photo['likes']['count']
            photos[id_photo] = likes_photo

        photos_sort_key = sorted(photos, key=photos.get, reverse=True)
        sorted_photos = {}
        for i in photos_sort_key:
            sorted_photos[i] = photos[i]
        
        dict_id_photos = []
        for photo_id in sorted_photos.keys():
            dict_id_photos.append(photo_id)
        return dict_id_photos[:3]
vk = Vk()
print(vk.get_info_user('522161386'))