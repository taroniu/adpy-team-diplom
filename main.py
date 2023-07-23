from VK_bot import *
import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import user_token, group_token


with open('config/user_token.txt', 'r') as file:
    user_token = file.read().strip()

with open('config/community_token.txt', 'r') as file:
    community_token = file.read().strip()


def main():
    vk = Vk()
    first_name, last_name, city, sex, age, link = Vk.get_info_user(vk, '1')
    dict_photos = Vk.get_photo_user(vk, '1')


# if __name__ == '__main__':
#     print(main())



#
# user_token = ""
# group_token = ''

session = vk_api.VkApi(token=user_token)
user_bot = session.get_api()

group_session = vk_api.VkApi(token=group_token)
group_bot = group_session.get_api()
longpoll = VkLongPoll(group_session)


def user_send_message(user_id, message):
    session.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': 0
    })
def group_send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': 0,
        # 'attachment': None
    }
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post
    group_session.method('messages.send', post)

def send_photo(user_id, message, attachments):
    """method for sending photos"""
    try:
        group_bot.messages.send(
            user_id=user_id,
            message=message,
            random_id=randrange(10 ** 7),
            attachment=attachments
            # attachment=",".join(attachments)
        )
    except TypeError:
        pass

def get_user_info(user_id):
    info = session.method('users.get', {'user_ids': user_id})
    return f"{info[0]['first_name']} {info[0]['last_name']}"

def get_hometown():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                user_id = event.user_id
                request = event.text
                group_send_message(user_id, 'Укажите возраст')
                hometown = request
                return hometown

def get_sex():
    fields = ['sex']
    info = session.method('users.get', { 'fields': fields})
    if info[0]['sex'] == 1:
        return 2
    else:
        return 1

def birth_year():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_id = event.user_id
                request = event.text.lower()
                try:
                    age = int(request)
                    birth_year = 2023 - age
                    group_send_message(user_id, f'age is {age}')
                    group_send_message(user_id, f'birth year is {birth_year}')
                    group_send_message((user_id, 'Начинаем поиск'))
                except:
                    group_send_message(user_id, f'input number')
                print(request)
                return birth_year
                # year_of_birth = 2023 - int(age)

def searching_users():
    fields = ['can_write_private_message, city, sex, can_see_all_posts, birth_year']
    city = 'Омск'
    sex = get_sex()
    status = 6
    # birth_year = birth_year()
    count = 50
    users = session.method('users.search', { 'hometown': get_hometown(), 'sex': sex, 'birth_year': birth_year(), 'count': count, 'fields': fields})
    # print(users)
    users_ids = []
    for i in users['items']:
        if i['can_see_all_posts'] == 1 and i['can_access_closed'] == True and i['can_write_private_message'] == 1:
            us_id = i['id']
            # print(i)
            photos = session.method('photos.get', {'owner_id': i['id'], 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1})
            name = i['first_name']
            last_name = i['last_name']
            sex = i['sex']
            # city = i['city']['id']
            # city_name = i['city']
            i['link'] = f'https://vk.com/id{us_id}'
            info = session.method('users.get')
            user_id = info[0]['id']
            # group_send_message(user_id, f'{name} {last_name} \n {i["link"]}')
            pprint(f'{name} {last_name} \\n {i["link"]}')
            #находим самые популярные фото профиля и удаляем остальные.
            photos_items_list = photos['items']
            newlist = sorted(photos_items_list, key=lambda d: d['likes']['count'])
            while len(newlist) > 3:
                newlist.pop()
            # извлекаем список со ссылками на фото и оставляем только самый большой размер.
            sizes_list = []
            max_size_link = []
            for j in newlist:
                sizes_list += j['sizes']
            for j in sizes_list:
                if j['type'] == 'z':
                 max_size_link.append(j['url'])
            pprint(newlist)
            pprint(max_size_link)
            # attachment = ",".join(attachments)
            group_send_message(user_id, f'{name} {last_name} \n {i["link"]}')
            send_photo(user_id, 'message', max_size_link)


def work():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                user_id = event.user_id
                request = event.text.lower()
                group_send_message(user_id, f'''Здарова, {get_user_info(user_id)}! 
                Этот бот поможет тебе найти девушку или парня из твоего города или из другого города.
                Для начала нажми "Искать".''')
                # if request == 'искать':

                keyboard = VkKeyboard()
                keyboard.add_location_button()
                keyboard.add_line()

                keyboard.add_button('искать', VkKeyboardColor.PRIMARY)
                buttons = ['blue', 'white', 'red', 'green']
                button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.SECONDARY, VkKeyboardColor.NEGATIVE, VkKeyboardColor.POSITIVE]
                for btn, btn_color in zip(buttons, button_colors):
                    keyboard.add_button(btn, btn_color)

                if request == 'искать':


                    group_send_message(user_id, 'Ты нажал кнопку "Искать" ', keyboard)
                    group_send_message(user_id, 'Сначала укажите город')
                    searching_users()
                if request == 'blue':
                    group_send_message(user_id, 'Вы нажали синюю')
                if request == 'white':
                    group_send_message(user_id, 'Вы нажали белую')
                if request == 'red':
                    group_send_message(user_id, 'Ты нажал красную')
                if request == 'green':
                    group_send_message(user_id, 'Ты нажал зеленую')

# get_user_status(459571744)
# send_message(38863174)
# set_user_status()

# searching_users()
work()
# print(get_sex())

# birth_year()