from flask_login import confirm_login, login_user
import flask_login
import app as app
import Functions.hashFunction as hashPassword
from http import HTTPStatus
from flask import Flask, abort, request, send_from_directory, make_response, render_template
from werkzeug.datastructures import WWWAuthenticate
import flask
from Login.login_form import LoginForm
import Functions.dbFunction as db
import Functions.hashFunction as hashPassword
from Functions.checkSafeUrlFunction import checkIfSafeURL

def login(conn,form):
    if form.is_submitted():
            print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
    if form.validate_on_submit():
            username = form.username.data.lower() # Lowers the username as usernames often are not case sensetive
            password = form.password.data
            try:
                uPassword = conn.execute('SELECT password FROM users WHERE userName=?', (username,)).fetchall()[0][0] #Extracting users password from database
                salt = conn.execute('SELECT salt FROM users WHERE userName=?', (username,)).fetchall()[0][0] # Extracting users salt from database
            except IndexError as e: # If username not in database return to index page
                return render_template('./login.html', form=form)
            password = hashPassword.getHashedPassword(password, salt) #Hash the input password with correct salt
            if password == uPassword: # Compare input password hash with database 
                user = app.user_loader(username)
                # automatically sets logged in session cookie
                app.login_user(user)
                confirm_login()
                flask.flash('Logged in successfully.')
                next = flask.request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if not checkIfSafeURL(next):
                    return flask.abort(400)

                return flask.redirect(next or flask.url_for('index_html'))
    return render_template('./login.html', form=form)