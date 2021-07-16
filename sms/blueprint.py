from models import *

import os

from flask import Blueprint, request, jsonify
import requests

blueprint_sms = Blueprint('sms', __name__)

api_id = os.getenv('sms_api_key')


def send_sms(phones, message=''):
    phones = ','.join(phones)
    params = {
        'json': 1,
        'api_id': api_id,
        'to': phones,
        'msg': message,
        'from': 'ubit',
    }
    url = f'https://sms.ru/sms/send'
    r = requests.get(url, params=params)
    return r.json()


@blueprint_sms.route('/', methods=['GET'])
def index():
    return "sms page"


@blueprint_sms.route('/send_message', methods=['POST'])
def send_message():
    args = request.get_json(force=True)
    message = args.get('message')
    phones = args.get('phones')
    r = send_sms(phones, message)
    return jsonify(r)
