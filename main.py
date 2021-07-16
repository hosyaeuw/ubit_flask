from app import app

from dancers.blueprint import blueprint_dancers
from trainers.blueprint import blueprint_trainers
from users.blueprint import blueprint_users
from groups.blueprint import blueprint_groups
from news_types.blueprint import blueprint_news_types
from news.blueprint import blueprint_news
from attendance.blueprint import blueprint_attendance
from lessons.blueprint import blueprint_lessons
from lesson_times.blueprint import blueprint_lesson_times
from timetable.blueprint import blueprint_timetable
from payments.blueprint import blueprint_payments
from records.blueprint import blueprint_records
from trainer_office.blueprint import blueprint_trainer_office

from sms.blueprint import blueprint_sms
from telegram.blueprint import blueprint_telegram
from alerts.blueprint import blueprint_alerts

app.register_blueprint(blueprint_news_types, url_prefix='/api/news_types')
app.register_blueprint(blueprint_dancers, url_prefix='/api/dancers')
app.register_blueprint(blueprint_groups, url_prefix='/api/groups')
app.register_blueprint(blueprint_trainers, url_prefix='/api/trainers')
app.register_blueprint(blueprint_users, url_prefix='/api/users')
app.register_blueprint(blueprint_news, url_prefix='/api/news')
app.register_blueprint(blueprint_attendance, url_prefix='/api/attendance')
app.register_blueprint(blueprint_lessons, url_prefix='/api/lessons')
app.register_blueprint(blueprint_timetable, url_prefix='/api/timetable')
app.register_blueprint(blueprint_lesson_times, url_prefix='/api/lesson_times')
app.register_blueprint(blueprint_payments, url_prefix='/api/payments')
app.register_blueprint(blueprint_records, url_prefix='/api/records')
app.register_blueprint(blueprint_trainer_office,
                       url_prefix='/api/trainer_office')

app.register_blueprint(blueprint_alerts, url_prefix='/api/alerts')
app.register_blueprint(blueprint_telegram, url_prefix='/telegram')
app.register_blueprint(blueprint_sms, url_prefix='/sms')

if __name__ == '__main__':
    app.run()
