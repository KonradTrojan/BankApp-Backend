from flask import Blueprint, jsonify, request, session, json, jsonify
from . import mysql
from project.mysqlHandler import mysql, getIdsAccountsOfCustomer, getIdsTransferOfAccount
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

transactionsblueprint = Blueprint('transactionsblueprint', __name__)

@transactionsblueprint.route('/transactions')
@jwt_required
def transactions():
    identity = get_jwt_identity()
    idAccounts = getIdsAccountsOfCustomer(identity)

    transactionsId = []
    for id in idAccounts:
        transactionsId = transactionsId + getIdsTransferOfAccount(id)

    return getInfoAboutTranscation(transactionsId)

@transactionsblueprint.route('/transations/<int:intAccount>', methods='GET')
@jwt_required
def transactionsOfAccount(intAccount):
    idTransactions = getIdsTransferOfAccount(intAccount)
    return getInfoAboutTranscation(idTransactions)

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