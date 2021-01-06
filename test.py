from flask import Blueprint, jsonify
from project.__init__ import cursor

testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/test')
def test():
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchone()
    resp=jsonify(data)
    return resp
    