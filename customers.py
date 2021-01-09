from flask import Blueprint, jsonify, request
from . import mysql
from datetime import datetime

customersblueprint = Blueprint('customersblueprint', __name__)


@customersblueprint.route('/customers')
def customers():
    cursor = mysql.get_db().cursor()
    sql = """select * from customers"""
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp



