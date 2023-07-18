import requests
import datetime

class VK:
    def __init__(self, token, USER_TOKEN):
        self.token = token
        self.user_token = USER_TOKEN

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
    