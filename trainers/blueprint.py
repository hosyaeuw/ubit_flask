from models import *
from users.blueprint import add_user, update_user, delete_user
from utils import image_preparation, translit_filename, get_img_link

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required

import os
from app import app


blueprint_trainers = Blueprint('trainers', __name__)

db_fields = get_column_fiends(Trainers)


@blueprint_trainers.route('/', methods=['GET'])
def index():
    return "trainer page"


@blueprint_trainers.route('/get/<id>', methods=['GET'])
def get(id):
    item = Users.query.filter(Users.id == id).first().trainers[0]
    data = {
        'id': item.id,
        'fio': item.users.fio,
        'phone': item.users.phone,
        'login': item.users.login,
        'photos': [{
                    'id': photo.id,
                    'link': os.path.join(app.config['UPLOAD_FOLDER'], photo.link),
                    } for photo in item.photos],
        'description': item.description
    }
    return jsonify(data)


@blueprint_trainers.route('/get_info/<id>', methods=['GET'])
def get_info(id):
    item = Trainers.query.filter(Trainers.id == id).first()
    data = {
        'id': item.id,
        'fio': item.users.fio,
        'photos': [{
                    'id': photo.id,
                    'link': get_img_link(photo.link)[1:],
                    } for photo in item.photos],
        'description': item.description
    }
    return jsonify(data)


@blueprint_trainers.route('/get_cards', methods=['GET'])
def get_cards():
    items = Trainers.query.all()
    print(get_img_link('196379455_381616379912979_2426770268117492683_n.webp'))
    data = [{
        'id': item.id,
        'fio': item.users.fio,
        'office': item.office.name,
        'photo': get_img_link(item.photos[0].link) if len(item.photos)
        else get_img_link('default_photo.webp')
    } for item in items]
    return jsonify(data)


@blueprint_trainers.route('/get_all', methods=['GET'])
def get_all():
    items = Trainers.query.all()
    data = [{
        'id': item.id,
        'fio': item.users.fio,
        'phone': item.users.phone,
        'login': item.users.login,
        'photo': item.photos[0].link if len(item.photos)
        else 'default_photo.webp'
    } for item in items]
    return jsonify(data)


@blueprint_trainers.route('/add', methods=['POST'])
def add():
    # try:
    form_args = request.form
    args = {key: form_args[key] for key in form_args}
    #
    data = get_attr(db_fields, args)
    ur_id = 3
    u = add_user(args, ur_id)
    data['user_id'] = u.id
    q = Trainers(**data)
    groups = Groups.query.filter(
        Groups.id.in_(args['groups'].split(','))).all()
    q.groups = groups
    db.session.add(q)
    db.session.commit()

    photos = request.files
    if len(photos):
        photo_array = []
        for photo_key in photos:
            img = image_preparation(photos[photo_key])
            photo_array.append(TrainerPhotos(link=img, trainer_id=q.id))
        db.session.add_all(photo_array)
        db.session.commit()
    return jsonify({'result': q.id})
    # return 'ok'


@blueprint_trainers.route('/update/<id>', methods=['GET', 'PUT'])
def update(id):
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    user_id = update_user(Trainers, id, args)
    data['user_id'] = user_id
    result = update_from_db(Trainers, id, data)
    return jsonify(result)


@blueprint_trainers.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    result = delete_user(Trainers, id)
    return jsonify(result)
