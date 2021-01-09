from flask import Blueprint, jsonify, request
from . import mysql
from datetime import datetime

customersblueprint = Blueprint('customersblueprint', __name__)


@customersblueprint.route('/customers')
def customers():
    cursor = mysql.get_db().cursor()
    sql = """select * from customers"""
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp


@customersblueprint.route('/customers/<int:id>', methods=['GET', 'POST', 'PUT'])
def customersForId(id):
    if request.method == 'PUT':
        cursor = mysql.get_db().cursor()


    else:
        cursor = mysql.get_db().cursor()

        cursor.execute('select * from customers where idCustomers= %d', (str(id),))
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp




