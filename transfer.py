from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, account_number_to_idAccounts, get_active_idAccounts_Of_Customer,is_input_json
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
transferBlueprint = Blueprint("transferBlueprint", __name__)
import re

@transferBlueprint.route("/transfer",methods=['POST'])
@jwt_required
def transfer():

    if not is_input_json(request, ['title', 'accountNumber', 'fromAccount', 'amount']):
        return jsonify({"msg": "Missing or bad JSON in request."}), 400

    title = str(request.json['title'])
    if not re.match('^[\s.,?()a-zA-Z0-9]+$'):
        return jsonify({"msg": "Allowed special characters are ,.?()"}), 401

    # Rzutowanie numerów kont na int
    try:
        toAccountNum = int(request.json['accountNumber'])
        fromAccountNum = int((request.json['fromAccount']))
    except ValueError:
        return jsonify({'msg': 'The account number must be a number.'}), 401

    if toAccountNum == fromAccountNum:
        return jsonify({'msg': 'Transfer between the same accounts is not allowed.'}), 401


    # sprawdzanie czy kwota ma odpowiedni typ i jest dodatnia
    try:
        amount = float(request.json['amount'])
        if amount <= 0:
            return jsonify({'msg': 'Amount of the transfer must be a positive number.'}), 401
    except ValueError:
        return jsonify({'msg': 'Amount of the transfer must be a number.'}), 401

    # przypisanie idAccount na podstawie numeru konta
    senderId = account_number_to_idAccounts(fromAccountNum)
    recipientId = account_number_to_idAccounts(toAccountNum)

    # sprawdzanie czy do numerów są przypisane jakieś konta
    if recipientId is None or senderId is None:
        return jsonify({'msg': 'This account does not exist.'}), 401

    # sprawdzanie czy dane konto należy do zalogowanego użytkownika
    if not isOwner(get_jwt_identity(), senderId):
        return jsonify({'msg': 'Restricted access.'}), 401

    # rozpoczęcie transakcji
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # sprawdzenie czy na kocie jest wystarczająco pięniędzy
        if not hasMoney(senderId, amount):
            return jsonify({'msg': "Nie wystarczające środki na koncie."}), 401
        balance = hasMoney(senderId, amount)

        # aktualizacja stanu konta u wysyłającego
        sql = """UPDATE accounts SET balance=(balance-%s) where idAccounts = %s"""
        cursor.execute(sql, [amount, senderId])

        # aktualizacja stanu konta u odbiorcy
        sql = """UPDATE accounts SET balance=(balance+%s) where idAccounts = %s"""
        cursor.execute(sql, [amount, recipientId])

        # dodanie do wpisu o transakcji
        sql = """INSERT INTO transactions (date, amountOfTransaction, idAccounts, idAccountsOfRecipient, 
        old_balance, new_balance, message, 	idCreditCards) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, [datetime.now(), amount, senderId, recipientId, balance, balance-amount, title, None])

        conn.commit()

    except mysql.connect.Error as error:
        # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
        cursor.rollback()
        return jsonify({'msg': "Transfer rejected", 'error': error}), 401
    finally:
        cursor.close()
        conn.close()
        return jsonify({'msg': "Transfer approved"}), 200

def hasMoney(accountsId, amount):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """SELECT balance FROM accounts WHERE idAccounts = %s """
    cursor.execute(sql, [accountsId])
    data = cursor.fetchone()

    balance = float(data[0])
    if balance - amount >= 0:
        return balance
    else:
        return False

