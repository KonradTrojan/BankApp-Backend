from flask import Flask, redirect, render_template, request,session,url_for,Blueprint,jsonify,Response,json


from . import mysql

loginblueprint = Blueprint('loginblueprint', __name__)
@loginblueprint.route("/login",methods = ['POST'])
def login():
    if request.method == 'POST':
        session.pop('userId', None)
        username = request.json['username']

        cursor = mysql.get_db().cursor()
        sql = """select idCustomers, password from customers where login like %s"""
        cursor.execute(sql, [username])

        # TODO dodać szyfrowanie hashowanie WSZĘDZIE
        data = cursor.fetchone()
        userId = data[0]
        password_ = data[1]

        password = request.json['password']
        if password_ == password:
            session['userId'] = userId
            return jsonify(token='test')
        else:
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}








