from flask import Blueprint, jsonify, request
from . import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

customersblueprint = Blueprint('customersblueprint', __name__)


@customersblueprint.route('/customer', methods=['GET'])
@jwt_required
def customer():

    if request.method == 'GET':

        # połączenie z BD
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = """select login, firstName, lastName, email, phone, dateBecomeCustomer from customers where idCustomers= %s """
        cursor.execute(sql, [get_jwt_identity()])
        data = cursor.fetchone()

        # wpisanie do tablicy wszystkich infromacji o zalogowanym użutkowniku
        userData = []
        for row in data:
            userData.append(row)

        return jsonify({
            'idCustomer': get_jwt_identity(),
            'login': userData[0],
            'firstName': userData[1],
            'lastName': userData[2],
            'email': userData[3],
            'phone': userData[4],
            'dataBecomeCustomer': userData[5]
        })


