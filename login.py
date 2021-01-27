from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response,json
import jwt, datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
from . import mysql

loginblueprint = Blueprint('loginblueprint', __name__)

@loginblueprint.route("/loginjwt", methods = ['POST'])
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
    try:
        password_ = data[0]
    except TypeError:
        return jsonify({"msg": "Bad username or password"}), 401

    if password != password_:
        return jsonify({"msg": "Bad username or password"}), 401


    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

