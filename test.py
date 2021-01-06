from flask import Blueprint

testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/test')
def test():
    return "test"