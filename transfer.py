from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, accountNumToAccountID
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
transferBlueprint = Blueprint("transferBlueprint", __name__)

@transferBlueprint.route("/transfer",methods=['POST'])
@jwt_required
def transfer():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    title = request.json['title']
    amount = request.json['amount']
    accountNumber = request.json['accountNumber']
    fromAccount = request.json['fromAccount']

    receiverId = accountNumToAccountID(accountNumber)
    senderId = accountNumToAccountID(fromAccount)

    # TODO później wciągnąć jakoś ten warunek do commita
    if not hasMoney(senderId, amount):
        return jsonify({'msg': "Nie wystarczające środki na koncie"}), 401
    balance = hasMoney(senderId, amount)

    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """UPDATE accounts SET balance=(balance-%s) where idAccounts = %s"""
    cursor.execute(sql, [amount, senderId])

    sql = """UPDATE accounts SET balance=(balance+%s) where idAccounts = %s"""
    cursor.execute(sql, [amount, receiverId])

    sql = """INSERT INTO transactions (date, amountOfTransaction, idAccounts, idAccountsOfRecipient, 
    old_balance, new_balance, message, 	idCreditCards) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, [datetime.now(), amount, senderId, receiverId, balance, balance-amount, title, None])

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'msg': 'transkacja udana'}), 200

def hasMoney(accountsId, amount):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select balance from accounts where idAccounts = %s """
    cursor.execute(sql, [accountsId])
    data = cursor.fetchone()

    balance = float(data[0])
    if balance - amount >= 0:
        return balance
    else:
        return False

