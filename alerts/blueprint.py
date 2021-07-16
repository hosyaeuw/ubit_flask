from models import *

from sms.blueprint import send_sms
from telegram.blueprint import send_telegram_message

from flask import Blueprint, request, jsonify
import re

blueprint_alerts = Blueprint('alerts', __name__)

db_fields = get_column_fiends(Alerts)


@blueprint_alerts.route('/', methods=['GET'])
def index():
    return "alerts page"


@blueprint_alerts.route('/get_all', methods=['GET'])
def get_all():
    items = Alerts.query.all()
    data = [{
        'id': item.id,
        'text': item.text,
        'date': item.date.strftime("%d.%m.%Y")
    } for item in items]
    return jsonify(data)


@blueprint_alerts.route('/get_by_user/<id>', methods=['GET'])
def get_by_user(id):
    g = Users.query.filter(Users.id == id).first().dancers[0].group
    items = g.alerts.order_by(Alerts.date.desc()).all()
    data = [{
        'id': item.id,
        'text': item.text,
        'date': item.date.strftime("%d.%m.%Y")
    } for item in items]
    return jsonify(data)


def strip_phone(phone):
    template = r'\d+'
    return ''.join(re.findall(template, phone))


@blueprint_alerts.route('/send_message', methods=['POST'])
def send_message():
    args = request.get_json(force=True)
    message = args.get('message')
    id_groups = args.get('groups')
    dancers_sms_active = Dancers.query.filter(
        (Dancers.sms_active == True) &
        (Dancers.group_id.in_(id_groups) == True)).all()
    dancers_telegram_active = Dancers.query.filter(
        (Dancers.telegram_active == True) &
        (Dancers.group_id.in_(id_groups) == True)).all()
    groups = Groups.query.filter(Groups.id.in_(id_groups)).all()

    dancers_phones = [strip_phone(dancer.users.phone) for dancer in dancers_sms_active]
    dancers_telegram_chat_id = [dancer.telegram_chat_id
                                for dancer in dancers_telegram_active]
    user_id = 1

    send_sms(dancers_phones, message)
    for chat_id in dancers_telegram_chat_id:
        send_telegram_message(chat_id, message)

    a = Alerts(user_id=user_id, text=message)
    a.groups = groups
    db.session.add(a)
    db.session.commit()

    return 'ok'
