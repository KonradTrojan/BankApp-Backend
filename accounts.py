from flask import Blueprint, jsonify
from . import mysql

accountsblueprint = Blueprint('accountsblueprint', __name__)

@accountsblueprint.route('/accounts')
def accounts():
    cursor = mysql.get_db().cursor()
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp

@accountsblueprint.route('/accounts/<int:id>')
def accountsForId(id):
    cursor = mysql.get_db().cursor()

    SQL="select * from accounts where idAccounts="+str(id) 
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp

@testblueprint.route('/accounts1', methods=['GET'])
def test1():
    cursor = mysql.get_db().cursor()
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp
