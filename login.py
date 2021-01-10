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

@loginblueprint.route("/login",methods = ['POST'])
def login():
    cursor = mysql.get_db().cursor()
    if request.method == 'POST':
        if request.form['action'] == "login":

            session.pop('userId', None)
            username = request.form['username']

            sql = """select idCustomers, password from customers where login like %s"""
            cursor.execute(sql, [username])
            if not cursor.fetchone()[0]:
                # TODO
                return -1

            rows = cursor.fetchone()
            userID = rows[0]
            password_ = rows[1]
            password = request.form['password']
            if password_ == password:
                session['userId'] = userID
                resp = jsonify(success=True)
                return resp
            else:
                resp = jsonify(success=False)
                return resp














