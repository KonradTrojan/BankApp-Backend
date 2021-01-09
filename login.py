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

        #TODO  dać jakieś porządne bindowanie do sql poniżej
        sql = "select login from customers where login = " + str(username)
        cursor.execute(sql)
        data = cursor.fetchall()
        passwordFromDB = data[7]
        userID = data[1]

    else:
        sql = "select login from customers where login = 1"
        cursor.execute(sql)
        data = cursor.fetchall()
        passwordFromDB = data[7]
        userID = data[1]

        return passwordFromDB

        '''
       
        if passwordFromDB == password:
            session['userID'] = userID
            resp = jsonify(success=True)
            return resp
        else:
            resp = jsonify(success=False)
            return resp
         '''

    return True

