from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Blueprint
)

loginblueprint = Blueprint('loginblueprint',__name__)

@loginblueprint.route("/login",method = 'POST')
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        sql = """select login from customers where login = :username """

    return True

