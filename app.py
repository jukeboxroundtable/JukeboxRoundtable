import os

import firebase_admin
from firebase_admin import db, credentials
from flask import Flask, render_template


app = Flask(__name__)

cred = credentials.Certificate({
    "type": os.environ['FIREBASE_TYPE'],
    "project_id": os.environ['FIREBASE_PROJECT_ID'],
    "private_key_id": os.environ['FIREBASE_PRIVATE_KEY_ID'],
    "private_key": os.environ['FIREBASE_PRIVATE_KEY'].replace("\\n", "\n"),
    "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
    "token_uri": os.environ['FIREBASE_TOKEN_URI'],
})

firebase_admin.initialize_app(
  cred,
  options={
      "databaseURL": os.environ['FIREBASE_DATABASE'],
      "projectId": os.environ['FIREBASE_PROJECT_ID'],
  }
)

ARTICLES = db.reference('articles')


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
