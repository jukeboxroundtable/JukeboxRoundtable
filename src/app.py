import os
import uuid

from flask import Flask, render_template, request, redirect, abort, session, \
    url_for

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
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
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
        if not error:
            return render_template('index.html', name=name, error=error)

        name = name.upper()
        if request.form.get('create'):
            return create_jukebox(name, password)
        elif request.form.get('join'):
            return join_jukebox(name, password)

        return render_template('index.html')
    elif request.method == 'GET':
        if 'party' in session:
            return redirect(url_for('jukebox', name=session['party']))

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


#############################
#         Juxeboxes         #
#############################
@app.route('/<name>', methods=['GET'])
def jukebox(name):
    """Returns the juxebox page.

    Args:
        name (str): The name of the jukebox.

    Returns:
        The jukebox page if it exists.
    """
    name = name.upper()[:10]

    party = session.get('party', None)
    if party:
        if party == name:
            return render_template('jukebox.html')
        else:
            return redirect(url_for('jukebox', name=party))

    if db.get_jukebox(name) is None:
        abort(404)

    return redirect(url_for('index'))


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
    return redirect('/{name}'.format(name=name))


def create_jukebox(name, password):
    """Create a jukebox.

    Args:
        name (str): The name of the jukebox.
        password (str): The password of the jukebox.

    Returns:
        The jukebox page if authorization successful, otherwise the homepage.
    """
    error = db.add_jukebox(name, password, True)
    if error:
        return render_template('index.html', name=name, error=error)

    create_session(name)
    return redirect('/{name}'.format(name=name))


#############################
#           About           #
#############################
@app.route('/about')
def about():
    """Show the about page."""
    return "Not yet implemented."


#############################
#       Error Routes        #
#############################
@app.errorhandler(404)
def page_not_found(e):
    """Show the 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
