from flask import Flask, Response, abort, request, send_from_directory, make_response, render_template, session
from werkzeug.datastructures import WWWAuthenticate
import flask
import secrets
from zmq import NULL
from Login.login_form import LoginForm
from json import dumps, loads
from base64 import b64decode
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from threading import local
import Functions.dbFunction as initializeDb
from Login.login_logic import login as loginUser
from Register.registrer import makeUser
from Register.register_form import RegisterForm
from flask_wtf.csrf import CSRFProtect
from Messages.send_message import sendMessage
from Messages.search_messages import searchInMessage
from Messages.getMessages_messages import getMessages
from Functions.checkSafeUrlFunction import checkIfSafeURL

tls = local()
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
# Set up database
conn = initializeDb.run()

# Set up app
app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True
)
csrf = CSRFProtect(app)

# The secret key enables storing encrypted session data in a cookie 
app.secret_key = secrets.token_hex(128)

# Add a login manager to the app
import flask_login
from flask_login import fresh_login_required, login_remembered, login_required, login_user, logout_user
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def getUserNames():
    names = conn.execute('SELECT userName FROM users').fetchall()
    accountnames = []
    for name in names:
        accountnames.append(name[0])
    return accountnames

# Class to store user info
# UserMixin provides us with an id field and the necessary
# methods (is_authenticated, is_active, is_anonymous and get_id())
class User(flask_login.UserMixin):
    possibleReceivers = []


# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id):
    # For a real app, we would load the User from a database or something
    user = User()
    user.id = user_id
    user.possibleReceivers = getUserNames()
    session["username"] = user_id
    return user

@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(app.root_path, 'favicon.png', mimetype='image/png')

@app.route('/index.js')
def index_js():
    return send_from_directory(app.root_path, 'templates/index.js', mimetype='text/javascript')

@app.route('/index.css')
def index_css():
    return send_from_directory(app.root_path, 'templates/index.css', mimetype='text/css')

@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    return render_template("index.html")

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        if(makeUser(username, password,conn)):
            next = flask.request.args.get('next')
            if(not checkIfSafeURL(next)):
                return abort(400)
            return flask.redirect(flask.url_for('login'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return loginUser(conn,form);

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return flask.redirect(flask.url_for('index_html'))

@app.get('/search')
@login_required
def search():
    return searchInMessage(request,conn)

@app.route('/send', methods=['POST','GET'])
@login_required
def send():
    return sendMessage(request,conn)

@app.get('/getmessages')
@login_required
def announcements():
    return getMessages(request,conn)

@app.get('/coffee/')
def nocoffee():
    abort(418)

@app.route('/coffee/', methods=['POST','PUT'])
def gotcoffee():
    return "Thanks!"

@app.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy']='default-src \'self\''
    return resp

