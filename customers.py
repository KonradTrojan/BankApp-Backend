from flask import Blueprint, jsonify, request, session, json
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

@customersblueprint.route('/customers/<int:id>', methods=['GET', 'DELETE'])
def customersForId(id):
    conn = mysql.connect()
    if request.method == 'DELETE':
        cursor = conn.cursor()
        sql = """delete from customers where id = '%s' """
        cursor.execute(sql, [id])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        cursor = conn.cursor()
        cursor.execute('''select * from customers where idCustomers= '%s' ''', [id])
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp

