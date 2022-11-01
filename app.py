from http import HTTPStatus
from flask import Flask, abort, request, send_from_directory, make_response, render_template, redirect, session
from werkzeug.datastructures import WWWAuthenticate
import flask
from login_form import LoginForm
from json import dumps, loads
from base64 import b64decode
import sys
import apsw
from apsw import Error
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import NameHighlightFilter, KeywordCaseFilter
from pygments import token;
from threading import local
import flask_login
from flask_login import login_required, login_user, logout_user
import hashlib

tls = local()
inject = "'; insert into messages (sender,message) values ('foo', 'bar');select '"
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
conn = None

# Set up app
app = Flask(__name__)
# The secret key enables storing encrypted session data in a cookie (make a secure random key for this!)
app.secret_key = 'mY s3kritz'

# Add a login manager to the app


login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def evalute_password(input, username):
    """
    Given a username and an input, evaluate the input against the real password.
    :param input: Password input.
    :param username: Name of the user that wants to login.
    :return: Do the passwords match?
    """
    u = get_current_user(username)
    salt = u['password'][1]
    # Apply hash function on user input.
    h_1 = hashlib.sha256(str.encode(input)).digest()
    # Convert result form hash function to integer and perform XOR-operation with salt.
    h_1 = int.from_bytes(h_1, 'big')
    add_salt = h_1 ^ salt
    # Apply hash function another time.
    h_2 = hashlib.sha256(add_salt.to_bytes(32, 'big')).hexdigest()
    # Check if the two passwords match.
    return h_2 == u['password'][0]


def setsession(username):
    session['username'] = username
    print(f"The session has been Set")


def getsession():
    if 'username' in session:
        username = session['username']
        print(f"Welcome {username}")
        return True
    else:
        print("Welcome Anonymous")
        return False


def popsession():
    session.pop('username', None)
    print("Session Deleted")


def get_current_user(username):
    try:
        """
        {'password': ('9432b8b17e4a6a2bab351cf92fa62f4391c174aeac12904f5cf8bb4afc4fe297',
                      0xBFDBF58A677F96595E938A53D9F8539D), 'token': 'tiktok'}
                      """
        stmt = f"SELECT password FROM login_data WHERE username='{username}'"
        c_password = conn.execute(stmt)
        password = c_password.fetchall()[0][0]
        stmt = f"SELECT salt FROM login_data WHERE username='{username}'"
        c_salt = conn.execute(stmt)
        salt = int(c_salt.fetchall()[0][0], 16)
        stmt = f"SELECT token FROM login_data WHERE username='{username}'"
        c_token = conn.execute(stmt)
        token = c_token.fetchall()[0][0]
        return {'password': (password, salt), 'token': token}
    except Error as e:
        return f'ERROR: {e}', 500


def get_users():
    try:
        stmt = f"SELECT username FROM login_data"
        c = conn.execute(stmt)
        users = c.fetchall()
        return [user[0] for user in users]
    except Error as e:
        return f'ERROR: {e}', 500


# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(flask_login.UserMixin):
    pass


# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id):
    if user_id not in get_users():
        return

    # For a real app, we would load the User from a database or something
    user = User()
    user.id = user_id
    return user

password123
# This method is called to get a User object based on a request,
# for example, if using an api key or authentication token rather
# than getting the user name the standard way (from the session cookie)
@login_manager.request_loader
def request_loader(request):
    # Even though this HTTP header is primarily used for *authentication*
    # rather than *authorization*, it's still called "Authorization".
    auth = request.headers.get('Authorization')

    # If there is not Authorization header, do nothing, and the login
    # manager will deal with it (i.e., by redirecting to a login page)
    if not auth:
        return

    (auth_scheme, auth_params) = auth.split(maxsplit=1)
    auth_scheme = auth_scheme.casefold()
    if auth_scheme == 'basic':  # Basic auth has username:password in base64
        (uid, passwd) = b64decode(auth_params.encode(errors='ignore')).decode(errors='ignore').split(':', maxsplit=1)
        print(f'Basic auth: {uid}:{passwd}')
        u = get_current_user(uid)
        if u:  # and check_password(u.password, passwd):
            return user_loader(uid)
    elif auth_scheme == 'bearer':  # Bearer auth contains an access token;
        # an 'access token' is a unique string that both identifies
        # and authenticates a user, so no username is provided (unless
        # you encode it in the token – see JWT (JSON Web Token), which
        # encodes credentials and (possibly) authorization info)
        print(f'Bearer auth: {auth_params}')
        for uid in get_users():
            cur = get_current_user(uid)
            if cur.get('token') == auth_params:
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
    abort(HTTPStatus.UNAUTHORIZED, www_authenticate=WWWAuthenticate('Basic realm=inf226, Bearer'))


