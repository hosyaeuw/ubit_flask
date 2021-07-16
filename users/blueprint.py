from models import *

from flask import Blueprint, request
from flask_jwt import jwt_required

import re

blueprint_users = Blueprint('users', __name__)

db_fields = get_column_fiends(Users)

def strip_phone(phone):
    template = r'\d+'
    return ''.join(re.findall(template, phone))

def add_user(args, ur_id):
    args['phone'] = strip_phone(args['phone'])
    data = get_attr(db_fields, args)
    ur = UserRoles.query.filter(UserRoles.id == ur_id).first()
    q = Users(**data)
    q.user_roles = [ur]
    db.session.add(q)
    db.session.commit()
    return q

def update_user(table, id, args):
    user_id = table.query.filter(table.id == id).first().users.id
    data = get_attr(db_fields, args)
    update_from_db(Users, user_id, data)
    return user_id


def delete_user(table, id):
    print('*'*50)
    print(id)
    print('*'*50)
    user_id = table.query.filter(table.id == id).first().users.id
    delete_from_db(table, id)
    result = delete_from_db(Users, user_id)
    return result


@blueprint_users.route('/', methods=['GET'])
def index():
    return "user page"


@blueprint_users.route('/add_role', methods=['POST'])
def add_role():
    name = request.get_json(force=True).get("name")
    ur = UserRoles(name=name)
    db.session.add(ur)
    db.session.commit()
    return "user page"
