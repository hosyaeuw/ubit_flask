import datetime


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost/unitedbit'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/unitedbit'
    SECRET_KEY = "database"
    UPLOAD_FOLDER = './static/media'
    # SQLALCHEMY_ECHO = True
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=3600)
