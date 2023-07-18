from VK import VK

with open('config/user_token.txt', 'r') as file:
    user_token = file.read().strip()

with open('config/community_token.txt', 'r') as file:
    community_token = file.read().strip() 

def main():
    vk = VK(community_token, user_token)
    first_name, last_name, city, sex, age, link = VK.get_info_user(vk, '1')
    dict_photos = VK.get_photo_user(vk, '1')
    

if __name__ == '__main__':
    main()