import os
import json
import datetime
import requests
from flask import Flask, request, render_template
from bot import token
import flask
# from models import User, History
# from user_agents import parse
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# подключаемся к бд
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content.db'
# db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def rer():
    return flask.send_file('voice.ogg', as_attachment=True, attachment_filename='rer.ogg')


@app.route('/api/voice/<file_path>/<uid>', methods=['GET'])
def api(file_path, uid):
    print(file_path)
    file = requests.get('https://api.telegram.org/file/bot{0}/voice/{1}'.format(token, file_path))
    print('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_path))
    with open(file_path, 'wb') as f:
        f.write(file.content)


def get_or_create(session, model, **kwargs):
    """
    функция получить или создать, нужна для того чтобы не создавать
    дублирующие записи в таблице пользователей
    :param session: сессия
    :param model: класс модели
    :param kwargs: данные
    :return:
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance


if __name__ == '__main__':
    app.run()

