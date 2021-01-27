from flask import Blueprint, jsonify, request, session, json
from . import mysql
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
from project.jwtHandler import jwt
customersblueprint = Blueprint('customersblueprint', __name__)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql="""select idCustomer, firstName, lastName, email, phone, dateBecomeCustomer from customers where login= '%s' """
    cursor.execute(sql, [identity])
    data = cursor.fetchone()
    idCustomer = data[0]
    firstName = data[1]
    lastName = data[2]
    email = data[3]
    phone = data[4]
    dataBecomeCustomer = data[5]
    return {
        'login': identity,
        'idCustomer': idCustomer,
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'phone': phone,
        'dataBecomeCustomer': dataBecomeCustomer
    }

@customersblueprint.route('/customers')
def customers():
    cursor = mysql.get_db().cursor()
    sql = "select * from customers"
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp

@customersblueprint.route('/customer/', methods=['GET', 'DELETE'])
@jwt_required
def customersForId(id):
    conn = mysql.connect()
    if request.method == 'DELETE':
        cursor = conn.cursor()
        sql = """delete from customers where id = '%s' """
        cursor.execute(sql, [id])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        #claims = get_jwt_claims()
       # return claims, 200
       return None

