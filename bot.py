import telebot
import requests

token = '1216892494:AAENx9So0e0_Drf78BCnMRRpJLxfeYgFCug'

bot = telebot.TeleBot(token)

url_api = 'http://127.0.0.1:5000/api/'
url = 'http://127.0.0.1:5000/'

error_emoji = u'\U0000274C'
success_emoji = u'\U00002705'


@bot.message_handler(commands=['start'])
def start_message(message):
    client_id = message.from_user.id
    print(client_id)
    bot.send_message(message.chat.id, 'Привет, я сохраню твои аудиозаписи в формате .wav'
                                      ' c частотой дискретизации 16kHz, а также фотографии'
                                      ' если на них будут лица ')


@bot.message_handler(content_types=['voice'])
def get_voice_message(message):
    file_info = bot.get_file(message.voice.file_id)
    client_id = message.from_user.id
    print(client_id)
    handler_exception(message, file_info, client_id)


@bot.message_handler(content_types=['photo'])
def get_photos_message(message):
    file_info = bot.get_file(message.photo[0].file_id)
    client_id = message.from_user.id
    handler_exception(message, file_info, client_id)


def handler_exception(message, file_info, client_id):
    try:
        req_api = requests.get(url_api + '{0}/{1}'.format(file_info.file_path, client_id))
    except requests.ConnectionError:
        bot.send_message(message.chat.id, error_emoji + ' Ошибка подключения к серверу данных')
    except Exception as e:
        bot.send_message(message.chat.id, 'Неизвестная ошибка: {0}'.format(e))
    else:
        if message.voice:
            bot.send_message(message.chat.id, success_emoji + ' Ваша аудиозапись конвертирована\n'
                                                              'Скачать: ' + url + req_api.text)
        elif message.photo:
            if req_api.text == 'error':
                bot.send_message(message.chat.id, error_emoji + ' Ошибка: на фотографии нет лица')
            else:
                bot.send_message(message.chat.id, success_emoji + ' Ваша фотография загружена\n'
                                                                  'Скачать: ' + url + req_api.text)


if __name__ == '__main__':
    bot.polling()
