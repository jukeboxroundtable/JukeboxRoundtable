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
#          Sessions         #
#############################
def create_session(name):
    session['party'] = name
    session['token'] = uuid.uuid4().hex


#############################
#         Home Page         #
#############################
@app.route('/', methods=('GET', 'POST'))
def index():
    """Returns the homepage."""
    if request.method == 'POST':
        if request.form.get('create'):
            return create_jukebox()
        elif request.form.get('join'):
            return join_jukebox()
        return render_template('index.html')
    elif request.method == 'GET':
        print(session)
        if 'party' in session:
            return redirect(url_for('jukebox', name=session['party']))
        return render_template('index.html')


#############################
#         Juxeboxes         #
#############################
@app.route('/<name>')
def jukebox(name):
    """Returns the juxebox page."""
    name = name.upper()[:10]

    print(session)
    if 'party' in session:
        if session['party'] == name:
            return render_template('jukebox.html')
        else:
            return redirect(url_for('jukebox', name=session['party']))

    if db.get_jukebox(name) is None:
        abort(404)

    return redirect(url_for('index'))


def join_jukebox():
    name = request.form['name'].upper()[:10]
    password = request.form['password']

    error = db.auth_user(name, password)
    if error:
        return render_template('index.html', name=name, error=error)
    else:
        create_session(name)
        return redirect('/{name}'.format(name=name))


def create_jukebox():
    name = request.form['name'].upper()[:10]
    password = request.form['password']

    error = db.add_jukebox(name, password, True)
    if error:
        return render_template('index.html', name=name, error=error)
    else:
        create_session(name)
        return redirect('/{name}'.format(name=name))


#############################
#           About           #
#############################
@app.route('/about')
def about():
    return "Not yet implemented."


#############################
#       Error Routes        #
#############################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
