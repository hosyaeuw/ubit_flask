from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask_sslify import SSLify

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

CORS(app)
# sslify = SSLify(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from flask_jwt import JWT
from jwt_file import authenticate, identity

jwt = JWT(app, authenticate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user': {
            'user_id': identity.id,
            'login': identity.login,
            'roles': [
                role.name for role in identity.user_roles
            ]
        }
    })
