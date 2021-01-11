from flask import Blueprint, jsonify, request, session
from . import mysql
from datetime import datetime

accountsblueprint = Blueprint('accountsblueprint', __name__)

@accountsblueprint.route('/accounts')
def accounts():
    cursor = mysql.get_db().cursor()
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp


@accountsblueprint.route('/accounts/<int:id>', methods=['GET', 'POST', 'DELETE'])
def accountsForId(id):
    if request.method == 'POST' and 'name' in request.form:
        cursor = mysql.get_db().cursor()
        name = request.form['name']
        now = datetime.today()
        balance = 0
        sql = """INSERT INTO accounts (balance, dataOpened, name) VALUES (:balance, :dataOPened, :name)"""
        cursor.execute(sql, [balance, now, name])
    if request.method == 'DELETE':
        cursor = mysql.get_db().cursor()
        sql = """SELECT idAccounts FROM owners WHERE idCustomers = %d"""
        cursor.execute(sql, [session['userId']])
        data = cursor.fetchone()
        idAccounts = data[0]
        sql = """DELETE FROM accounts WHERE idAccounts = %d"""
        cursor.execute(sql, [idAccounts])
        cursor.close()
    else:
        cursor = mysql.get_db().cursor()
        SQL="select * from accounts where idAccounts="+str(id)
        cursor.execute(SQL)
        data=cursor.fetchall()
        resp=jsonify(data)
        return resp
