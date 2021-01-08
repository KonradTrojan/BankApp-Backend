from flask import Blueprint, jsonify
from . import mysql

testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/test')
def test():
    cursor = mysql.get_db().cursor()
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchall()
    resp=jsonify(data)
    return resp
    

   
    
