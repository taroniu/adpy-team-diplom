
import VK_bot
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from VK_bot import *

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


import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

user_token = ""
group_token = ''

session = vk_api.VkApi(token=user_token)
user_bot = session.get_api()

group_session = vk_api.VkApi(token=group_token)
group_bot = group_session.get_api()
longpoll = VkLongPoll(group_session)


def user_send_message(user_id, message):
    session.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    })
def group_send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7),
    }

    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post
    group_session.method('messages.send', post)

def get_user_status(user_id):
    status = session.method('status.get', {'user_id': user_id})
    # print(status)
    # friends = session.method('friends.get', {'user_id': user_id})
    # print(friends)
    # for friend in friends['items']:
    #     user = session.method('users.get', {'user_ids': friend})
    #     # print(user[0]['first_name'], user[0]['last_name'], )
    #     status = session.method('status.get', {'user_id': friend})
        # print(user[0]['first_name'], user[0]['last_name'], status['text'])

def get_user_info(user_id):
    info = session.method('users.get', {'user_ids': user_id})
    return f"{info[0]['first_name']} {info[0]['last_name']}"

def set_user_status():
    user_bot.status.set(text='Суперстатус')


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

            keyboard.add_button('Искать', VkKeyboardColor.PRIMARY)
            buttons = ['blue', 'white', 'red', 'green']
            button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.SECONDARY, VkKeyboardColor.NEGATIVE, VkKeyboardColor.POSITIVE]
            for btn, btn_color in zip(buttons, button_colors):
                keyboard.add_button(btn, btn_color)

            if request == 'искать':
                group_send_message(user_id, 'Ты нажал кнопку "Искать" ', keyboard)
            if request == 'blue':
                group_send_message(user_id, 'Вы нажали синюю')
            if request == 'white':
                group_send_message(user_id, 'Вы нажали белую')
            if request == 'red':
                group_send_message(user_id, 'Ты нажал красную')
            if request == 'green':
                group_send_message(user_id, 'Ты нажал зеленую')
                