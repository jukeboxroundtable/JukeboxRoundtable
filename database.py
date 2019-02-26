import os
import firebase_admin
from firebase_admin import db, credentials

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

ref = db.reference('/')


def get_jukebox(name):
    return db.reference("/{name}".format(name=name)).get()


def add_jukebox(name, passcode, party):
    if get_jukebox(name) is not None:
        print("can't add")
    else:
        print("adding...")
        ref.update({
            name: {
                'passcode': passcode,
                'party_mode': party
            }})


def remove_jukebox(name):
    pass


def auth_user(name, passcode):
    if get_jukebox(name)['passcode'] == passcode:
        print("authenticated")
    else:
        print("not the correct passcode.")
