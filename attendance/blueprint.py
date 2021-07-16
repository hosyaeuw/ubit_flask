from models import *

from flask import Blueprint, request, jsonify
from datetime import datetime
import calendar
from sqlalchemy import func

blueprint_attendance = Blueprint('attendance', __name__)

db_fields = get_column_fiends(Attendance)


def get_present_count():
    q = db.engine.execute("""SELECT count_lessons.id_child, count_lessons, count_present_lessons.count_present_lessons, count_no_present_lessons.count_no_present_lessons from 
    (SELECT a.id_child, count(a.id_lesson) AS count_lessons from dancers d, attendance a, lessons l, 
    (SELECT p.id_dancer, MAX(p.date) AS max_date FROM payments p group by p.id_dancer) md 
    WHERE d.id = md.id_dancer AND a.id_child = d.id AND l.id = a.id_lesson AND l."date" >= md.max_date AND l."date" <= '30.05.2021'
    group by a.id_child having count(a.id_lesson) > 7) AS count_lessons LEFT JOIN (SELECT a.id_child, count(a.id_lesson) AS count_present_lessons from dancers d, attendance a, lessons l, 
    (SELECT p.id_dancer, MAX(p.date) AS max_date FROM payments p group by p.id_dancer) md 
    WHERE d.id = md.id_dancer AND a.id_child = d.id AND l.id = a.id_lesson AND l."date" >= md.max_date AND l."date" <= '30.05.2021' AND a.present = true
    group by a.id_child) as count_present_lessons ON count_lessons.id_child = count_present_lessons.id_child LEFT JOIN (
    SELECT a.id_child, count(a.id_lesson) AS count_no_present_lessons from dancers d, attendance a, lessons l, 
    (SELECT p.id_dancer, MAX(p.date) AS max_date FROM payments p group by p.id_dancer) md 
    WHERE d.id = md.id_dancer AND a.id_child = d.id AND l.id = a.id_lesson AND l."date" >= md.max_date AND l."date" <= '30.05.2021' AND a.present = false
    group by a.id_child) AS count_no_present_lessons ON count_no_present_lessons.id_child = count_present_lessons.id_child
    """)
    data = {}
    for row in q:
        data[row[0]] = {
            'count': row[1],
            'present': row[2],
            'no_present': row[3]
        }
    return data


def get_present_count_by_group(id_group):
    q = db.engine.execute(f"""SELECT count_lessons.id_child, count_lessons, count_present_lessons.count_present_lessons, count_no_present_lessons.count_no_present_lessons from 
    (SELECT a.id_child, count(a.id_lesson) AS count_lessons from dancers d, attendance a, lessons l, 
    (SELECT p.id_dancer, MAX(p.date) AS max_date FROM payments p group by p.id_dancer) md 
    WHERE d.id = md.id_dancer AND a.id_child = d.id AND l.id = a.id_lesson AND l."date" >= md.max_date and d.group_id = {id_group} AND l."date" <= '30.05.2021'
    group by a.id_child having count(a.id_lesson) > 7) AS count_lessons LEFT JOIN (SELECT a.id_child, count(a.id_lesson) AS count_present_lessons from dancers d, attendance a, lessons l, 
    (SELECT p.id_dancer, MAX(p.date) AS max_date FROM payments p group by p.id_dancer) md 
    WHERE d.id = md.id_dancer AND a.id_child = d.id AND l.id = a.id_lesson AND l."date" >= md.max_date and d.group_id = {id_group}  AND l."date" <= '30.05.2021' AND a.present = true
    group by a.id_child) as count_present_lessons ON count_lessons.id_child = count_present_lessons.id_child LEFT JOIN (
    SELECT a.id_child, count(a.id_lesson) AS count_no_present_lessons from dancers d, attendance a, lessons l, 
    (SELECT p.id_dancer, MAX(p.date) AS max_date FROM payments p group by p.id_dancer) md 
    WHERE d.id = md.id_dancer AND a.id_child = d.id AND l.id = a.id_lesson AND l."date" >= md.max_date and d.group_id = {id_group} AND l."date" <= '30.05.2021' AND a.present = false
    group by a.id_child) AS count_no_present_lessons ON count_no_present_lessons.id_child = count_present_lessons.id_child
    """)
    data = {}
    for row in q:
        print(row)
        data[row[0]] = {
            'count': row[1],
            'present': row[2],
            'no_present': row[3]
        }
    print(data)
    return data


# TODO: удалить
def get_test(group_present, dancer):
    try:
        data = {
            'count_lessons': group_present[dancer.id]['count'],
            'count_present': group_present[dancer.id]['present'],
            'count_no_present': group_present[dancer.id]['no_present']
        }
    except Exception as e:
        data = None
    return data


def get_attendance_group(first_day, last_day, id_group):
    group_present = get_present_count_by_group(id_group)

    lessons = Lessons.query \
        .join(Attendance) \
        .join(Dancers) \
        .filter(
                Lessons.date >= first_day,
                Lessons.date <= last_day,
                Dancers.group_id == id_group
        ).group_by(Lessons).order_by(Lessons.date.desc()).all()

    dancers = Dancers.query \
        .join(Attendance) \
        .join(Lessons) \
        .join(Users) \
        .filter(
                Lessons.date >= first_day,
                Lessons.date <= last_day,
                Dancers.group_id == id_group
            ).group_by(Dancers, Users.fio).order_by(Users.fio).all()
    data = {
        'first_day': first_day,
        'last_day': last_day,
        'dancers': [{
            'id': dancer.id,
            'fio': dancer.users.fio,
            'membership': get_test(group_present, dancer)
        } for dancer in dancers],
        'lessons': [{
            'id': lesson.id,
            'date': lesson.date.strftime('%d.%m.%Y'),
            'attendance': [
                {
                    'dancer': {
                        'id': attendance.id_child,
                        'fio': attendance.dancer.users.fio
                    },
                    'present': attendance.present
                } for attendance in lesson.attendance]
        } for lesson in lessons]
    }
    return data


