from flask import Blueprint, jsonify
import project.__init__.mysql

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
    