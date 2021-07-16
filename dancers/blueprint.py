from models import *
from users.blueprint import add_user, update_user, delete_user

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

blueprint_dancers = Blueprint('dancers', __name__)

db_fields = get_column_fiends(Dancers)


@blueprint_dancers.route('/', methods=['GET'])
def index():
    return "dancers page"


@blueprint_dancers.route('/get/<id>', methods=['GET'])
def get(id):
    item = Users.query.filter(Users.id == id).first().dancers[0]
    print(dir(item.group))
    data = {
        'id': item.id,
        'fio': item.users.fio,
        'phone': item.users.phone,
        'login': item.users.login,
        'group': {
            'id': item.group.id,
            'age_to': item.group.age_to,
            'from_age': item.group.from_age
        },
        'telegram': {
                        'token': item.telegram_token,
                        'username': item.telegram_username,
                        'active': item.telegram_active
                    }
    }
    return jsonify(data)


@blueprint_dancers.route('/get_all', methods=['GET'])
def get_all():
    items = Dancers.query.all()
    data = [{
        'id': item.id,
        'fio': item.users.fio,
        'phone': item.users.phone,
        'login': item.users.login,
        'birthday': item.birthday.strftime("%d.%m.%Y")
    } for item in items]
    return jsonify(data)


@blueprint_dancers.route('/add', methods=['POST'])
# @jwt_required()
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    ur_id = 2
    u = add_user(args, ur_id)
    data['user_id'] = u.id
    data['telegram_token'] = Dancers.generate_telegram_token(u.phone)
    result = add_to_db(Dancers, data)

    if args.get('have_parent'):
        parent_args = {
            'fio': args.get('fioParent'),
            'phone': args.get('phoneParent'),
            'child_id': result.id
        }
        parent_db_fields = get_column_fiends(Parents)
        parent_data = get_attr(parent_db_fields, parent_args)
        ur_id = 4
        u = add_user(parent_args, ur_id)
        parent_data['user_id'] = u.id
        add_to_db(Parents, parent_data)
    return jsonify({'result': result.id})
    # return 'ok'


@blueprint_dancers.route('/update/<id>', methods=['PUT'])
# @jwt_required()
def update(id):
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    user_id = update_user(Dancers, id, args)
    data['user_id'] = user_id
    result = update_from_db(Dancers, id, data)
    return jsonify(result)


@blueprint_dancers.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    result = delete_user(Dancers, id)
    return jsonify(result)
