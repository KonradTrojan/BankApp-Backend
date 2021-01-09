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
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        sql = """select login, password from customers where login like %s"""
        cursor.execute(sql, [username])
        rows = cursor.fetchall()
        userID = rows[0][0]
        password_ = rows[0][1]

        if password_ == password:
            session['userID'] = userID
            resp = jsonify(success=True)
            return resp
        else:
            resp = jsonify(success=False)
            return resp







