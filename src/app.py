import os
import time
import urllib.request
import uuid

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, abort, session
from flask_socketio import SocketIO, emit

from src.db import Firebase
from src.about import about_blueprint
from src.error import error_blueprint

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', uuid.uuid4().hex)

app.register_blueprint(about_blueprint)
app.register_blueprint(error_blueprint)

# socketio = SocketIO(app, async_mode='eventlet')
socketio = SocketIO(app)

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
        else:
            session['token'] = uuid.uuid4().hex


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


#############################
#          Sockets          #
#############################
@socketio.on('connect')
def test_connect():
    print('Connected!')


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

    if 'token' not in session:
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
    error = db.add_jukebox(name, password, party_mode, session.get('token'))
    if error:
        return render_template('index.html', name=name, error=error)

    return render_template('jukebox.html', host=True)


#############################
#        Youtube API        #
#############################
@socketio.on('song_search')
def song_search(text):
    def parse_id(string):
        return string.split('/watch?v=', 1)[1]

    query = urllib.parse.quote(text['search'])
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    json_out = []
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        href = vid['href']
        if '/watch?v=' in href:
            vid_id = parse_id(href)
            json_out.append(
                {
                    'id': vid_id,
                    'title': vid['title'],
                    'thumbnail': 'https://i.ytimg.com/vi/' + vid_id + '/default.jpg',
                    'url': 'https://www.youtube.com' + href
                }
            )
    emit('search_results', {'data': json_out})


if __name__ == '__main__':
    socketio.run(app)
