from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, getIdsAccountsOfCustomer, getIdsCreditCardsOfAccount, isOwner
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

credit_cardsblueprint = Blueprint('credit_cardsblueprint', __name__)

# wszystkie karty przypisane do danego użytkownika
@credit_cardsblueprint.route('/credit_cards', methods=['GET','DELETE','POST'])
@jwt_required
def credit_cards():
    if request.method == 'GET':
        accountsIDs = getIdsAccountsOfCustomer(get_jwt_identity())
        idCards = []
        for id in accountsIDs:
            idCards = idCards + getIdsCreditCardsOfAccount(id)

        return getInfoAboutCards(idCards)

    # Usuwanie karty
    elif request.method == 'DELETE':

        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        idCard = request.json['idCard']

        if not isinstance(idCard, int):
            return jsonify({'msg': 'Zły typ'}), 401

        idAcc = getAccountIdOfCard(idCard)

        if not isinstance(idAcc, int):
            return jsonify({"msg": "Nie ma takiej karty"}), 401

        if not isOwner(get_jwt_identity(), idAcc):
            return jsonify({"msg": "Brak dostępu"}), 401

        # rozpoczęcie transakcji
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Usuwanie karty z bd
            sql = """DELETE FROM credit_cards where idCreditCards = %s"""
            cursor.execute(sql, [idCard])

            # commit zmian
            conn.commit()

        except mysql.connect.Error as error:
            # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
            cursor.rollback()
            return jsonify({'msg': "Transakcja odrzucona", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "Karta usunięta pomyślnie"}), 200

    elif request.method == 'POST':

        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        idAcc = request.json['idAccount']

        if not isOwner(get_jwt_identity(), idAcc):
            return jsonify({"msg": "Brak dostępu"}), 401

        # rozpoczęcie transakcji
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Dodawanie karty do bd
            sql = """INSERT INTO credit_cards (maximumLimit, expireDate, idAccounts ) VALUES (%s, %s, %s)"""
            cursor.execute(sql, [5000, datetime.datetime.now() + datetime.timedelta(days=2*365), idAcc])

            # commit zmian
            conn.commit()

        except mysql.connect.Error as error:
            # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
            cursor.rollback()
            return jsonify({'msg': "Transakcja odrzucona", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "Karta dodane pomyślnie"}), 200


# wszystkie karty przypisane do danego konta
@credit_cardsblueprint.route('/credit_cards/<int:idAccount>', methods=['GET'])
@jwt_required
def creditCardsOfAccount(idAccount):
    if isOwner(get_jwt_identity(), idAccount):
        idCards = getIdsCreditCardsOfAccount(idAccount)
        return getInfoAboutCards(idCards)
    else:
        return jsonify({"msg": "Brak dostępu"}), 401


def getAccountIdOfCard(idCreditCard):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = """select idAccounts from credit_cards where idCreditCards= %s """
    cursor.execute(sql, [idCreditCard])
    data = cursor.fetchone()

    return data[0]


def getInfoAboutCards(idCards):
    myJson = []
    conn = mysql.connect()
    cursor = conn.cursor()
    for id in idCards:
        sql = """select idAccounts, maximumLimit, expiryDate from credit_cards where idCreditCards= %s """
        cursor.execute(sql, [id])
        data = cursor.fetchone()

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