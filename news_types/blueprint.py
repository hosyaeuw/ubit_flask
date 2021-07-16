from models import *

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

blueprint_news_types = Blueprint('news_types', __name__)

db_fields = get_column_fiends(NewsTypes)


@blueprint_news_types.route('/', methods=['GET'])
def index():
    return "news_types page"


@blueprint_news_types.route('/get_all', methods=['GET'])
def get_all():
    items = NewsTypes.query.all()
    data = [{
        'id': item.id,
        'name': item.name
    } for item in items]
    return jsonify(data)


@blueprint_news_types.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    result = add_to_db(NewsTypes, data)
    return jsonify({'result': result.id})


@blueprint_news_types.route('/update', methods=['PUT'])
def update():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    result = update_from_db(NewsTypes, data)
    return jsonify(result)


@blueprint_news_types.route('/delete', methods=['DELETE'])
def delete():
    id = request.get_json(force=True).get('id')
    result = delete_from_db(NewsTypes, id)
    return jsonify(result)
