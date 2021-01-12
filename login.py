<<<<<<< HEAD
from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response,json


from . import mysql

loginblueprint = Blueprint('loginblueprint', __name__)
@loginblueprint.route("/login",methods = ['POST'])
def login():
    if request.method == 'POST':
        session.pop('userId', None)
        username = request.json['username']

        cursor = mysql.get_db().cursor()
        sql = """select idCustomers, password from customers where login like %s"""
        cursor.execute(sql, [username])

        # TODO dodać szyfrowanie hashowanie WSZĘDZIE
        data = cursor.fetchone()
        userId = data[0]
        password_ = data[1]

        password = request.json['password']
        if password_ == password:
            session['userId'] = userId
            return jsonify(token='test')
        else:
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}








=======
from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response,json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from . import mysql

loginblueprint = Blueprint('loginblueprint', __name__)
@loginblueprint.route("/login",methods = ['POST'])
def login():
    if request.method == 'POST':
        session.pop('userId', None)
        username = request.json['username']

        cursor = mysql.get_db().cursor()
        sql = """select idCustomers, password from customers where login like %s"""
        cursor.execute(sql, [username])

        # TODO dodać szyfrowanie hashowanie WSZĘDZIE
        data = cursor.fetchone()
        userId = data[0]
        password_ = data[1]

        password = request.json['password']
        if password_ == password:
            session['userId'] = userId
            return jsonify(token='test')
        else:
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

@loginblueprint.route("/loginjwt",methods = ['POST'])
def loginJWT():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    cursor = mysql.get_db().cursor()
    sql = """select password from customers where login like %s"""
    cursor.execute(sql, [username])

    data = cursor.fetchone()

    password_ = data[0]

    if password != password_:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200






>>>>>>> 393d128ca3073c29a190a647f513dd7473b685dd
