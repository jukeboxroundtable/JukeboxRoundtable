import os
import uuid

from flask import Flask, render_template, request, abort, session

from src.db import Firebase

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', uuid.uuid4().hex)
# src.permanent_session_lifetime = datetime.timedelta(minutes=10)
# src.session_cookie_secure = True

db = Firebase()


#############################
#      CSRF Protection      #
#############################
# For more information:
# http://flask.pocoo.org/snippets/3/
# https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.md
@app.before_request
def csrf_protect():
    """Protect against Cross-Site Forgery attacks."""
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        print("TOKEN:", token)
        print("FORM_TOKEN", request.form.get('_csrf_token'))
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    print("Before", session)
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    print("After", session)
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


#############################
#          Sessions         #
#############################
def create_session(name):
    """Create a new session.

    Sessions should contain a key for the party name and a key for a randomly
    generated token.

    Args:
        name (str): The name of a jukebox the user joined.
    """
    session['party'] = name
    session['token'] = uuid.uuid4().hex


#############################
#         Home Page         #
#############################
@app.route('/', methods=('GET', 'POST'))
def index():
    """Returns the homepage."""
    if request.method == 'POST':
        name = request.form.get('name', None)
        password = request.form.get('password', None)

        error = validate_input(name)
        if error:
            return render_template('index.html', name=name, error=error)

        name = name.upper()
        if 'create' in request.form:
            return create_jukebox(name, password, 'party' in request.form)
        elif 'join' in request.form:
            return join_jukebox(name, password)

        return render_template('index.html')
    elif request.method == 'GET':
        if 'party' in session:
            return render_template('jukebox.html')

        return render_template('index.html')


def validate_input(name):
    """Check that the user supplied name conforms to our standards.

    A name should be between 1-10 characters (inclusive) and composed of all
    alphabetic characters.

    Args:
        name (str): The name to be validated.

    Returns:
        An error message if the name is invalid, otherwise None.
    """
    if name is None:
        return "You must supply a name!"
    if len(name) > 10:
        return "Your party name is too long!"
    if len(name) < 1:
        return "Your party name must be at least 1 letter!"
    if not name.isalpha():
        return "Your party name must consist of alphabetic characters only!"


def join_jukebox(name, password):
    """Join a jukebox.

    Args:
        name (str): The name of the jukebox.
        password (str): The password of the jukebox.

    Returns:
        The jukebox page if authorization successful, otherwise the homepage.
    """
    error = db.auth_user(name, password)
    if error:
        return render_template('index.html', name=name, error=error)

    create_session(name)
    return render_template('jukebox.html')


def create_jukebox(name, password, party_mode):
    """Create a jukebox.

    Args:
        name (str): The name of the jukebox.
        password (str): The password of the jukebox.
        party_mode (bool): True if party_mode on, False otherwise

    Returns:
        The jukebox page if authorization successful, otherwise the homepage.
    """
    error = db.add_jukebox(name, password, party_mode)
    if error:
        return render_template('index.html', name=name, error=error)

    create_session(name)
    return render_template('jukebox.html')


#############################
#           About           #
#############################
@app.route('/about')
def about():
    """Show the about page."""
    return render_template('about.html')


#############################
#       Error Routes        #
#############################
@app.errorhandler(404)
def page_not_found(e):
    """Show the 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
