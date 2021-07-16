from app import db

from datetime import datetime
from hashlib import sha256

from werkzeug.security import generate_password_hash, check_password_hash
from transliterate import translit


def get_attr(db_fields, args):
    return {db_field: args.get(db_field) for db_field in db_fields}


def get_column_fiends(obj):
    return obj.metadata.tables[obj.__tablename__].columns.keys()


def add_to_db(table, data):
    try:
        q = table(**data)
        db.session.add(q)
        db.session.commit()
        return q
    except Exception as e:
        print(e)
        return e


def update_from_db(table, id, data):
    try:
        q = table.query.filter(table.id == id)
        q.update(data)
        db.session.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return e


def delete_from_db(table, id):
    try:
        q = table.query.filter(table.id == id).first()
        print('*' * 50)
        print(q)
        print('*' * 50)
        db.session.delete(q)
        db.session.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return e


# юзер
roles_users = db.Table('roles_users',
                       db.Column('id_user', db.Integer,
                                 db.ForeignKey('users.id',
                                               ondelete='CASCADE'),
                                 primary_key=True, index=True, nullable=False),
                       db.Column('id_role', db.Integer,
                                 db.ForeignKey('user_roles.id',
                                               ondelete='CASCADE'),
                                 primary_key=True, index=True, nullable=False),
                       )


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(UserRoles, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    fio = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    login = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))

    user_roles = db.relationship('UserRoles', secondary=roles_users,
                                 backref=db.backref('users', lazy='dynamic'))

    trainers = db.relationship('Trainers', backref='users', lazy=True)
    dancers = db.relationship('Dancers', backref='users', lazy=True)
    parents = db.relationship('Parents', backref='users', lazy=True)
    news = db.relationship('News', backref='users', lazy=True)
    alerts = db.relationship('Alerts', backref='users', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self.generate_login()
        self.set_password(self.phone)

    def generate_login(self):
        if self.fio:
            translate_fio = translit(self.fio.lower(), 'ru', reversed=True)
            fio_split = translate_fio.split()
            if len(fio_split) > 1:
                self.login = fio_split[1][:2] + fio_split[0]
            else:
                self.login = fio_split[1]

    def set_password(self, password):
        self.password = generate_password_hash(password.strip())

    def check_password(self,  password):
        return check_password_hash(self.password, password.strip())

    def __repr__(self):
        return self.fio
# # /юзер


# # новости
class NewsTypes(db.Model):
    __tablename__ = 'news_types'

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)

    news = db.relationship('News', backref='news_types', lazy=True)

    def __init__(self, *args, **kwargs):
        super(NewsTypes, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())
    preview = db.Column(db.String(255), default='default_news.webp')

    news_type_id = db.Column(db.Integer, db.ForeignKey('news_types.id'),
                             nullable=False)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                    ondelete='CASCADE'),
                          nullable=False)

    def __init__(self, *args, **kwargs):
        super(News, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.title} {self.date}"

# /новости


# # танцы
trainers_groups = db.Table('trainers_groups',
                           db.Column('id_group', db.Integer,
                                     db.ForeignKey('groups.id'),
                                     primary_key=True, index=True,
                                     nullable=False),
                           db.Column('id_trainer', db.Integer,
                                     db.ForeignKey('trainers.id',
                                                   ondelete='CASCADE'),
                                     primary_key=True, index=True,
                                     nullable=False,),
)


class Trainers(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    description = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='CASCADE'),
                        nullable=False)

    office_id = db.Column(db.Integer, db.ForeignKey('trainer_office.id',
                                                    ondelete='CASCADE'),
                          nullable=True)

    groups = db.relationship('Groups', secondary=trainers_groups,
                             backref=db.backref('trainers', lazy='dynamic'))

    lessons = db.relationship('Lessons', backref='trainer', lazy=True)
    photos = db.relationship('TrainerPhotos', backref='trainer', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Trainers, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.users.fio


class TrainerOffice(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    name = db.Column(db.String(255), nullable=False)

    trainers = db.relationship('Trainers', backref='office', lazy=True)

    def __init__(self, *args, **kwargs):
        super(TrainerOffice, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


class TrainerPhotos(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    link = db.Column(db.String(255), nullable=False)

    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id',
                                                     ondelete='CASCADE'),
                           index=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(TrainerPhotos, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.link


class Dancers(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    birthday = db.Column(db.Date(), nullable=False)

    telegram_token = db.Column(db.String(100), nullable=True, index=True)
    telegram_username = db.Column(db.String(255), nullable=True)
    telegram_chat_id = db.Column(db.String(255), nullable=True)
    telegram_active = db.Column(db.Boolean, default=False)

    sms_active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='CASCADE'),
                        nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id',
                                                   ondelete='NO ACTION'), index=True,
                         nullable=False)

    attendance = db.relationship('Attendance', backref='dancer', lazy=True)
    parents = db.relationship('Parents', backref='dancer', lazy=True)
    payments = db.relationship('Payments', backref='dancer', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Dancers, self).__init__(*args, **kwargs)

    @staticmethod
    def generate_telegram_token(phone):
        return sha256(phone.encode()).hexdigest()

    def __repr__(self):
        return self.users.fio


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    from_age = db.Column(db.Integer, nullable=False)
    age_to = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    dancers = db.relationship('Dancers', backref='group', lazy=True)
    timetable = db.relationship('Timetable', backref='group', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Groups, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.from_age}-{self.age_to}'


class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='CASCADE'),
                        nullable=False)

    child_id = db.Column(db.Integer, db.ForeignKey('dancers.id',
                                                   ondelete='CASCADE'),
                         nullable=False)

    def __init__(self, *args, **kwargs):
        super(Parents, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.users.fio


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    date = db.Column(db.Date, default=datetime.now())

    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id',
                                                     ondelete="NO ACTION"),
                           index=True, nullable=False)

    timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id',
                                                       ondelete="NO ACTION"),
                             index=True, nullable=True)

    attendance = db.relationship('Attendance', backref='lessons', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Lessons, self).__init__(*args, **kwargs)


