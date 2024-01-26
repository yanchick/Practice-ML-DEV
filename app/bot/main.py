import os
import requests
import telebot
from telebot import types
import pandas as pd
import io

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BACKEND_URL = os.environ.get('BACKEND_URL')
 
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message)
    if message.text == '/start':
        # Сохраним пользователя в БД
        response = requests.get(f"{BACKEND_URL}/user/{message.from_user.id}")
        if response.status_code == 200:
            bot.send_message(message.from_user.id, f"STATUS:{response.content}")
            default(message)        
        else: 
            greetings(message)  
            confirm(message)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "all_users":
        try:
            response = requests.get(f"{BACKEND_URL}/users/get")
            bot.send_message(call.from_user.id, 
                             response)
        except Exception as e:    
            bot.send_message(call.from_user.id, 
                             f'Ой, что-то пошло не так :(\nПовторите попытку позже...\n{e}')
    elif call.data == 'register' :
        response = requests.post(f"{BACKEND_URL}/user/",
                        json={
                        "id": f"{call.from_user.id}",
                        "username": f"{call.from_user.username}",
                        "credits": 1000
                        },)  
        bot.send_message(call.from_user.id, f"RESPONSE:{response.content}")
    elif call.data == 'model_choice1':
        pass
    elif call.data == 'model_choice2':
        pass
    elif call.data == 'model_choice3':
        pass
    elif call.data == 'history':
        response = requests.get(f"{BACKEND_URL}/user/actions/{call.from_user.id}")
        bot.send_message(call.from_user.id, f"History:{response.content}")
    elif call.data == 'add_balance':
        response = requests.post(f"{BACKEND_URL}/user/{call.from_user.id}/",
                        params={
                        "new_credits": 10,
                        },)  
        bot.send_message(call.from_user.id, f"Adding 10 credits:{response.content}")
    
       

@bot.message_handler(content_types=['document'])
def process_documents(message):
    # file_name = message.document.file_name
    # file_info = bot.get_file(message.document.file_id)
    # downloaded_file = bot.download_file(file_info.file_path)
    # bot.send_message(message.from_user.id, f"file info: {downloaded_file}, {file_name}")

    
    # file_name = message.document.file_name
    # file_id = message.document.file_name
    # file_id_info = bot.get_file(message.document.file_id)
    # downloaded_file = bot.download_file(file_id_info.file_path)
    # bot.send_message(message.from_user.id, f"file info: {file_name}")
    # with open(file_name, 'wb') as new_file:
    #     new_file.write(downloaded_file)
        
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Use io.BytesIO to create a file-like object
        file_like_object = io.BytesIO(downloaded_file)
        
        # Assuming the file is a CSV file
        df = pd.read_csv(file_like_object)
        
        # Convert the DataFrame to a JSON string
        json_data = df.to_json(orient='records')
        
        # Display the JSON string or send it as a message
        bot.send_message(message.from_user.id, f"JSON Data:\nOK")
        response = requests.post(f"{BACKEND_URL}/model/test_model/{message.from_user.id}",
                        params={
                        "user_id": f"{message.from_user.id}",
                        "model_id": f"{1}",
                        "input_data": str(json_data)
                        },) 
        bot.send_message(message.from_user.id, f"Result: {str(response.content)}")
        
    except Exception as e:
        # Handle exceptions (e.g., invalid CSV format)
        bot.send_message(message.from_user.id, f"Error processing the document: {str(e)}")


    
   
def default(message):
    bot.send_video(message.from_user.id, 'https://i.pinimg.com/originals/71/22/6e/71226e63be7afa7e92d68e4407fa853d.gif')
    bot.send_message(message.from_user.id, """
Привет, это учебный бот для инференса моделей!

Бот может хранить историю операций, привязанную к определенному аккаунту, прошу подтвердить запись информации об аккаунте

    """,
    reply_markup=menu_buttons(),
    parse_mode= 'Markdown')    
    
def greetings(message):
    # bot.send_photo(message.from_user.id, 'https://cs14.pikabu.ru/post_img/2022/11/03/11/1667504777134725533.jpg')
    # bot.send_video(message.from_user.id, 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNW8yNThheTYxdHF2YXpseDVjd2w4aGZ4amQ1Z3hhbm5iNGk5cGQwbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/VFf2015gPpE80ii9iX/giphy.gif', None, 'Text')
    bot.send_video(message.from_user.id, 'https://i.pinimg.com/originals/71/22/6e/71226e63be7afa7e92d68e4407fa853d.gif')
    bot.send_message(message.from_user.id, """
Привет, это учебный бот для инференса моделей!

Бот может хранить историю операций, привязанную к определенному аккаунту, прошу подтвердить запись информации об аккаунте

    """,
    )


def confirm(message):
    bot.send_message(message.from_user.id, """
    Подтвердите согласие на хранение данных!
    """,
    reply_markup=confirm_buttons(),
    parse_mode= 'Markdown')

def confirm_buttons():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Подтвердить', callback_data='register')
    markup.add(btn)
    return markup


def menu_buttons():
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Использовать модель rf', callback_data='model_choice1')
    markup.add(btn)
    btn = types.InlineKeyboardButton(text='Использовать модель svm', callback_data='model_choice2')
    markup.add(btn)
    btn = types.InlineKeyboardButton(text='Использовать модель xgboost', callback_data='model_choice3')
    markup.add(btn)
    btn = types.InlineKeyboardButton(text='История действий', callback_data='history')
    markup.add(btn)
    btn = types.InlineKeyboardButton(text='Пополнить баланс на 10 кредитов', callback_data='add_balance')
    markup.add(btn)
    return markup

bot.infinity_polling()