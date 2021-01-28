from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, accountNumToAccountID, getIdsAccountsOfCustomer
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
transferBlueprint = Blueprint("transferBlueprint", __name__)

@transferBlueprint.route("/transfer",methods=['POST'])
@jwt_required
def transfer():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Rzutowanie numerów kont na int i tytułu na str
    try:
        title = str(request.json['title'])
        accountNumber = int(request.json['accountNumber'])
        fromAccount = int((request.json['fromAccount']))
    except ValueError:
        return jsonify({'msg': 'Zły tytuł lub numery kont '}), 401

    if accountNumber == fromAccount:
        return jsonify({'msg': 'Nie można dokonać transakcji między tym samym kontem '}), 401

    amount = request.json['amount']
    # sprawdzanie czy kwota ma odpowiedni typ i jest dodatnia
    if not (isinstance(amount, int) or isinstance(amount, float)):
        return jsonify({'msg': 'Zły typ kwoty przelewu'}), 401
    else:
        if amount <= 0:
            return jsonify({'msg': 'Kwota przelewu nie może być ujemna lub równa 0'}), 401

    # przypisanie idAccount na podstawie numeru konta
    senderId = accountNumToAccountID(accountNumber)
    recipientId = accountNumToAccountID(fromAccount)

    # sprawdzanie czy do numerów są przypisane jakieś konta
    if len(recipientId) == 0 or len(senderId) == 0:
        return jsonify({'msg': 'Nie istnieje taki numer konta'}), 401

    # sprawdzanie czy dane konto należy do zalogowanego użytkownika
    if isOwner(get_jwt_identity(), senderId):
        return jsonify({'msg': 'Brak dostępu do tego konta'}), 401

    # rozpoczęcie transakcji
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # sprawdzenie czy na kocie jest wystarczająco pięniędzy
        if not hasMoney(senderId, amount):
            return jsonify({'msg': "Nie wystarczające środki na koncie"}), 401
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

        # commit zmian
        conn.commit()

    except mysql.connect.Error as error:
        # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
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

