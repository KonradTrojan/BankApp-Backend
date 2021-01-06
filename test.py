from flask import Blueprint, jsonify
from . import mysql

testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/test')
def test():
    conn = mysql.connect()
    cursor = conn.cursor()
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchone()
    resp=jsonify(data)
    return resp
    