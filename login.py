from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Blueprint,
    jsonify
)
from . import mysql

loginblueprint = Blueprint('loginblueprint',__name__)

@loginblueprint.route("/login",methods = ['POST','GET'])
def login():
    cursor = mysql.get_db().cursor()
    #if request.method == 'GET':
    #session.pop('userId', None)
    #username = request.form['username']
    #password = request.form['password']
    username = "trojan"
    sql = """select idCustomers, password from customers where login like %s"""
    cursor.execute(sql, [username])
    rows = cursor.fetchone()
    userID = rows[0]
    password_ = rows[1]

    #session['userId'] = userID
    resp = jsonify(rows)
    return resp


    '''
        if password_ == password:
            session['userId'] = userID
            resp = jsonify(success=True)
            return resp
        else:
            resp = jsonify(success=False)
            return resp
    '''







