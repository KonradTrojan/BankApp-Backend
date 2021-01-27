import os
from flask import Flask
from project.mysqlHandler import mysql
from project.accounts import accountsblueprint
from project.transactions import transactionsblueprint
from project.credit_cards import credit_cardsblueprint
from project.customers import customersblueprint
from project.login import loginblueprint
from project.jwtHandler import jwt, blacklist

def create_app(test_config=None):
    # utworzenie nowej instacji aplikacji
    randomString = "bZmgFwcMtloKpnjYjgLcPIU9WDDGFobSFpZGaHMsgG2ck28g5Y6H940Y1OhLgG2ck28g5Y6H940Y1OhLSOlj7W5TPgZjNFsyV3w7"
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=randomString,
    )

    # konfigurowanie danych dla flask_jwt
    app.config['JWT_SECRET_KEY'] = randomString  # Change this!
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    jwt.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = 'g18'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'gd5qbk7z'
    app.config['MYSQL_DATABASE_DB'] = 'g18'
    app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
    mysql.init_app(app)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(accountsblueprint)
    app.register_blueprint(transactionsblueprint)
    app.register_blueprint(credit_cardsblueprint)
    app.register_blueprint(customersblueprint)
    app.register_blueprint(loginblueprint)

    return app
