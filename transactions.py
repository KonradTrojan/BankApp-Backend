from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, get_active_idAccounts_Of_Customer, get_idTransfers_of_Account, get_all_idAccounts_of_Customer, is_input_json, account_number_to_idAccounts
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, render_template, make_response
import pdfkit

transactionsblueprint = Blueprint('transactionsblueprint', __name__)

# wyświetla wszystkie transakcje danego użytkownika
@transactionsblueprint.route('/transactions')
@jwt_required
def transactionsFilter():

    if is_input_json(request, ['limit', 'offset']):
        limit = request.json['limit']
        offset = request.json['offset']

    FROM_DATE_FILTER = False
    if is_input_json(request, ['fromDate']):
        fromDate = request.json['fromDate']
        FROM_DATE_FILTER = True

    TO_DATE_FILTER = False
    if is_input_json(request, ['toDate']):
        toDate = request.json['tpDate']
        TO_DATE_FILTER = True

    CLIENT_NUMBER_FILTER = False
    if is_input_json(request, ['clienNumber']):
        clientNumber = request.json['clienNumber']
        CLIENT_NUMBER_FILTER = True

    FOREIGN_NUMBER_FILTER = False
    if is_input_json(request, ['foreignNumber']):
        foreignNumber = request.json['foreignNumber']
        FOREIGN_NUMBER_FILTER = True

    CREDIT_CARD_FILTER = False
    if is_input_json(request, ['creditCard']):
        creditCard = request.json['creditCard']
        CREDIT_CARD_FILTER = True

    FROM_AMOUNT_FILTER = False
    if is_input_json(request, ['fromAmount']):
        fromAmount = request.json['fromAmount']
        FROM_AMOUNT_FILTER = True

    TO_AMOUNT_FILTER = False
    if is_input_json(request, ['toAmount']):
        toAmount = request.json['toAmount']
        TO_AMOUNT_FILTER = True

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        bindingTable = []

        sql = """SELECT idAccounts, idAccountsOfRecipient, amountOfTransaction, date, old_balance, new_balance,
        message, idTransactions, idCreditCards  FROM transactions where """

        if FROM_DATE_FILTER and TO_DATE_FILTER:
            sql += """ (date BEETWEN %s AND %s) AND """
            bindingTable.append(fromDate)
            bindingTable.append(toDate)
        else:
            if FROM_DATE_FILTER:
                sql += " (date >= %s) AND "
                bindingTable.append(fromDate)
            elif TO_DATE_FILTER:
                sql += " (date <= %s) AND "
                bindingTable.append(toDate)

        # TODO
        if CLIENT_NUMBER_FILTER:
            idAcc = account_number_to_idAccounts(clientNumber)
            sql += """ (idAccounts = %s OR idAccountsOfRecipient = %s) AND """
            bindingTable.append(idAcc)
            bindingTable.append(idAcc)

        if FOREIGN_NUMBER_FILTER:
            idAcc = account_number_to_idAccounts(foreignNumber)
            sql += """ (idAccounts = %s OR idAccountsOfRecipient = %s) AND """
            bindingTable.append(idAcc)
            bindingTable.append(idAcc)

        if CREDIT_CARD_FILTER:
            sql += """ (idCreditCards = %s) AND """
            bindingTable.append(creditCard)

        if FROM_AMOUNT_FILTER and TO_AMOUNT_FILTER:
            sql += """ (amountOfTransaction BEETWEN %s AND %s) """
            bindingTable.append(fromAmount)
            bindingTable.append(toAmount)
        else:
            if FROM_AMOUNT_FILTER:
                sql += """ (amountOfTransaction > %s) """
                bindingTable.append(fromAmount)
            elif TO_AMOUNT_FILTER:
                sql += """ (amountOfTransaction < %s) """
                bindingTable.append(toAmount)
            else:
                sql += """ (amountOfTransaction > %s) """
                bindingTable.append(0)


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

        return myJson

    except mysql.connect.Error as error:
        # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
        cursor.rollback()
        return jsonify({'msg': "Transakcja odrzucona", 'error': error}), 401
    finally:
        cursor.close()
        conn.close()
        return jsonify({'msg': "Transakcja zakończona pomyślnie"}), 200



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