class Attendance(db.Model):
    id_child = db.Column(db.Integer, db.ForeignKey('dancers.id',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False, primary_key=True)
    id_lesson = db.Column(db.Integer, db.ForeignKey('lessons.id',
                                                    ondelete='CASCADE'),
                          index=True, nullable=False, primary_key=True)
    present = db.Column(db.Boolean, nullable=True)

    def __init__(self, *args, **kwargs):
        super(Attendance, self).__init__(*args, **kwargs)


class DaysOfTheWeek(db.Model):
    __tablename__ = 'days_of_the_week'

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    abbreviation = db.Column(db.String(10), unique=True, nullable=False)

    timetables = db.relationship('Timetable',
                                 backref='day_of_the_week', lazy=True)

    def __init__(self, *args, **kwargs):
        super(DaysOfTheWeek, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.name


class LessonTimes(db.Model):
    __tablename__ = 'lesson_times'

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    start = db.Column(db.Time, unique=True, nullable=False)
    finish = db.Column(db.Time, unique=True, nullable=False)

    timetables = db.relationship('Timetable',
                                 backref='lesson_time', lazy=True)

    def __init__(self, *args, **kwargs):
        super(LessonTimes, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.number} {self.start}:{self.finish}"


class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)

    day_of_the_week_id = db.Column(db.Integer,
                                   db.ForeignKey('days_of_the_week.id'),
                                   index=True, nullable=False)
    lesson_time_id = db.Column(db.Integer, db.ForeignKey('lesson_times.id',
                                                         ondelete='CASCADE'),
                               index=True, nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id',
                                                   ondelete='CASCADE'),
                         index=True, nullable=False)

    lesson = db.relationship('Lessons', backref='timetable', lazy=True)

    def __init__(self, *args, **kwargs):
        super(Timetable, self).__init__(*args, **kwargs)


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    date = db.Column(db.Date, default=datetime.now())

    id_dancer = db.Column(db.Integer, db.ForeignKey('dancers.id',
                                                    ondelete="CASCADE"),
                          index=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Payments, self).__init__(*args, **kwargs)


groups_alerts = db.Table('groups_alerts',
                           db.Column('id_alert', db.Integer,
                                     db.ForeignKey('alerts.id'),
                                     primary_key=True, index=True,
                                     nullable=False),
                           db.Column('id_group', db.Integer,
                                     db.ForeignKey('groups.id',
                                                   ondelete='CASCADE'),
                                     primary_key=True, index=True,
                                     nullable=False),
)


class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    date = db.Column(db.Date, default=datetime.now())
    text = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete='NO ACTION'),
                        index=True, nullable=False)

    groups = db.relationship('Groups', secondary=groups_alerts,
                             backref=db.backref('alerts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Alerts, self).__init__(*args, **kwargs)


# TODO: удалить
class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True,
                   nullable=False)
    fio = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)

    date = db.Column(db.Date, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Records, self).__init__(*args, **kwargs)


def commit_add(q):
    db.session.add(q)
    db.session.commit()
    return q


def create():
    db.create_all()

    ur = UserRoles(name="Администратор")
    ur1 = UserRoles(name="Танцор")
    ur2 = UserRoles(name="Тренер")

    nt = NewsTypes(name="Новость")

    g = Groups(from_age=7, age_to=9, price=5500)

    db.session.add_all([ur, ur1, ur2, nt, g])
    db.session.commit()

    u = Users(fio="Яковлев Артемий Александрович", phone="89125415597")
    u = commit_add(u)
    u.user_roles.append(ur)

    t = Trainers(users=u)

    n = News(title="Название статьи", text="Описание статьи", news_types=nt,
             authors=u)
    n = commit_add(n)

    db.session.add_all([u, n, t])
    db.session.commit()

    print(u, u.id)
    print(ur, ur.id)
    print(n, n.id)
    print(nt, nt.id)
    print(t, t.id)
    print(g, g.id)


if __name__ == '__main__':
    create()
    # db.drop_all()
