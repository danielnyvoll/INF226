from flask_login import login_user
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

def login(conn,form):
    print("KJØRR")
    if form.is_submitted():
            print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
            print(request.form)
    if form.validate_on_submit():
            username = form.username.data.lower() # Lowers the username as usernames often are not case sensetive
            password = form.password.data
            try:
                uPassword = conn.execute('SELECT password FROM users WHERE userName=?', (username,)).fetchall()[0][0] #Extracting users password from database
                salt = conn.execute('SELECT salt FROM users WHERE userName=?', (username,)).fetchall()[0][0] # Extracting users salt from database
                print(uPassword)
                print(salt)
            except IndexError as e: # If username not in database return to index page
                return render_template('./login.html', form=form)
            password = hashPassword.getHashedPassword(password, salt) #Hash the input password with correct salt
            if password == uPassword: # Compare input password hash with database 
                user = app.user_loader(username)
                # automatically sets logged in session cookie
                app.login_user(user)

                flask.flash('Logged in successfully.')
                next = flask.request.args.get('next')
                print("HEYEHEYEYHEYEHYEHEYE")
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if False and not is_safe_url(next):
                    return flask.abort(400)

                return flask.redirect(next or flask.url_for('index'), variable=username)
    return render_template('./index.html', form=form, variable=username)