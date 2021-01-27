from flask import Blueprint, jsonify, request, session, json, jsonify
from . import mysql
from project.mysqlHandler import getIdsAccountsOfCustomer
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

transactionsblueprint = Blueprint('transactionsblueprint', __name__)

@transactionsblueprint.route('/transactions')
def transactions():
    cursor = mysql.get_db().cursor()


    SQL="select * from transactions"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp

@transactionsblueprint.route('/transactions/<int:id>', methods=['GET'])
def customersForId(id):
    cursor = mysql.get_db().cursor()
    # zwraca transakcje użytkownika o idCustomers = id z użytkownikiem o loginie request.json['login']
    if request.json['login']:
        login = request.json['login']
        # TODO


    sql = "select * from transactions owners WHERE idCustomers = '%s'"""
    cursor.execute(sql, [id])
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp
