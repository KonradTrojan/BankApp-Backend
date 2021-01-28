from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, accountNumToAccountID
from flaskext.mysql import MySQL
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
transferBlueprint = Blueprint("transferBlueprint", __name__)

@transferBlueprint.route("/transfer",methods=['POST'])
@jwt_required
def transfer():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    amount = request.json['amount']

    # Rzutowanie numerów kont na int i tytułu na str
    try:
        title = str(request.json['title'])
        accountNumber = int(request.json['accountNumber'])
        fromAccount = int((request.json['fromAccount']))
    except ValueError:
        return jsonify({'msg': 'Zły tytuł lub numery kont '}), 401

    # sprawdzanie czy kwota ma odpowiedni typ
    if not (isinstance(amount, int) or isinstance(amount, float)):
        return jsonify({'msg': 'Zły typ kwoty przelewu'}), 401

    receiverId = accountNumToAccountID(accountNumber)
    senderId = accountNumToAccountID(fromAccount)

    # TODO później wciągnąć jakoś ten warunek do commita

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        if not hasMoney(senderId, amount):
            return jsonify({'msg': "Nie wystarczające środki na koncie"}), 401
        balance = hasMoney(senderId, amount)

        sql = """UPDATE accounts SET balance=(balance-%s) where idAccounts = %s"""
        cursor.execute(sql, [amount, senderId])

        sql = """UPDATE accounts SET balance=(balance+%s) where idAccounts = %s"""
        cursor.execute(sql, [amount, receiverId])

        sql = """INSERT INTO transactions (date, amountOfTransaction, idAccounts, idAccountsOfRecipient, 
        old_balance, new_balance, message, 	idCreditCards) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, [datetime.now(), amount, senderId, receiverId, balance, balance-amount, title, None])
        conn.commit()
    except mysql.connect.Error as error:
        cursor.rollback()
        return jsonify({'msg': "Transakcja odrzucona", 'error': error}), 401
    finally:
        cursor.close()
        conn.close()
        return jsonify({'msg': "Transakcja zakończona pomyślnie"}), 200

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

