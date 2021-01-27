from flask import Blueprint, jsonify
from . import mysql
from project.mysqlHandler import accountNumToAccountID
testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/test')
def test():


    return jsonify(accountNumToAccountID(5465565656656565))
    

   
    
