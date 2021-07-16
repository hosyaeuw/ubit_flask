from models import *
from users.blueprint import add_user, update_user, delete_user

import os
from app import app

from json import loads

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required
from utils import image_preparation, translit_filename


blueprint_news = Blueprint('news', __name__)

db_fields = get_column_fiends(News)


@blueprint_news.route('/', methods=['GET'])
def index():
    return "new page"


@blueprint_news.route('/get/<id>', methods=['GET'])
def get(id):
    item = News.query.filter(News.id == id).first()
    data = {
        'id': item.id,
        'title': item.title,
        'text': item.text,
        'date': item.date.strftime("%d.%m.%Y"),
        'preview': item.preview,
        'news_type': item.news_types.id
    }
    return jsonify(data)


@blueprint_news.route('/get_all', methods=['GET'])
def get_all():
    items = News.query.all()
    data = [{
        'id': item.id,
        'title': item.title,
        'text': item.text,
        'date': item.date.strftime("%d.%m.%Y"),
        'preview': os.path.join(app.config['UPLOAD_FOLDER'], item.preview),
        'news_type': item.news_types.name
    } for item in items]
    return jsonify(data)


@blueprint_news.route('/get_news_all', methods=['GET'])
def get_news_all():
    items = News.query.filter(News.news_type_id == 1).all()
    data = [{
        'id': item.id,
        'title': item.title,
        'text': item.text,
        'date': item.date.strftime("%d.%m.%Y"),
        'preview': os.path.join(app.config['UPLOAD_FOLDER'], item.preview),
        'news_type': item.news_types.name
    } for item in items]
    return jsonify(data)


@blueprint_news.route('/get_events_all', methods=['GET'])
def get_events_all():
    items = News.query.filter(News.news_type_id == 2).all()
    data = [{
        'id': item.id,
        'title': item.title,
        'text': item.text,
        'date': item.date.strftime("%d.%m.%Y"),
        'preview': os.path.join(app.config['UPLOAD_FOLDER'], item.preview),
        'news_type': item.news_types.name
    } for item in items]
    return jsonify(data)


@blueprint_news.route('/add', methods=['POST'])
def add():
    form_args = request.form
    photo = request.files.get('preview')
    args = {key: form_args[key] for key in form_args}
    if photo:
        img = image_preparation(photo)
        args['preview'] = img
    else:
        args['preview'] = None
    data = get_attr(db_fields, args)
    result = add_to_db(News, data)
    return jsonify({'result': result.id})


@blueprint_news.route('/update/<id>', methods=['GET', 'PUT'])
def update(id):
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    user_id = update_user(News, id, args)
    data['user_id'] = user_id
    result = update_from_db(News, id, data)
    return jsonify(result)


@blueprint_news.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    delete_from_db(News, id)
    return jsonify({'result': id})
