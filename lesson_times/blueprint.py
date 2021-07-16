from models import *

from random import randint

from flask import Blueprint, request, jsonify
import requests

blueprint_lesson_times = Blueprint('lesson_times', __name__)

db_fields = get_column_fiends(LessonTimes)


@blueprint_lesson_times.route('/', methods=['GET'])
def index():
    return "lesson_times page"


@blueprint_lesson_times.route('/get/<id>', methods=['GET'])
def get(id):
    item = LessonTimes.query.filter(LessonTimes.id == id).first()
    data = {
        'id': item.id,
        'start': item.start.strftime("%H:%M"),
        'finish': item.finish.strftime("%H:%M")
    }
    return jsonify(data)


@blueprint_lesson_times.route('/get_all', methods=['GET'])
def get_all():
    items = LessonTimes.query.all()
    data = [{
        'id': item.id,
        'start': item.start.strftime("%H:%M"),
        'finish': item.finish.strftime("%H:%M")
    } for item in items]
    return jsonify(data)


@blueprint_lesson_times.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    data['number'] = randint(1, 9999)
    result = add_to_db(LessonTimes, data)
    return jsonify({'result': result.id})


@blueprint_lesson_times.route('/update/<id>', methods=['GET', 'PUT'])
def update(id):
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    data['number'] = randint(1, 9999)
    result = update_from_db(LessonTimes, id, data)
    return jsonify(result)


@blueprint_lesson_times.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    delete_from_db(LessonTimes, id)
    return jsonify({'result': id})


@blueprint_lesson_times.route('/get_days', methods=['GET'])
def days():
    items = DaysOfTheWeek.query.all()
    data = [{
        'id': item.id,
        'name': item.name
    } for item in items]
    return jsonify(data)
    # return 'ok'
