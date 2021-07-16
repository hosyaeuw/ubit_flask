from models import *

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

blueprint_payments = Blueprint('payments', __name__)

db_fields = get_column_fiends(Payments)


@blueprint_payments.route('/', methods=['GET'])
def index():
    return "payments page"


@blueprint_payments.route('/get_all', methods=['GET'])
def get_all():
    items = Payments.query.order_by(Payments.date.desc()).all()
    data = [{
        'id': item.id,
        'date': item.date.strftime("%d.%m.%Y"),
        'dancer': {
            'id': item.dancer.id,
            'fio': item.dancer.users.fio
        }
    } for item in items]
    return jsonify(data)


@blueprint_payments.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    print(data)
    result = add_to_db(Payments, data)
    return jsonify({'result': result.id})


# @blueprint_payments.route('/update', methods=['PUT'])
# def update():
#     args = request.get_json(force=True)
#     data = get_attr(db_fields, args)
#     result = update_from_db(NewsTypes, data)
#     return jsonify(result)
#
#
# @blueprint_payments.route('/delete', methods=['DELETE'])
# def delete():
#     id = request.get_json(force=True).get('id')
#     result = delete_from_db(NewsTypes, id)
#     return jsonify(result)
