from flask import Flask, render_template, request, redirect, url_for, abort
from database import Firebase


app = Flask(__name__)
db = Firebase()


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
        return render_template('index.html')


#############################
#         Juxeboxes         #
#############################
@app.route('/<name>')
def jukebox(name):
    """Returns the juxebox page."""
    name = name.upper()[:10]

    jukebox = db.get_jukebox(name)

    if jukebox is None:
        abort(404)
    else:
        return render_template('jukebox.html')


def join_jukebox():
    name = request.form['name'].upper()[:10]
    password = request.form['password']

    error = db.auth_user(name, password)
    if error:
        return render_template('index.html', name=name, error=error)
    else:
        return redirect('/{name}'.format(name=name))


def create_jukebox():
    name = request.form['name'].upper()[:10]
    password = request.form['password']

    error = db.add_jukebox(name, password, True)
    if error:
        return render_template('index.html', name=name, error=error)
    else:
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
