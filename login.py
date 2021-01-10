from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response


from . import mysql

loginblueprint = Blueprint('loginblueprint',__name__)
@loginblueprint.route("/login1",methods = ['POST','GET'])
def login1():



    session.pop('userId', None)
    #username = request.form['username']

    cursor = mysql.get_db().cursor()
    username = "trojan"
    sql = """select idCustomers, password from customers where login like %s"""
    cursor.execute(sql, [username])
    #if not cursor.fetchone()[0]:
    #    # TODO zdecydować się na jeden sposób przesyłania statusów

    #    return "error 1"

    # TODO dodać szyfrowanie haseł WSZĘDZIE
    data = cursor.fetchall()
    resp = jsonify(data)
    return resp
    userID = 1
    password_ = "123"
    password = password_
    #password = request.form['password']
    if password_ == password:
        session['userId'] = userID
        # TODO zdecydować się na jeden sposób przesyłania statusów

        return "udane logowanko"
    else:
        # TODO zdecydować się na jeden sposób przesyłania statusów

        return "nieudane logowanko"

@loginblueprint.route("/login",methods = ['POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == "login":

            session.pop('userId', None)
            username = request.form['username']

            cursor = mysql.get_db().cursor()
            sql = """select idCustomers, password from customers where login like %s"""
            cursor.execute(sql, [username])
            if not cursor.fetchone()[0]:
                # TODO zdecydować się na jeden sposób przesyłania statusów

                return "error 1"

            # TODO dodać szyfrowanie haseł WSZĘDZIE
            rows = cursor.fetchall()
            userID = 1
            password_ = "123"
            password = request.form['password']
            if password_ == password:
                session['userId'] = userID
                # TODO zdecydować się na jeden sposób przesyłania statusów
                resp = jsonify(success=True)
                return "udane logowanko"
            else:
                # TODO zdecydować się na jeden sposób przesyłania statusów
                resp = jsonify(success=False)
                return "nieudane logowanko"

@loginblueprint.route("/logout",methods = ['POST'])
def logout():
    if request.method == 'POST':
        if 'userID' in session:
            session.pop("userID")
            content = {'please move along': 'nothing to see here'}
            # TODO zdecydować się na jeden sposób przesyłania statusów
            statusCode = Response(status=200)
            return statusCode












