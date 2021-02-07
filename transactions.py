from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, get_active_idAccounts_Of_Customer, get_idTransfers_of_Account, get_all_idAccounts_of_Customer, is_input_json
from flask_jwt_extended import jwt_required, get_jwt_identity

transactionsblueprint = Blueprint('transactionsblueprint', __name__)


# wyświetla wszystkie transakcje danego użytkownika
@transactionsblueprint.route('/transactions')
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

        return ''


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