from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, getIdsAccountsOfCustomer, getIdsTransferOfAccount
from flask_jwt_extended import jwt_required, get_jwt_identity

transactionsblueprint = Blueprint('transactionsblueprint', __name__)


# wyświetla wszystkie transakcje danego użytkownika
@transactionsblueprint.route('/transactions')
@jwt_required
def transactions():
    identity = get_jwt_identity()
    idAccounts = getIdsAccountsOfCustomer(identity)

    transactionsId = []
    for id in idAccounts:
        transactionsId = transactionsId + getIdsTransferOfAccount(id)

    return getInfoAboutTranscation(transactionsId)


# wyświetla wszystkie transakcje na koncie o podanym idAccount
@transactionsblueprint.route('/transactions/<int:idAccount>', methods=['GET'])
@jwt_required
def transactionsOfAccount(idAccount):
    if isOwner(get_jwt_identity(),idAccount):
        idTransactions = getIdsTransferOfAccount(idAccount)
        return getInfoAboutTranscation(idTransactions)
    else:
        return jsonify({"msg": "Brak dostępu"}), 401


# generowanie PDFa
@transactionsblueprint.route('/transactions/pdf', methods=['POST'])
@jwt_required
def generatePDF():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        if not isinstance(request.json['idTransactions'], int):
            return jsonify({"msg": "IdTransactions musi być typu int"}), 400

        idTrans = request.json['idTransactions']

        # sprawdzanie czy transakcja należy do konta zalogowanego użytkownika
        if not isOwnerOfTransaction(idTrans):
            return jsonify({"msg": "Brak dostępu do tej transakcji"}), 400

        infoTrans = getInfoAboutTranscation(idTrans)


        return str(infoTrans.json['idAccounts'])


def isOwnerOfTransaction(idTransaction):

    accountsList = getIdsAccountsOfCustomer(get_jwt_identity())
    for idAcc in accountsList:
        for idTran in getIdsTransferOfAccount(idAcc):
            if idTran == idTransaction:
                return True
    return False


def getInfoAboutTranscation(idTransactions):
    myJson = []
    conn = mysql.connect()
    cursor = conn.cursor()

    idTrans = idTransactions
    if isinstance(idTrans,int):
        idTransactions = []
        idTransactions.append(idTrans)

    for id in idTransactions:
        sql = """select idAccounts, idAccountsOfRecipient, amountOfTransaction, date, old_balance, new_balance,
        message from transactions where idTransactions = %s """
        cursor.execute(sql, [id])
        data = cursor.fetchone()

        userData = []
        for row in data:
            userData.append(row)

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
    return jsonify(myJson)