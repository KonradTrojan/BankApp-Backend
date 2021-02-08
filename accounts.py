from flask import Blueprint, jsonify, request
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
            return jsonify({"msg": "Missing or bad JSON in request."}), 400

        try:
            idAccounts = int(request.json['idAccounts'])
        except ValueError:
            return jsonify({"msg": "Bad type."}), 400

        if not isOwner(get_jwt_identity(), idAccounts):
            return jsonify({'msg': 'Restricted access'}), 401

        # rozpoczęcie transakcji
        try:
            sql = """SELECT balance FROM accounts WHERE idAccounts = %s"""
            cursor.execute(sql, [idAccounts])
            data = cursor.fetchone()

            if data[0] == 0:
                # Usuwanie konta - triggery w BD zadbają, żeby usunąć wszystkie wpisy powiązane z tym kontem
                sql = """DELETE FROM accounts WHERE idAccounts = %s"""
                cursor.execute(sql, [idAccounts])

                # commit zmian
                conn.commit()
            else:
                return jsonify({"msg": "The account cannot be deleted. Transfer the money first."})

        except mysql.connect.Error as error:
            cursor.rollback()
            return jsonify({'msg': "Connect with Data Base unsuccessfully.", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "The account has been deleted."}), 200

    # Dodawanie kont
    elif request.method == 'POST':

        try:

            # Dodawanie konta do bd
            sql = """INSERT INTO owners (idCustomers) VALUES (%s)"""
            cursor.execute(sql, [get_jwt_identity()])
            conn.commit()

            cursor = conn.cursor()
            sql = """UPDATE accounts SET dataOpened = %s WHERE dataOpened IS NULL"""
            cursor.execute(sql, [datetime.now()])
            conn.commit()

        except mysql.connect.Error as error:
            cursor.rollback()
            return jsonify({'msg': "Connect with Data Base unsuccessfully.", 'error': error}), 401
        finally:
            cursor.close()
            conn.close()
            return jsonify({'msg': "The account has been added"}), 200


