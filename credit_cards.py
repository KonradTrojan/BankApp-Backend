from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, get_active_idAccounts_Of_Customer, get_idCreditCards_of_Account, isOwner, \
    is_input_json
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

credit_cardsblueprint = Blueprint('credit_cardsblueprint', __name__)


# wszystkie karty przypisane do danego użytkownika
@credit_cardsblueprint.route('/credit_cards', methods=['GET', 'DELETE', 'POST'])
@jwt_required
def credit_cards():
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.method == 'GET':
        accountsIDs = get_active_idAccounts_Of_Customer(get_jwt_identity())
        idCards = []
        for id in accountsIDs:
            idCards = idCards + get_idCreditCards_of_Account(id)

        return get_info_about_cards(idCards)

    # Usuwanie karty
    elif request.method == 'DELETE':

        if not is_input_json(request, ['idCard']):
            return jsonify({"msg": "Missing or bad JSON in request."}), 400

        idCard = request.json['idCard']

        if not isinstance(idCard, int):
            return jsonify({'msg': 'Bad type'}), 401

        idAcc = get_account_of_idCreditCards(idCard)

        if not isinstance(idAcc, int):
            return jsonify({"msg": "This card does not exist."}), 401

        if not isOwner(get_jwt_identity(), idAcc):
            return jsonify({"msg": "Access restricted"}), 401

        # rozpoczęcie transakcji
        try:

            # Usuwanie karty z bd
            sql = """DELETE FROM credit_cards where idCreditCards = %s"""
            cursor.execute(sql, [idCard])

            # commit zmian
            conn.commit()

        except mysql.connect.Error as error:
            # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
            cursor.rollback()
            return jsonify({'msg': "Connect with Data Base unsuccessfully.", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "The card has been deleted."}), 200

    elif request.method == 'POST':

        if not is_input_json(request, ['idAccount']):
            return jsonify({"msg": "Missing or bad JSON in request."}), 400

        idAcc = request.json['idAccount']

        if not isOwner(get_jwt_identity(), idAcc):
            return jsonify({"msg": "Access restricted."}), 401

        # rozpoczęcie transakcji
        try:

            # Dodawanie karty do bd
            sql = """INSERT INTO credit_cards (maximumLimit, expiryDate, idAccounts ) VALUES (%s, %s, %s)"""
            cursor.execute(sql, [5000, datetime.datetime.now() + datetime.timedelta(days=2 * 365), idAcc])

            # commit zmian
            conn.commit()

        except mysql.connect.Error as error:
            # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
            cursor.rollback()
            return jsonify({'msg': "Connect with Data Base unsuccessfully.", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "The card has been added."}), 200


# wszystkie karty przypisane do danego konta
@credit_cardsblueprint.route('/credit_cards/<int:idAccount>', methods=['GET'])
@jwt_required
def creditCardsOfAccount(idAccount):
    if isOwner(get_jwt_identity(), idAccount):
        idCards = get_idCreditCards_of_Account(idAccount)
        return get_info_about_cards(idCards)
    else:
        return jsonify({"msg": "Access restricted"}), 401


# zmiana limitu kart
@credit_cardsblueprint.route('/credit_cards/limit', methods=['POST'])
@jwt_required
def limit():
    if not is_input_json(request, ['idCard', 'limit']):
        return jsonify({"msg": "Missing or bad JSON in request."}), 400
    try:
        idCard = int(request.json['idCard'])
        limit = float(request.json['limit'])
    except ValueError:
        return jsonify({"msg": "Bad type"})

    if not isinstance(idCard, int):
        return jsonify({'msg': 'Bad type'}), 401


    if limit <= 0:
        return jsonify({'msg': 'Limit must be a number.'}), 401

    idAcc = get_account_of_idCreditCards(idCard)

    if not isinstance(idAcc, int):
        return jsonify({"msg": "This card does not exist."}), 401

    if not isOwner(get_jwt_identity(), idAcc):
        return jsonify({"msg": "Access restricted."}), 401

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = """SELECT limit """

        # Dodawanie karty do bd
        sql = """UPDATE credit_cards SET maximumLimit = %s WHERE idCreditCards = %s"""
        cursor.execute(sql, [limit, idCard])

        # commit zmian
        conn.commit()

    except mysql.connect.Error as error:
        # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
        cursor.rollback()
        return jsonify({'msg': "Connect with Data Base unsuccessfully.", 'error': error}), 401
    finally:
        cursor.close()
        conn.close()
        return jsonify({'msg': "The limit has been changed."}), 200


def get_account_of_idCreditCards(idCreditCard):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = """select idAccounts from credit_cards where idCreditCards= %s """
    cursor.execute(sql, [idCreditCard])
    data = cursor.fetchone()

    return data[0]


def get_info_about_cards(idCards):
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
