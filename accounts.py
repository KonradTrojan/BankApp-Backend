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
    if request.method == 'POST' and 'name' in request.form:
        cursor = mysql.get_db().cursor()
        name = request.form['name']
        now = datetime.today()
        balance = 0
        sql = """INSERT INTO accounts (balance, dataOpened, name) VALUES ('%s', '%s', '%s')"""
        cursor.execute(sql, [balance, now, name])
    if request.method == 'DELETE':
        cursor = mysql.get_db().cursor()
        sql = """SELECT idAccounts FROM owners WHERE idCustomers = '%s'"""
        cursor.execute(sql, [session['userId']])
        data = cursor.fetchone()
        idAccounts = data[0]
        sql = """DELETE FROM accounts WHERE idAccounts = '%s'"""
        cursor.execute(sql, [idAccounts])
        cursor.close()
    else:
        cursor = mysql.get_db().cursor()
        sql = """select * from accounts where idAccounts= '%s'"""
        cursor.execute(sql, id)
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp

@accountsblueprint.route('/accountsTest/<int:id>', methods=['GET', 'POST', 'DELETE'])
def accountsForIdTest(id):
    '''
    if request.method == 'POST':
        cursor = mysql.get_db().cursor()
        name = request.form['name']
        now = datetime.today()
        balance = 0
        sql = """INSERT INTO accounts (balance, dataOpened, name) VALUES (:balance, :dataOPened, :name)"""
        cursor.execute(sql, [balance, now, name])
    '''

    #if request.method == 'DELETE':
    conn = mysql.connect()
    cursor = conn.cursor()
    session['userId'] = 1
    sql = """SELECT idAccounts FROM owners WHERE idCustomers = '%s'"""
    cursor.execute(sql, [session['userId']])
    data = cursor.fetchone()
    idAccounts = data[0]


    sql = """DELETE FROM accounts WHERE idAccounts = '%s'"""
    cursor.execute(sql, 2)
    sql = """DELETE FROM owners WHERE idAccounts = '%s'"""
    cursor.execute(sql, 2)
    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    '''
    else:
        cursor = mysql.get_db().cursor()
        sql = """select * from accounts where idAccounts= :idAcc"""
        cursor.execute(sql, [id])
        data = cursor.fetchall()
        resp = jsonify(data)
        return resp
    '''