from flask import Blueprint, jsonify, request, session, json
from . import mysql
from flask_jwt_extended import jwt_required, get_jwt_claims
from project.jwtHandler import jwt, blacklist
customersblueprint = Blueprint('customersblueprint', __name__)


# TODO /customers należy usunąć, chyba że dodajemy tryb administratora
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
def customersForId():
    conn = mysql.connect()
    if request.method == 'DELETE':
        cursor = conn.cursor()
        sql = """delete from customers where id = '%s' """
        cursor.execute(sql, [id])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        claims = get_jwt_claims()
        return claims, 200

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select login, firstName, lastName, email, phone, dateBecomeCustomer from customers where idCustomers= %s """
    cursor.execute(sql, [identity])
    data = cursor.fetchone()

    userData = []
    for row in data:
        userData.append(row)

    return {
        'idCustomer': identity,
        'login': userData[0],
        'firstName': userData[1],
        'lastName': userData[2],
        'email': userData[3],
        'phone': userData[4],
        'dataBecomeCustomer': userData[5]
    }
