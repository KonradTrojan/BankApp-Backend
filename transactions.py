from flask import Blueprint, jsonify
from . import mysql

transactionsblueprint = Blueprint('transactionsblueprint', __name__)

@transactionsblueprint.route('/transactions')
def accounts():
    cursor = mysql.get_db().cursor()
    SQL="select * from transactions"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp
    