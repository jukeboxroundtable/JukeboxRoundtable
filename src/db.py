import os
import firebase_admin
from firebase_admin import db, credentials
import bcrypt


class Firebase:
    """Find more information about the Firebase API here:

    https://firebase.google.com/docs/reference/admin/python/firebase_admin.db
    """
    errors = {
        'exists': 'A jukebox with this name already exists!',
        'not_exists': 'A jukebox with this name does not exist!',
        'bad_password': 'The password is incorrect!',
    }

    def __init__(self):
        self.cred = credentials.Certificate({
            "type": os.environ['FIREBASE_TYPE'],
            "project_id": os.environ['FIREBASE_PROJECT_ID'],
            "private_key_id": os.environ['FIREBASE_PRIVATE_KEY_ID'],
            "private_key": os.environ['FIREBASE_PRIVATE_KEY'].replace("\\n",
                                                                      "\n"),
            "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
            "token_uri": os.environ['FIREBASE_TOKEN_URI'],
        })

        firebase_admin.initialize_app(
            self.cred,
            options={
                "databaseURL": os.environ['FIREBASE_DATABASE'],
                "projectId": os.environ['FIREBASE_PROJECT_ID'],
            }
        )

    def get_jukebox(self, name):
        """Retrieve the jukebox from the database.

        Args:
            name (str): The name of the jukebox to connect.

        Raises:
            ApiCallError: If an error occurs while communicating with the
                          remote database server.

        Returns:
            Union[str, None]: An error message on error or None if no error.
        """
        return db.reference("/{name}".format(name=name)).get()

    def add_jukebox(self, name, passcode, party):
        """Add a jukebox to the database.

        Args:
            name (str): The name of the jukebox
            passcode (str): The password of the jukebox. May be an empty string.
            party (bool): Whether the jukebox is in party mode.

        Raises:
            ApiCallError: If an error occurs while communicating with the
                          remote database server.

        Returns:

        TODO:
            - Update return type. Maybe True if succeeds, false otherwise?
              Raise an error if failure?
            - Store passcode only if it is not empty.
        """
        ref = db.reference('/')

        # Check if there is a jukebox with that name
        if self.get_jukebox(name):
            return Firebase.errors['exists']

        if passcode:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(bytes(passcode, 'utf-8'), salt).decode('utf-8')

            ref.update({
                name: {
                    'password': password,
                    'party_mode': party
                }
            })
        else:
            ref.update({
                name: {
                    'party_mode': party
                }
            })

        return None

    def remove_jukebox(self, name):
        """Remove the jukebox with the given name from the database.

        Args:
            name (str): The name of the jukebox to be removed.

        Raises:
            ApiCallError: If an error occurs while communicating with the
                          remote database server.

        TODO:
            - Test what happens if name doesn't exist in database.
        """
        db.reference('/{name}'.format(name=name)).delete()

    def auth_user(self, name, passcode):
        """Authenticate the user.

        Args:
            name (str): The name of the jukebox.
            passcode (str): The passcode of the jukebox.

        Raises:
            ApiCallError: If an error occurs while communicating with the
                          remote database server.

        Returns:
            Union[str, None]: An error message if there was an error,
                              None otherwise.
        """
        jukebox = self.get_jukebox(name)

        if not jukebox:
            return Firebase.errors['not_exists']

        hashed_password = jukebox.get('password')
        if not hashed_password:
            return None

        if not bcrypt.checkpw(passcode.encode(), hashed_password.encode()):
            return Firebase.errors['bad_password']

        return None
