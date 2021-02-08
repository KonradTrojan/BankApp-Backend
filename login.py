from flask import request,Blueprint,jsonify
from flask_jwt_extended import (jwt_required, create_access_token, get_raw_jwt,
     jwt_refresh_token_required, create_refresh_token, get_jwt_identity
)
from . import mysql
from project.jwtHandler import jwt, blacklist
from project.mysqlHandler import is_input_json
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

loginblueprint = Blueprint('loginblueprint', __name__)


@loginblueprint.route("/loginjwt", methods = ['POST'])
def loginJWT():
    # sprawdzanie danych wejściowych
    if not is_input_json(request, ['username', 'password']):
        return jsonify({"msg": "Błąd związany z JSONem."}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # pobranie danych z bazy danych
    cursor = mysql.get_db().cursor()
    sql = """SELECT password, idCustomers FROM customers WHERE login LIKE %s"""
    cursor.execute(sql, [username])

    data = cursor.fetchone()
    try:
        hash_ = data[0]
        idCustomers = data[1]
    except TypeError:
        return jsonify({"msg": "Błędny login lub hasło"}), 401

    # hashowanie i porównanie haseł
    if not sha256.verify(password, hash_):
        return jsonify({"msg": "Błędny login lub hasło"}), 401
    ret = {
        'access_token': create_access_token(identity=idCustomers, expires_delta=get_expires_time()),
        'refresh_token': create_refresh_token(identity=idCustomers, expires_delta=get_expires_time())
    }
    return jsonify(ret), 200


# wylogowywanie - należy unieważnic access_token pod /logoutjwt i fresh_token pod /logoutjwtrefresh
@loginblueprint.route('/logoutjwt', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Wylogowywanie pomyślne."}), 200


@loginblueprint.route('/logoutjwtrefresh', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Wylogowywanie pomyślne."}), 200


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
        'access_token': create_access_token(identity=current_user, expires_delta=get_expires_time()),
        'refresh_token': create_refresh_token(identity=current_user, expires_delta=get_expires_time())
    }
    return jsonify(ret), 200

@loginblueprint.route('/expires_time', methods=['GET'])
@jwt_required
def expires_time():
    ret = {
        'expires_time_in_minutes': get_default_time()
    }
    return jsonify(ret), 200

def get_expires_time():
    return datetime.timedelta(minutes=get_default_time())

def get_default_time():
    minutes = 1
    return minutes
