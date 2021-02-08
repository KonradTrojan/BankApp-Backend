from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, get_active_idAccounts_Of_Customer, get_idTransfers_of_Account, get_all_idAccounts_of_Customer, is_input_json, account_number_to_idAccounts
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import render_template, make_response
import pdfkit
import datetime

transactionsblueprint = Blueprint('transactionsblueprint', __name__)

# wyświetla wszystkie transakcje danego użytkownika
@transactionsblueprint.route('/transactions', methods=['GET'])
@jwt_required
def transactionsFilter():

    if is_input_json(request, ['limit', 'offset']):
        try:
            limit = int(request.json['limit'])
            offset = int(request.json['offset'])
            if limit < 0 or offset < 0:
                return jsonify({'msg': 'Limit i Offset muszą być dodatnie.'}), 401
        except ValueError:
            return jsonify({'msg': 'Limit i offset muszą być liczbami.'}), 401

    CUSTOMER_NUMBER_FILTER = False
    if is_input_json(request, ['customerNumber']):
        try:
            customerNumber = int(request.json['customerNumber'])
            idAccCustomer = account_number_to_idAccounts(customerNumber)
            if isOwner(get_jwt_identity(), idAccCustomer):
                CUSTOMER_NUMBER_FILTER = True
            else:
                return jsonify({'msg': 'Brak dostępu.'}), 401
        except ValueError:
            return jsonify({'msg': 'Numer konta musi być liczbą.'}), 401
    else:
        return jsonify({"msg": "Błąd związany z JSONem. 1"}), 400

    FOREIGN_NUMBER_FILTER = False
    if is_input_json(request, ['foreignNumber']):
        try:
            foreignNumber = int(request.json['foreignNumber'])
            idAccForeign = account_number_to_idAccounts(foreignNumber)
            FOREIGN_NUMBER_FILTER = True
        except ValueError:
            return jsonify({'msg': 'Numer konta musi być liczbą. '}), 401

    FROM_DATE_FILTER = False
    if is_input_json(request, ['fromDate']):
        try:
            fromDate = datetime.datetime.strptime(request.json['fromDate'], '%Y-%m-%d %H:%M:%S')
            if isinstance(fromDate, datetime.date):
                FROM_DATE_FILTER = True
            else:
                return jsonify({"msg": "Zły typ daty"}), 400
        except ValueError:
            return jsonify({"msg": "Wymagana data"}), 400

    TO_DATE_FILTER = False
    if is_input_json(request, ['toDate']):
        try:
            toDate = datetime.datetime.strptime(request.json['toDate'], '%Y-%m-%d %H:%M:%S')
            if isinstance(toDate, datetime.date):
                TO_DATE_FILTER = True
            else:
                return jsonify({"msg": "Zły typ daty"}), 400
        except ValueError:
            return jsonify({"msg": "Wymagana data"}), 400

    CREDIT_CARD_FILTER = False
    if is_input_json(request, ['idCreditCard']):
        try:
            idCreditCard = int(request.json['idCreditCard'])
            CREDIT_CARD_FILTER = True
        except ValueError:
            return jsonify({'msg': 'Numer karty musi być liczbą.'}), 401

    FROM_AMOUNT_FILTER = False
    if is_input_json(request, ['fromAmount']):
        try:
            fromAmount = float(request.json['fromAmount'])
            FROM_AMOUNT_FILTER = True
        except ValueError:
            return jsonify({'msg': 'Kwota przelewu musi być liczbą.'}), 401

    TO_AMOUNT_FILTER = False
    if is_input_json(request, ['toAmount']):
        try:
            toAmount = float(request.json['toAmount'])
            TO_AMOUNT_FILTER = True
        except ValueError:
            return jsonify({'msg': 'Kwota przelewu musi być liczbą.'}), 401

    conn = mysql.connect()
    cursor = conn.cursor()

    bindingTable = []

    sql = """SELECT idAccounts, idAccountsOfRecipient, amountOfTransaction, date, old_balance, new_balance,
    message, idTransactions, idCreditCards  FROM transactions where """

    if FROM_DATE_FILTER and TO_DATE_FILTER:
        sql += """ (date BETWEEN %s AND %s) AND """
        bindingTable.append(fromDate)
        bindingTable.append(toDate)
    else:
        if FROM_DATE_FILTER:
            sql += " (date >= %s) AND "
            bindingTable.append(fromDate)
        elif TO_DATE_FILTER:
            sql += " (date <= %s) AND "
            bindingTable.append(toDate)

    if FOREIGN_NUMBER_FILTER:
        sql += """ (idAccounts = %s OR idAccountsOfRecipient = %s) AND """
        bindingTable.append(idAccForeign)
        bindingTable.append(idAccForeign)

    if CREDIT_CARD_FILTER:
        sql += """ (idCreditCards = %s) AND """
        bindingTable.append(idCreditCard)

    if FROM_AMOUNT_FILTER and TO_AMOUNT_FILTER:
        sql += """ (amountOfTransaction BETWEEN %s AND %s) AND """
        bindingTable.append(fromAmount)
        bindingTable.append(toAmount)
    else:
        if FROM_AMOUNT_FILTER:
            sql += """ (amountOfTransaction > %s) AND """
            bindingTable.append(fromAmount)
        elif TO_AMOUNT_FILTER:
            sql += """ (amountOfTransaction < %s) AND """
            bindingTable.append(toAmount)

    if CUSTOMER_NUMBER_FILTER:
        idAccCustomer = account_number_to_idAccounts(customerNumber)
        sql += """ (idAccounts = %s OR idAccountsOfRecipient = %s) """
        bindingTable.append(idAccCustomer)
        bindingTable.append(idAccCustomer)

    sql += """ ORDER BY date LIMIT %s OFFSET %s"""
    bindingTable.append(limit)
    bindingTable.append(offset)

    cursor.execute(sql, bindingTable)
    records = cursor.fetchall()

    myJson = []
    for row in records:
        myJson.append({
            'idAccounts': row[0],
            'idAccountsOfRecipient': row[1],
            'amountOfTransaction': row[2],
            'date': row[3],
            'old_balance': row[4],
            'new_balance': row[5],
            'message': row[6],
            'idTransactions': row[7],
            'idCreditCards': row[8]
        })

    return jsonify(myJson), 200


