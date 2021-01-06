import os
from flask import Flask
from flaskext.mysql import MySQL
from test import testblueprint

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
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

    #mysql
    mysql = MySQL()
 
    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = 'g18'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'gd5qbk7z'
    app.config['MYSQL_DATABASE_DB'] = 'g18'
    app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
    mysql.init_app(app)

    #global mysql connection
    conn = mysql.connect()
    global cursor 
    cursor = conn.cursor()

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(testblueprint)
    return app
