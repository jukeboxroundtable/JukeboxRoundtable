from flask import Flask, render_template

app = Flask(__name__)

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
@app.route('/<uid>')
def jukebox(uid):
    """Returns the juxebox page."""
    return render_template('jukebox.html')


#############################
#       Error Routes        #
#############################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
