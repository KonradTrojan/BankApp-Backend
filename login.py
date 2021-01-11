from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response


from . import mysql

loginblueprint = Blueprint('loginblueprint',__name__)
@loginblueprint.route("/login",methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        session.pop('userId', None)
        username = request.form['username']

        cursor = mysql.get_db().cursor()
        sql = """select idCustomers, password from customers where login like %s"""
        cursor.execute(sql, [username])

        # TODO dodać szyfrowanie haseł WSZĘDZIE
        data = cursor.fetchone()
        userID = data[0]
        password_ = data[1]

        password = request.form['password']
        if password_ == password:
            session['userId'] = userID
            # TODO zdecydować się na jeden sposób przesyłania statusów

            return "udane logowanko"
        else:
            # TODO zdecydować się na jeden sposób przesyłania statusów

            return "nieudane logowanko"
'''
@loginblueprint.route("/login1",methods = ['POST','GET'])
def loginTest():



    session.pop('userId', None)

    username = "trojan"
    cursor = mysql.get_db().cursor()
    sql = """select idCustomers, password from customers where login like %s"""
    cursor.execute(sql, [username])


    # TODO dodać szyfrowanie haseł WSZĘDZIE
    data = cursor.fetchone()
    if data[0]  and data[1] is not None:
        userID = data[0]
        password_ = data[1]
        password =password_
        if password_ == password:
            session['userId'] = userID
            # TODO zdecydować się na jeden sposób przesyłania statusów
            resp = jsonify(success=True)
            return "udane logowanko"
        else:
            # TODO zdecydować się na jeden sposób przesyłania statusów
            resp = jsonify(success=False)
            return "nieudane logowanko"
    else:
        return "blad"
@loginblueprint.route("/logout", methods = ['POST'])
def logout():
    if request.method == 'POST':
        if 'userID' in session:
            session.pop("userID")
            content = {'please move along': 'nothing to see here'}
            # TODO zdecydować się na jeden sposób przesyłania statusów
            statusCode = Response(status=200)
            return statusCode
'''











