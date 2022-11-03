from http import HTTPStatus
from flask import Flask, Response, abort, request, send_from_directory, make_response, render_template, session
from werkzeug.datastructures import WWWAuthenticate
import flask
import secrets

from zmq import NULL
from Login.login_form import LoginForm
from json import dumps, loads
from base64 import b64decode
from apsw import Error
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import NameHighlightFilter, KeywordCaseFilter
from pygments import token;
from threading import local
from markupsafe import escape
import Functions.hashFunction as hashPassword
import Functions.dbFunction as initializeDb
from Login.login_logic import login as loginUser
import Login.login_logic as login_logic
from Register.registrer import makeUser
from Register.register_form import RegisterForm
from flask_wtf.csrf import CSRFProtect
from Messages.send_message import sendMessage
from Messages.search_messages import searchInMessage
from Messages.announcements_messages import checkAnnouncements

tls = local()
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
conn = initializeDb.run()

# Set up app
app = Flask(__name__)
csrf = CSRFProtect(app)

# The secret key enables storing encrypted session data in a cookie 
app.secret_key = secrets.token_hex(32)

# Add a login manager to the app
import flask_login
from flask_login import fresh_login_required, login_remembered, login_required, login_user, logout_user
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


users = {'alice' : {'password' : 'password123', 'token' : 'tiktok'},
         'bob' : {'password' : 'bananas'}
         }

def getUserNames():
    names = conn.execute('SELECT userName FROM users').fetchall()
    accountnames = []
    for name in names:
        accountnames.append(name[0])
        print("NAMES:" + name[0])
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


# This method is called to get a User object based on a request,
# for example, if using an api key or authentication token rather
# than getting the user name the standard way (from the session cookie)
@login_manager.request_loader
def request_loader(request):
    # Even though this HTTP header is primarily used for authentication
    # rather than authorization, it's still called "Authorization".
    auth = request.headers.get('Authorization')

    # If there is not Authorization header, do nothing, and the login
    # manager will deal with it (i.e., by redirecting to a login page)
    if not auth:
        return

    (auth_scheme, auth_params) = auth.split(maxsplit=1)
    auth_scheme = auth_scheme.casefold()
    if auth_scheme == 'basic':  # Basic auth has username:password in base64
        (uid,passwd) = b64decode(auth_params.encode(errors='ignore')).decode(errors='ignore').split(':', maxsplit=1)
        print(f'Basic auth: {uid}:{passwd}')
        u = users.get(uid)
        if u: # and check_password(u.password, passwd):
            return user_loader(uid)
    elif auth_scheme == 'bearer': # Bearer auth contains an access token;
        # an 'access token' is a unique string that both identifies
        # and authenticates a user, so no username is provided (unless
        # you encode it in the token – see JWT (JSON Web Token), which
        # encodes credentials and (possibly) authorization info)
        print(f'Bearer auth: {auth_params}')
        for uid in users:
            if users[uid].get('token') == auth_params:
                return user_loader(uid)
    # For other authentication schemes, see
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication

    # If we failed to find a valid Authorized header or valid credentials, fail
    # with "401 Unauthorized" and a list of valid authentication schemes
    # (The presence of the Authorized header probably means we're talking to
    # a program and not a user in a browser, so we should send a proper
    # error message rather than redirect to the login page.)
    # (If an authenticated user doesn't have authorization to view a page,
    # Flask will send a "403 Forbidden" response, so think of
    # "Unauthorized" as "Unauthenticated" and "Forbidden" as "Unauthorized")
    abort(HTTPStatus.UNAUTHORIZED, www_authenticate = WWWAuthenticate('Basic realm=inf226, Bearer'))

def pygmentize(text):
    if not hasattr(tls, 'formatter'):
        tls.formatter = HtmlFormatter(nowrap = True)
    if not hasattr(tls, 'lexer'):
        tls.lexer = SqlLexer()
        tls.lexer.add_filter(NameHighlightFilter(names=['GLOB'], tokentype=token.Keyword))
        tls.lexer.add_filter(NameHighlightFilter(names=['text'], tokentype=token.Name))
        tls.lexer.add_filter(KeywordCaseFilter(case='upper'))
    return f'<span class="highlight">{highlight(text, tls.lexer, tls.formatter)}</span>'

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

@app.route('/createUser.html', methods=['POST','GET'])
def create_user():
    return render_template("createUser.html")

@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    return render_template("index.html")
    #return send_from_directory(app.root_path,
                       # 'index.html', mimetype='text/html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        if(makeUser(username, password,conn)):
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
def search():
    return searchInMessage(request,conn)

@app.route('/send', methods=['POST','GET'])
def send():
    return sendMessage(request,conn)

@app.get('/announcements')
def announcements():
    return checkAnnouncements(conn)

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
