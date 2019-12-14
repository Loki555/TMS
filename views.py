from flask import render_template


def index_view():
    return render_template('index.html')


def login_view():
    return render_template('login.html')


def register_view():
    return render_template('register.html')


def mdf_user_view():
    return render_template('mdf_user.html')

