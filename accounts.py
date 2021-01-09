from flask import Blueprint, jsonify, request
from . import mysql
from datetime import datetime

accountsblueprint = Blueprint('accountsblueprint', __name__)

@accountsblueprint.route('/accounts')
def accounts():
    cursor = mysql.get_db().cursor()
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp


@accountsblueprint.route('/accounts/<int:id>', methods=['GET', 'POST'])
def accountsForId(id):
    if request.method == 'POST' and 'name' in request.form:
        cursor = mysql.get_db().cursor()
        now = datetime.today()
        balance = 0
    else:
        cursor = mysql.get_db().cursor()
        SQL="select * from accounts where idAccounts="+str(id)
        cursor.execute(SQL)
        data=cursor.fetchall()
        resp=jsonify(data)
        return resp
