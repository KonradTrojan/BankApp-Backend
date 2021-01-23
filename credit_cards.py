from flask import Blueprint, jsonify
from . import mysql

credit_cardsblueprint = Blueprint('credit_cardsblueprint', __name__)

@credit_cardsblueprint.route('/credit_cards')
def credit_cards():
    cursor = mysql.get_db().cursor()
    SQL="select * from credit_cards"
    cursor.execute(SQL)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp
    