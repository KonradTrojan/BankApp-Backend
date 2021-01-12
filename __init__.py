import os
from flask import Flask,session, redirect, escape, url_for
from flaskext.mysql import MySQL

mysql = MySQL()

from project.accounts import accountsblueprint
from project.transactions import transactionsblueprint
from project.credit_cards import credit_cardsblueprint
from project.customers import customersblueprint
from project.login import loginblueprint
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    # obsługa jwt
    app.config['JWT_SECRET_KEY'] = 'dsanjasdnldIOI932DHQ9xJISDHJIHF9u90euxdjqidsasdccatser'  # Change this!
    jwt = JWTManager(app)


    app.secret_key='dfHBKsdjknsda9320ijod2f90cnwiodwdsa'
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

    #global mysql connection
    conn = mysql.connect()
    cursor = conn.cursor()

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
