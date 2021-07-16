from models import *

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

blueprint_timetable = Blueprint('timetable', __name__)

db_fields = get_column_fiends(Timetable)


@blueprint_timetable.route('/', methods=['GET'])
def index():
    return "timetable page"


@blueprint_timetable.route('/get_all', methods=['GET'])
def get_all():
    items = Timetable.query.order_by(Timetable.group_id).all()
    data = [{
            'id': item.id,
            'from_age': item.group.from_age,
            'age_to': item.group.age_to,
            'day_of_the_week': {
                    'id': item.day_of_the_week.id,
                    'name': item.day_of_the_week.name,
                    'abbreviation': item.day_of_the_week.abbreviation
                },
            'time_lesson': {
                'id': item.lesson_time.id,
                'start': item.lesson_time.start.strftime("%H:%M"),
                'finish': item.lesson_time.finish.strftime("%H:%M")
            }
            } for item in items]
    return jsonify(data)


@blueprint_timetable.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    print(data)
    result = add_to_db(Timetable, data)
    return jsonify({'result': result.id})

# @blueprint_timetable.route('/update/<id>', methods=['GET', 'PUT'])
# def update(id):
#     args = request.get_json(force=True)
#     data = get_attr(db_fields, args)
#     user_id = update_user(News, id, args)
#     data['user_id'] = user_id
#     result = update_from_db(News, id, data)
#     return jsonify(result)


@blueprint_timetable.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    delete_from_db(Timetable, id)
    return jsonify({'result': id})