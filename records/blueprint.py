from models import *

from flask import Blueprint, request, jsonify

blueprint_records = Blueprint('records', __name__)

db_fields = get_column_fiends(Records)


@blueprint_records.route('/', methods=['GET'])
def index():
    return "records page"


@blueprint_records.route('/get_all', methods=['GET'])
def get_all():
    items = Records.query.order_by(Records.date.desc()).all()
    data = [{
        'id': item.id,
        'fio': item.fio,
        'phone': item.phone,
        'date': item.date.strftime("%d.%m.%Y")
    } for item in items]
    return jsonify(data)


@blueprint_records.route('/add', methods=['POST'])
def add():
    args = request.get_json(force=True)
    data = get_attr(db_fields, args)
    result = add_to_db(Records, data)
    return jsonify({'result': result.id})
