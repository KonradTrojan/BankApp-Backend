from flask import Blueprint, jsonify
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

def getInfoAboutTranscation(idTransactions):
    myJson = []
    conn = mysql.connect()
    cursor = conn.cursor()
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