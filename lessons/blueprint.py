from models import *

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

blueprint_lessons = Blueprint('lessons', __name__)

db_fields = get_column_fiends(Lessons)


@blueprint_lessons.route('/', methods=['GET'])
def index():
    return "group page"


# @blueprint_lessons.route('/get/<id>', methods=['GET'])
# def get(id):
#     item = Groups.query.filter(Groups.id == id).first()
#     data = {
#         'id': item.id,
#         'from_age': item.from_age,
#         'age_to': item.age_to,
#         'price': item.price,
#     }
#     return jsonify(data)


@blueprint_lessons.route('/get_all', methods=['GET'])
def get_all():
    items = Lessons.query.all()
    data = [{
        'id': item.id,
        'date': item.date.strftime("%d.%m.%Y"),
        'trainer': item.trainer.users.fio
    } for item in items]
    return jsonify(data)


@blueprint_lessons.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    print(data)
    # date, trainer
    # result = add_to_db(Groups, data)
    # return jsonify({'result': result.id})
    return 'ok'

# @blueprint_lessons.route('/update/<id>', methods=['PUT'])
# def update(id):
#     args = request.get_json(force=True)
#     data = get_attr(db_fields, args)
#     result = update_from_db(Groups, id, data)
#     return jsonify(result)
#
#
# @blueprint_lessons.route('/delete/<id>', methods=['DELETE'])
# def delete(id):
#     result = delete_from_db(Groups, id)
#     return jsonify(result)
