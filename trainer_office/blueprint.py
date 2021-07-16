from models import *

from flask import Blueprint, request, jsonify
from flask_jwt import jwt_required


blueprint_trainer_office = Blueprint('trainer_office', __name__)

# db_fields = get_column_fiends(Trainers)


@blueprint_trainer_office.route('/', methods=['GET'])
def index():
    return "trainer page"


@blueprint_trainer_office.route('/get_all', methods=['GET'])
def get_all():
    items = TrainerOffice.query.all()
    data = [{
        'id': item.id,
        'name': item.name
    } for item in items]
    return jsonify(data)