from flask import Blueprint, jsonify, request, session, json
from project.mysqlHandler import mysql, get_active_idAccounts_Of_Customer, isOwner, is_input_json
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt_identity

accountsblueprint = Blueprint('accountsblueprint', __name__)


@accountsblueprint.route('/accounts', methods=['GET', 'DELETE', 'POST'])
@jwt_required
def accountsOfCustomer():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'GET':
        # wpisanie do tablicy wszyskich informacji o koncie o danym id
        accountsIDs = get_active_idAccounts_Of_Customer(get_jwt_identity())
        myJson = []

        for idAcc in accountsIDs:

            sql = """select number, dataOpened, balance from accounts where idAccounts= %s """
            cursor.execute(sql, [idAcc])
            data = cursor.fetchone()

            userData = []
            for row in data:
                userData.append(row)

            myJson.append({
                'idAccounts': idAcc,
                'number': userData[0],
                'dataOpened': userData[1],
                'balance': userData[2]
            })

        return jsonify(myJson)

    # Usuwanie konta
    elif request.method == 'DELETE':

        if not is_input_json(request, ['idAccounts']):
            return jsonify({"msg": "Missing JSON in request"}), 400

        idAccounts = request.json['idAccounts']

        if not isinstance(idAccounts, int):
            return jsonify({'msg': 'Zły typ'}), 401

        if not isOwner(get_jwt_identity(),idAccounts):
            return jsonify({'msg': 'Brak dostępu'}), 401

        # rozpoczęcie transakcji
        try:

            # Usuwanie konta - triggery w BD zadbają, żeby usunąć wszystkie wpisy powiązane z tym kontem
            sql = """DELETE FROM accounts where idAccounts = %s"""
            cursor.execute(sql, [idAccounts])

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

    # Dodawanie kont
    elif request.method == 'POST':

        # rozpoczęcie transakcji
        try:

            # Dodawanie karty do bd
            sql = """INSERT INTO owners (idCustomers) VALUES (%s)"""
            cursor.execute(sql, [get_jwt_identity()])
            # commit zmian
            conn.commit()

            cursor = conn.cursor()
            # Dodawanie karty do bd
            sql = """UPDATE accounts SET dataOpened = %s WHERE dataOpened is NULL"""
            cursor.execute(sql, [datetime.now()])
            # commit zmian
            conn.commit()

        except mysql.connect.Error as error:
            # przy wystąpieniu jakiegoś błędu, odrzucenie transakcji
            cursor.rollback()
            return jsonify({'msg': "Transakcja odrzucona", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "Konto dodane pomyślnie"}), 200