@blueprint_attendance.route('/', methods=['GET'])
def index():
    return "attendance page"


@blueprint_attendance.route('/cheange_dancer_present', methods=['PUT'])
def cheange_dancer_present():
    args = request.get_json(force=True)
    a = Attendance.query.filter(
        (Attendance.id_child == args.get('child_id')) &
        (Attendance.id_lesson == args.get('lesson_id')))
    a.update({'present': args.get('present')})
    db.session.commit()
    return "attendance page"


@blueprint_attendance.route('/get_by_lesson/<id>', methods=['GET'])
def get_attendance_by_lesson(id):
    items = Attendance.query.filter(Attendance.id_lesson == id).all()
    data = {
        'date': items[0].lessons.date.strftime('%d.%m.%Y'),
        'items': [{
            'dancer': {
                'id': item.dancer.id,
                'name': item.dancer.users.fio
            },
            'present': item.present
        } for item in items]
    }
    return jsonify(data)


@blueprint_attendance.route('/get_attendance_range/<id_group>', methods=['GET'])
def get_attendance_range(id_group):
    first_day = request.args.get('ot')
    last_day = request.args.get('do')
    data = get_attendance_group(first_day, last_day, id_group)
    return jsonify(data)


@blueprint_attendance.route('/get_two_month_attendance/<id_group>',
                            methods=['GET'])
def get_two_month_attendance(id_group):
    today = datetime.today()
    first_day = datetime.today().replace(month=today.month - 2)\
        .strftime('%d.%m.%Y')
    # last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    # last_day = datetime.today().replace(day=last_day_of_month)
    last_day = today.strftime('%d.%m.%Y')
    data = get_attendance_group(first_day, last_day, id_group)
    return jsonify(data)
    # print(Lessons.query.join(Attendance).join(Dancers).filter(Lessons.date >= first_day, Lessons.date <= last_day, Dancers.group_id == id_group))
    # for item in items:
    #     print(item.date)
    #
    # dancers = list(set([a for b in [
    #     [i.dancer for i in item.attendance] for item in items] for a in b]))
    # print(dancers[0].attendance)
    # data = {
    #     'lessons': [{
    #             'id': item.id,
    #             'date': item.date.strftime('%d.%m.%Y')
    #          } for item in items],
    #     'dancers': [{
    #         'info': {
    #             'id': dancer.id,
    #             'fio': dancer.users.fio
    #         },
    #         'attendances': []
    #     } for dancer in dancers]
    # }
    # print(data)
    # return jsonify(data)
    # print(data)
    # print(data)

    # dancers = [[i.dancer for i in item.attendance] for item in items]
    # print(dancers)
    # print(dir(items[0].attendance))
    # dancers = [[i.id_child for i in item.attendance] for item in items]
    # print(dancers)
    # dancers_one = [a for b in [[i.dancer for i in item.attendance] for item in items] for a in b]
    # print(len(dancers_one))
    # print(len(set(dancers_one)))
    # date = items[0].lessons.date.strftime('%d.%m.%Y')
    # for item in items:
    #     lesson_date = item.lessons.date.strftime('%d.%m.%Y')
    #     if lesson_date == date:
    #         print(item)
    #     else:
    #         break
    # print(items)
    # return 'ok'
    # data = {
    #     'date': items[0].lessons.date.strftime('%d.%m.%Y'),
    #     'items': [{
    #         'dancer': {
    #             'id': item.dancer.id,
    #             'name': item.dancer.users.fio
    #         },
    #         'present': item.present
    #     } for item in items]
    # }
    # return jsonify(data)


@blueprint_attendance.route('/get_by_dancer/<id>', methods=['GET'])
def get_attendance_by_dancer(id):
    items = Attendance.query.filter(Attendance.id_child == id).all()
    dancer = {
            'id': items[0].dancer.id,
            'name': items[0].dancer.users.fio
        }
    data = [{
        'dancer': dancer,
        'date': item.lessons.date,
        'present': item.present
    } for item in items]
    return jsonify(data)


@blueprint_attendance.route('/get_all', methods=['GET'])
def get_all():
    items = Dancers.query.all()
    data = [{
        'id': item.id,
        'fio': item.users.fio,
        'phone': item.users.phone,
        'login': item.users.login,
        'birthday': item.birthday.strftime("%d.%m.%Y")
    } for item in items]
    return jsonify(data)


# @blueprint_attendance.route('/add', methods=['POST'])
# def add():
#     args = request.get_json(force=True)
#     data = get_attr(db_fields, args)
#     print(args)
#     # ur_id = 2
#     # u = add_user(args, ur_id)
#     # data['user_id'] = u.id
#     # result = add_to_db(Dancers, data)
#     # return jsonify({'result': result.id})
#     return 'ok'
#
#
# @blueprint_attendance.route('/update/<id>', methods=['GET', 'PUT'])
# def update(id):
#     args = request.get_json(force=True)
#     data = get_attr(db_fields, args)
#     user_id = update_user(Dancers, id, args)
#     data['user_id'] = user_id
#     result = update_from_db(Dancers, id, data)
#     return jsonify(result)
#
#
# @blueprint_attendance.route('/delete/<id>', methods=['DELETE'])
# def delete(id):
#     result = delete_user(Dancers, id)
#     return jsonify(result)
