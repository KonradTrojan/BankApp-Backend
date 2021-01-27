from flask import Blueprint, jsonify
from . import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

credit_cardsblueprint = Blueprint('credit_cardsblueprint', __name__)

@credit_cardsblueprint.route('/credit_cards')
@jwt_required
def credit_cards():
    identity = get_jwt_identity()
    cursor = mysql.get_db().cursor()
    SQL = "select * from credit_cards"
    cursor.execute(SQL)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp


