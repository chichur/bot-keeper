import telebot
import requests

token = 'token'

bot = telebot.TeleBot(token)

url_api = 'http://127.0.0.1:5000/api/'
url = 'http://127.0.0.1:5000/'

error_emoji = u'\U0000274C'
success_emoji = u'\U00002705'


@bot.message_handler(commands=['start'])
def start_message(message):
    client_id = message.from_user.id
    print(client_id)
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['voice'])
def get_voice_message(message):
    file_info = bot.get_file(message.voice.file_id)
    client_id = message.from_user.id
    print(client_id)
    try:
        req_api = requests.get(url_api + '{0}/{1}'.format(file_info.file_path, client_id))
    except requests.ConnectionError:
        bot.send_message(message.chat.id, error_emoji + ' Ошибка подключения к серверу данных')
    except Exception as e:
        bot.send_message(message.chat.id, 'Неизвестная ошибка: {0}'.format(e))
    else:
        bot.send_message(message.chat.id, success_emoji + ' Ваша аудизапись конвертирована\n'
                                                          'Скачать: ' + url + req_api.text)


@bot.message_handler(content_types=['photo'])
def get_photos_message(message):
    for p in message.photo:
        file_info = bot.get_file(p.file_id)
        client_id = message.from_user.id
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open('static/' + file_info.file_path, 'wb') as f:
            f.write(file.content)


# def api(url_api, ):
#     try:
#         req_api = requests.get(url_api + '{0}/{1}'.format(file_info.file_path, client_id))
#     except requests.ConnectionError:
#         bot.send_message(message.chat.id, error_emoji + ' Ошибка подключения к серверу данных')
#     except Exception as e:
#         bot.send_message(message.chat.id, 'Неизвестная ошибка: {0}'.format(e))
#     else:
#         print(req_api.text)


bot.polling()
