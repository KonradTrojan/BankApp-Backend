from flask import Blueprint, jsonify, request, session, json
from . import mysql
from datetime import datetime

accountsblueprint = Blueprint('accountsblueprint', __name__)

@accountsblueprint.route('/accounts')
def accounts():
    cursor = mysql.get_db().cursor()
    sql = """select * from accounts"""
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp

@accountsblueprint.route('/accounts/<int:id>', methods=['GET', 'POST', 'DELETE'])
def accountsForId(id):
    conn = mysql.connect()
    if request.method == 'POST' and 'balance' in request.json:
        # name = request.form['name']
        name = "xxxxxxxxxxxx"
        now = datetime.today()
        balance = request.json['balance']
        cursor = conn.cursor()
        sql = """INSERT INTO accounts (balance, dataOpened, name) VALUES ('%s', '%s', '%s')"""
        cursor.execute(sql, [balance, now, name])
        conn.commit()
        cursor.close()
        conn.close()
        return  json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    if request.method == 'DELETE':
        cursor = conn.cursor()
        sql = """SELECT idAccounts FROM owners WHERE idCustomers = '%s'"""
        cursor.execute(sql, [session['userId']])
        data = cursor.fetchone()
        idAccounts = data[0]
        sql = """DELETE FROM accounts WHERE idAccounts = '%s'"""
        cursor.execute(sql, [idAccounts])
        conn.commit()
        cursor.close()
        conn.close()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        cursor = mysql.get_db().cursor()
        sql = """select * from accounts where idAccounts= '%s'"""
        cursor.execute(sql, id)
        data = cursor.fetchall()
        resp = jsonify(data)
        conn.close()
        return resp