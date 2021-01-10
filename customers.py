from flask import Blueprint, jsonify, request, session
from . import mysql
from datetime import datetime

customersblueprint = Blueprint('customersblueprint', __name__)


@customersblueprint.route('/customers')
def customers():
    cursor = mysql.get_db().cursor()
    sql = "select * from customers"
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp

@customersblueprint.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customersForId(id):
    if request.method == 'PUT':
        cursor = mysql.get_db().cursor()

    elif request.method == 'DELETE':
        cursor = mysql.get_db().cursor()
        sql = """delete from customers where id = %d """
        if cursor.execute(sql, [id]):
            return 200



    else:

        cursor = mysql.get_db().cursor()

        cursor.execute('select * from customers where idCustomers= ' + str(id))
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp

