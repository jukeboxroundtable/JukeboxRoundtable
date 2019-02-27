from flask import Flask, render_template, request, redirect, url_for, abort
from database import Firebase


app = Flask(__name__)
db = Firebase()


#############################
#         Home Page         #
#############################
@app.route('/')
def index():
    """Returns the homepage."""

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


@app.route('/create_jukebox', methods=['POST'])
def create_jukebox():
    name = request.form['name'].upper()[:10]
    password = request.form['password']

    if db.add_jukebox(name, password, True):
        return redirect('/{name}'.format(name=name))
    else:
        return redirect(url_for('index'))


#############################
#       Error Routes        #
#############################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
