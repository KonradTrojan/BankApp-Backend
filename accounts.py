from flask import Blueprint, jsonify, request, session, json
from project.mysqlHandler import mysql, getIdsAccountsOfCustomer
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt_identity

accountsblueprint = Blueprint('accountsblueprint', __name__)

@accountsblueprint.route('/allaccounts')
def accounts():
    cursor = mysql.get_db().cursor()
    sql = """select * from accounts"""
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp

@accountsblueprint.route('/accounts', methods=['GET'])
@jwt_required
def accountsOfCustomer():
    identity = get_jwt_identity()

    # połączenie z bd
    '''
    
    sql = """select idAccounts from owners where idCustomers= %s """
    cursor.execute(sql, [identity])
    data = cursor.fetchall()

    # wpisanie do tablicy id wszystkich kont zalogowanego użytkownika
    accountsIDs = []
    for row in data:
        accountsIDs.append(row[0])
    '''
    accountsIDs = getIdsAccountsOfCustomer(identity)
    # wpisanie do tablicy wszyskich informacji o koncie o danym id
    myJson = []
    conn = mysql.connect()
    cursor = conn.cursor()
    for id in accountsIDs:

        sql = """select number, dataOpened, balance from accounts where idAccounts= %s """
        cursor.execute(sql, [id])
        data = cursor.fetchone()

        userData = []
        for row in data:
            userData.append(row)

        myJson.append({
            'idAccounts': id,
            'number': userData[0],
            'dataOpened': userData[1],
            'balance': userData[2]
        })

    return jsonify(myJson)

# TODO poniższe usunąć, gdy nie będzie już potrzebne
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

