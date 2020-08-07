"""
Скрипт обработки сообщений посылаемых боту
"""
import telebot
import requests

token = 'token'

bot = telebot.TeleBot(token)

# адрес api-сервера
url_api = 'http://127.0.0.1:5000/api/'
url = 'http://127.0.0.1:5000/'

error_emoji = u'\U0000274C'
success_emoji = u'\U00002705'
face_emoji = u'\U0001F31D'


@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Обработчик команды старт
    """
    name = message.from_user.first_name
    bot.send_message(message.chat.id, 'Привет ' + name + ', я сохраню твои'
                                      ' аудиосообщения в формате .wav'
                                      ' c частотой дискретизации 16kHz, а также фотографии'
                                      ' если на них будут лица ' + face_emoji + '\n/github')


@bot.message_handler(commands=['github'])
def github(message):
    """
    Обработчик команды github, отправляет ссылку на репозиторий проекта
    """
    bot.send_message(message.chat.id, 'https://github.com/chichur/bot-keeper')


@bot.message_handler(content_types=['voice'])
def get_voice_message(message):
    """
    Обработчик голосовых сообщений
    """
    file_info = bot.get_file(message.voice.file_id)
    client_id = message.from_user.id
    handler_exception(message, file_info, client_id)


@bot.message_handler(content_types=['photo'])
def get_photos_message(message):
    """
    Обработчик фотографий
    """
    file_info = bot.get_file(message.photo[0].file_id)
    client_id = message.from_user.id
    handler_exception(message, file_info, client_id)


def handler_exception(message, file_info, client_id):
    """
    Обработчик исключений возникающих при обращении
    к апи-серверу
    :param message: сообщение
    :param file_info: файл принятый ботом
    :param client_id: уникальный номер пользователя
    :return:
    """
    try:
        # обращение к апи серверу с помощью метода GET
        req_api = requests.get(url_api + '{0}/{1}'.format(file_info.file_path, client_id))
    except requests.ConnectionError:
        # обрабатываем исключения ConnectionError, как наиболее частое
        bot.send_message(message.chat.id, error_emoji + ' Ошибка подключения к серверу данных')
    except Exception as e:
        bot.send_message(message.chat.id, 'Неизвестная ошибка: {0}'.format(e))
    else:
        if message.voice:
            bot.send_message(message.chat.id, success_emoji + ' Ваше аудиосообщение конвертировано\n'
                                                              'Скачать: ' + url + req_api.text)
        elif message.photo:
            if req_api.text == 'error':
                bot.send_message(message.chat.id, error_emoji + ' Ошибка: на фотографии нет лица')
            else:
                bot.send_message(message.chat.id, success_emoji + ' Ваша фотография загружена\n'
                                                                  'Скачать: ' + url + req_api.text)


if __name__ == '__main__':
    bot.polling()
