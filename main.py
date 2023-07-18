import asyncio
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
import vk_api
import os
import requests

vk_token = 'YOUR VK TOKEN'
group_id = -#YOUR ID GROUP
telegram_token = 'YOUR TG TOKEN'

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

def get_last_posts(group_id, access_token, count=5):
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()

    response = vk.wall.get(owner_id=group_id, count=count)

    if response and 'items' in response:
        posts = response['items']
        result_posts = []
        for post in posts:
            post_text = post.get('text', '')
            attachments = post.get('attachments', [])
            photo_urls = []

            for attachment in attachments:
                if attachment['type'] == 'photo':
                    photo_url = max(attachment['photo']['sizes'], key=lambda x: x['width'])['url']
                    photo_urls.append(photo_url)

            result_posts.append((post_text, photo_urls))

        return result_posts

    return []

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

def add_user_to_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def delete_user_from_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await message.reply("Привет!")
    add_user_to_db(user_id)
    await message.reply("Теперь вы добавлены в базу данных!")

async def send_data_to_users():
    while True:
        posts = get_last_posts(group_id, vk_token, count=2)
        users = get_all_users()

        for user_id in users:
            try:
                for post_text, photo_urls in posts:
                    if post_text:
                        await bot.send_message(user_id, post_text)

                    for photo_url in photo_urls:
                        response = requests.get(photo_url)
                        with open('photo.jpg', 'wb') as file:
                            file.write(response.content)
                        with open('photo.jpg', 'rb') as file:
                            await bot.send_photo(user_id, file)

            except aiogram.utils.exceptions.ChatNotFound:
                print(f"User {user_id} is no longer accessible. Removing from the database.")
                delete_user_from_db(user_id)
            except Exception as e:
                print(f"An error occurred while sending data to user {user_id}: {e}")

        await asyncio.sleep(2 * 60 * 60)

async def on_startup(dp):
    create_db()
    asyncio.create_task(send_data_to_users())
    print("Бот запущен и готов к работе!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(dp))
    executor.start_polling(dp, skip_updates=True)
