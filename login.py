from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response,json
import jwt, datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt,
    get_jwt_claims, jwt_refresh_token_required, create_refresh_token, get_jwt_identity
)
from . import mysql
from project.jwtHandler import jwt, blacklist
loginblueprint = Blueprint('loginblueprint', __name__)

@loginblueprint.route("/loginjwt", methods = ['POST'])
def loginJWT():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # sprawdzanie danych wejściowych
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # pobranie danych z bazy danych
    cursor = mysql.get_db().cursor()
    sql = """select password, idCustomers from customers where login like %s"""
    cursor.execute(sql, [username])

    data = cursor.fetchone()
    try:
        password_ = data[0]
        idCustomers = data[1]
    except TypeError:
        return jsonify({"msg": "Bad username or password"}), 401

    # hashowanie i porównanie haseł
    # TODO dodać hashowanie
    if password != password_:
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {
        'access_token': create_access_token(identity=idCustomers),
        'refresh_token': create_refresh_token(identity=idCustomers)
    }
    return jsonify(ret), 200

# wylogowywanie
@loginblueprint.route('/logoutjwt', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

@loginblueprint.route('/logoutjwtrefresh', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

# dodawanie wygasłych tokenów do blacklisty
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@loginblueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200