from flask import Blueprint, jsonify
import project.__init__

testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/test')
def test():
    SQL="select * from accounts"
    cursor.execute(SQL)
    data=cursor.fetchone()
    resp=jsonify(data)
    return resp
    