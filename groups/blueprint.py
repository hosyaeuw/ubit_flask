from models import *

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

blueprint_groups = Blueprint('groups', __name__)

db_fields = get_column_fiends(Groups)


@blueprint_groups.route('/', methods=['GET'])
def index():
    return "group page"


@blueprint_groups.route('/get/<id>', methods=['GET'])
def get(id):
    item = Groups.query.filter(Groups.id == id).first()
    data = {
        'id': item.id,
        'from_age': item.from_age,
        'age_to': item.age_to,
        'price': item.price,
    }
    return jsonify(data)


@blueprint_groups.route('/get_all', methods=['GET'])
def get_all():
    items = Groups.query.all()
    data = [{
        'id': item.id,
        'from_age': item.from_age,
        'age_to': item.age_to,
        'price': item.price,
        'timetables': [{
            'id': timetable.id,
            'lesson_time': {
                'id': timetable.lesson_time.id,
                'time_start': timetable.lesson_time.start.strftime("%H:%M"),
                'time_finish': timetable.lesson_time.finish.strftime("%H:%M"),
            },
            'day': {
                'id': timetable.day_of_the_week.id,
                'name': timetable.day_of_the_week.name,
                'abbreviation': timetable.day_of_the_week.abbreviation,
            }
        }
            for timetable in item.timetable
        ]
    } for item in items]
    return jsonify(data)


@blueprint_groups.route('/get_by_trainer/<id>', methods=['GET'])
def get_by_trainer(id):
    items = Trainers.query.filter(Trainers.user_id == id).first().groups
    data = [{
        'id': item.id,
        'from_age': item.from_age,
        'age_to': item.age_to,
        'price': item.price,
        'timetables': [{
            'id': timetable.id,
            'lesson_time': {
                'id': timetable.lesson_time.id,
                'time_start': timetable.lesson_time.start.strftime("%H:%M"),
                'time_finish': timetable.lesson_time.finish.strftime("%H:%M"),
            },
            'day': {
                'id': timetable.day_of_the_week.id,
                'name': timetable.day_of_the_week.name,
                'abbreviation': timetable.day_of_the_week.abbreviation,
            }
        }
            for timetable in item.timetable
        ]
    } for item in items]
    return jsonify(data)


@blueprint_groups.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    result = add_to_db(Groups, data)
    return jsonify({'result': result.id})


@blueprint_groups.route('/update/<id>', methods=['PUT'])
def update(id):
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    result = update_from_db(Groups, id, data)
    return jsonify(result)


@blueprint_groups.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    result = delete_from_db(Groups, id)
    return jsonify(result)
