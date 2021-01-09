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


@customersblueprint.route('/customers/<int:id>', methods=['GET', 'POST'])
def customersForId(id):
    if request.method == 'POST' and 'name' in request.form:
        cursor = mysql.get_db().cursor()
        name = request.form['name']
        now = datetime.today()
        balance = 0

    else:
        cursor = mysql.get_db().cursor()
        SQL = "select * from accounts where idCustomers= "+str(id)
        cursor.execute(SQL, id)
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp




