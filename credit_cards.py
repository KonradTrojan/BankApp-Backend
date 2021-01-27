from flask import Blueprint, jsonify
from project.mysqlHandler import mysql, getIdsAccountsOfCustomer, getIdsCreditCardsOfAccount
from flask_jwt_extended import jwt_required, get_jwt_identity

credit_cardsblueprint = Blueprint('credit_cardsblueprint', __name__)

@credit_cardsblueprint.route('/credit_cards')
@jwt_required
def credit_cards():
    identity = get_jwt_identity()

    accountsIDs = getIdsAccountsOfCustomer(identity)
    # wpisanie do tablicy wszyskich informacji o koncie o danym id
    myJson = []
    conn = mysql.connect()
    cursor = conn.cursor()

    idCards = []
    for id in accountsIDs:
        idCards = idCards + getIdsCreditCardsOfAccount(id)

    for id in idCards:
        sql = """select idAccounts, maximumLimit, expiryDate from credit_cards where idAccounts= %s """
        cursor.execute(sql, [id])
        data = cursor.fetchall()

        userData = []
        for row in data:
            userData.append(row)

        myJson.append({
            'idCreditCards': id,
            'idAccounts': userData[0],
            'maximumLimit': userData[1],
            'expiryDate': userData[2]
        })
    return jsonify(myJson)

