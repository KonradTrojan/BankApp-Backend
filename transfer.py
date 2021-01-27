from flask import Blueprint, jsonify, request
from project.mysqlHandler import mysql, isOwner, accountNumToAccountIDt
from flask_jwt_extended import jwt_required, get_jwt_identity

transferBlueprint = Blueprint("transferBlueprint", __name__)

@transferBlueprint.route("/transfer",methods=['POST'])
@jwt_required
def transfer():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    title = request.json['title']
    amount = request.json['amount']
    accountNumber = request.json['accountNumber']
    fromAccount = request.json['fromAccount']

    receiverId = accountNumToAccountID(accountNumber)
    senderId = accountNumToAccountID(fromAccount)

    return ''

def hasMoney(accountsId, amount):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """select balance from accounts where idAccounts = %s """
    cursor.execute(sql, [accountsId])
    data = cursor.fetchall()

    balance = data[0]
    if balance - amount >= 0:
        return True
    else:
        return False