# wyświetla wszystkie transakcje danego użytkownika
@transactionsblueprint.route('/transactionsAll')
@jwt_required
def transactions():

    idAccounts = get_all_idAccounts_of_Customer(get_jwt_identity())

    transactionsId = []
    for idAcc in idAccounts:
        transactionsId = transactionsId + get_idTransfers_of_Account(idAcc)

    return get_info_about_transcation(transactionsId, 'JSON')


# wyświetla wszystkie transakcje na koncie o podanym idAccount
# TODO sprawdzić, czy potrzebne, jeśli tak to zmienić pobieranie danych z tablicy owners na allOwners
@transactionsblueprint.route('/transactions/<int:idAccount>', methods=['GET'])
@jwt_required
def transactionsOfAccount(idAccount):
    if isOwner(get_jwt_identity(), idAccount):
        idTransactions = get_idTransfers_of_Account(idAccount)
        return get_info_about_transcation(idTransactions, 'JSON')
    else:
        return jsonify({"msg": "Brak dostępu"}), 401


# generowanie PDFa
@transactionsblueprint.route('/transactions/pdf', methods=['POST'])
@jwt_required
def generatePDF():
    if request.method == 'POST':
        if not is_input_json(request, ['idTransactions']):
            return jsonify({"msg": "Błąd związany z JSONem."}), 400

        if not isinstance(request.json['idTransactions'], int):
            return jsonify({"msg": "Identyfikator transakcji musi być typu int"}), 400

        idTrans = request.json['idTransactions']

        # sprawdzanie czy transakcja należy do konta zalogowanego użytkownika
        if not is_account_of_transaction(idTrans):
            return jsonify({"msg": "Brak dostępu do tej transakcji"}), 400

        infoTrans = get_info_about_transcation(idTrans, '')

        # TODO dodać samo generowanie pdfa, najlepiej używając pakietu z flaska
        # TODO wszystko jest w infoTrans, w takiej kolejności jak dodawane są dane
        # TODO do JSONa z userData w linijce 95 tego programu

        rendered = render_template('pdf_template.html', 
            idTransactions  = idTrans, 
            idAccounts = infoTrans[0],
            idAccountsOfRecipient = infoTrans[1],
            amountOfTransaction = infoTrans[2],
            idCreditCards = infoTrans[3],
            old_balance = infoTrans[4],
            new_balance = infoTrans[5],
            message = infoTrans[6])
        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']='inline; filename=potwierdzenie-'+idTrans+'.pdf'

        return response


def is_account_of_transaction(idTransaction):

    accountsList = get_active_idAccounts_Of_Customer(get_jwt_identity())
    for idAcc in accountsList:
        for idTran in get_idTransfers_of_Account(idAcc):
            if idTran == idTransaction:
                return True
    return False


# funkcja zwraca informacje o podanej transakcji lub liście transakcji
# type = 'JSON' oznacza że zwrócony typ danych to JSON, a '', że lista
def get_info_about_transcation(idTransactions, type):
    conn = mysql.connect()
    cursor = conn.cursor()

    # spradzanie czy na wejściu jest int czy lista
    idTrans = idTransactions
    if isinstance(idTrans, int):
        idTransactions = []
        idTransactions.append(idTrans)

    myJson = []
    simpleData = []
    for id in idTransactions:
        sql = """SELECT idAccounts, idAccountsOfRecipient, amountOfTransaction, date, old_balance, new_balance,
        message FROM transactions WHERE idTransactions = %s """
        cursor.execute(sql, [id])
        data = cursor.fetchone()

        userData = []
        for row in data:
            userData.append(row)
            simpleData.append(row)

        myJson.append({
            'idTransactions ': id,
            'idAccounts': userData[0],
            'idAccountsOfRecipient': userData[1],
            'amountOfTransaction': userData[2],
            'idCreditCards': userData[3],
            'old_balance': userData[4],
            'new_balance': userData[5],
            'message': userData[6]
        })
    if type == 'JSON':
        return jsonify(myJson)
    else:
        return simpleData