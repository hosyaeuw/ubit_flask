from models import *

import os

from flask import Blueprint, request
import requests

blueprint_telegram = Blueprint('telegram', __name__)

access_token = os.getenv('telegram_access_token')

URL = f'https://api.telegram.org/bot{access_token}/'


def send_telegram_message(chat_id, message=('Не знаю, что на это ответить. '
                                            'Проверьте запрос')):
    try:
        url = URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text': message}
        r = requests.post(url, json=answer)
        return r.json()
    except Exception as e:
        return 'ok'


@blueprint_telegram.route('/', methods=['POST'])
def index():
    try:
        r = request.get_json()
        user_username = r['message']['from']['username']
        user_chat_id = r['message']['chat']['id']
        user_message = r['message']['text'].strip()
        bot_message = 'Не знаю, что на это ответить. Проверьте запрос'
        if user_message == '/start':
            bot_message = 'Введите токен, который можно найти в профиле:'
        else:
            d = Dancers.query.filter(Dancers.telegram_token == user_message)
            if d.scalar():
                d.update({
                    'telegram_chat_id': user_chat_id,
                    'telegram_username': user_username
                })
                db.session.commit()
                bot_message = 'Вы удачно подключили ' \
                              'телеграм к системе оповещений!'
        send_telegram_message(user_chat_id, bot_message)
    except Exception as e:
        print(e)
    finally:
        return "ok"


@blueprint_telegram.route('/update_active', methods=['PUT'])
def update_active():
    args = request.get_json(force=True)
    id_user = args.get('id')
    active = args.get('active')
    d = Users.query.filter(Users.id == id_user).first().dancers[0]
    d.telegram_active = active
    db.session.commit()
    return 'ok'