def pygmentize(text):
    if not hasattr(tls, 'formatter'):
        tls.formatter = HtmlFormatter(nowrap=True)
    if not hasattr(tls, 'lexer'):
        tls.lexer = SqlLexer()
        tls.lexer.add_filter(NameHighlightFilter(names=['GLOB'], tokentype=token.Keyword))
        tls.lexer.add_filter(NameHighlightFilter(names=['text'], tokentype=token.Name))
        tls.lexer.add_filter(KeywordCaseFilter(case='upper'))
    return f'<span class="highlight">{highlight(text, tls.lexer, tls.formatter)}</span>'


@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    getsession()
    return send_from_directory(app.root_path,
                               'index.html', mimetype='text/html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = get_current_user(username)
        if u and evalute_password(password, username):
            user = user_loader(username)

            # automatically sets logged in session cookie
            login_user(user)

            flask.flash('Logged in successfully.')
            get_current_user(username)
            get_users()
            setsession(username)

            next = flask.request.args.get('next')

            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if False and not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
    return render_template('./login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    popsession()
    return redirect(".")


@app.get('/search')
def search():
    is_session = getsession()
    if not is_session:
        return redirect('.')
    query = request.args.get('q') or request.form.get('q') or '*'
    user = session['username']
    stmt = f"SELECT * FROM messages WHERE message GLOB '{query}' AND sender='{user}'"
    result = f"Query: {pygmentize(stmt)}\n"
    try:
        c = conn.execute(stmt)
        rows = c.fetchall()
        result = result + 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)


@app.get('/messages')
def messages():
    is_session = getsession()
    if not is_session:
        return redirect('.')
    query = '*'
    user = session['username']
    stmt = f"SELECT * FROM messages WHERE sender='{user}'"
    result = f"Querry for messages: {pygmentize(stmt)}\n"
    try:
        c = conn.execute(stmt)
        rows = c.fetchall()
        result = result + 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)


@app.get('/message/<int:ID>')
def message_id(ID):
    is_session = getsession()
    if not is_session:
        return redirect('.')
    # query = request.args.get('q') or request.form.get('q') or '*'
    user = session['username']
    stmt = f"SELECT * FROM messages WHERE id = {ID} AND sender='{user}'"
    result = f"Querry for messages: {pygmentize(stmt)}\n"
    try:
        c = conn.execute(stmt)
        rows = c.fetchall()
        result = result + 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)


@app.route('/new', methods=['POST', 'GET'])
def new():
    is_session = getsession()
    if not is_session:
        return redirect('.')
    try:
        sender = session['username']
        message = request.args.get('message') or request.args.get('message')
        if not sender or not message:
            return f'ERROR: missing sender or message'
        stmt = f"INSERT INTO messages (sender, message) values ('{sender}', '{message}');"
        result = f"Query: {pygmentize(stmt)}\n"
        conn.execute(stmt)
        return f'{result}ok'
    except Error as e:
        return f'{result}ERROR: {e}'


@app.route('/send', methods=['POST', 'GET'])
def send():
    is_session = getsession()
    if not is_session:
        return redirect('.')
    try:
        sender = session['username']
        message = request.args.get('message') or request.args.get('message')
        if not sender or not message:
            return f'ERROR: missing sender or message'
        stmt = f"INSERT INTO messages (sender, message) values ('{sender}', '{message}');"
        result = f"Query: {pygmentize(stmt)}\n"
        conn.execute(stmt)
        return f'{result}ok'
    except Error as e:
        return f'{result}ERROR: {e}'

try:
    conn = apsw.Connection('./tiny.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id integer PRIMARY KEY, 
        sender TEXT NOT NULL,
        message TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS login_data (
            id integer PRIMARY KEY, 
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            token TEXT);''')
    """
    c.execute('''INSERT INTO login_data (username, password, salt, token)
                values ('alice', '9432b8b17e4a6a2bab351cf92fa62f4391c174aeac12904f5cf8bb4afc4fe297',
                '0xBFDBF58A677F96595E938A53D9F8539D', 'tiktok');''')
    c.execute('''INSERT INTO login_data (username, password, salt, token)
                    values ('bob', '203fcc0dd6e6ad4aa4ae72b5c284756fd52628e0017af2e5dc3f7135acc0c545',
                    '0x542CA2AD7A731B6118A3F7541F0C8831', 'tiktok');''')
    """
    # c.execute('''CREATE TABLE IF NOT EXISTS announcements (
    #     id integer PRIMARY KEY,
    #     author TEXT NOT NULL,
    #     text TEXT NOT NULL);''')
except Error as e:
    print(e)
    sys.exit(1)
