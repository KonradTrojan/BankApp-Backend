from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, conn, isOwner, account_number_to_idAccounts, get_active_idAccounts_Of_Customer,is_input_json
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
transferBlueprint = Blueprint("transferBlueprint", __name__)

#conn = mysql.connect()
#cursor = conn.cursor()

@transferBlueprint.route("/transfer",methods=['POST'])
@jwt_required
def transfer():

    if not is_input_json(request, ['title', 'accountNumber', 'fromAccount', 'amount']):
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Rzutowanie numerów kont na int i tytułu na str
    try:
        title = str(request.json['title'])
        toAccountNum = int(request.json['accountNumber'])
        fromAccountNum = int((request.json['fromAccount']))
    except ValueError:
        return jsonify({'msg': 'Zły tytuł lub numery kont '}), 401

    if toAccountNum == fromAccountNum:
        return jsonify({'msg': 'Nie można dokonać transakcji między tym samym kontem '}), 401

    amount = request.json['amount']
    # sprawdzanie czy kwota ma odpowiedni typ i jest dodatnia
    if not (isinstance(amount, int) or isinstance(amount, float)):
        return jsonify({'msg': 'Zły typ kwoty przelewu'}), 401
    else:
        if amount <= 0:
            return jsonify({'msg': 'Kwota przelewu nie może być ujemna lub równa 0'}), 401

    # przypisanie idAccount na podstawie numeru konta
    senderId = account_number_to_idAccounts(fromAccountNum)
    recipientId = account_number_to_idAccounts(toAccountNum)

    # sprawdzanie czy do numerów są przypisane jakieś konta
    if recipientId is None or senderId is None:
        return jsonify({'msg': 'Nie istnieje taki numer konta'}), 401

    # sprawdzanie czy dane konto należy do zalogowanego użytkownika
    if not isOwner(get_jwt_identity(), senderId):
        return jsonify({'msg': 'Brak dostępu do tego konta'}), 401

    # rozpoczęcie transakcji
    try:

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

    sql = """select balance from accounts where idAccounts = %s """
    cursor.execute(sql, [accountsId])
    data = cursor.fetchone()

    balance = float(data[0])
    if balance - amount >= 0:
        return balance
    else:
        return False

