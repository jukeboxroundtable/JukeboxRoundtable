import unittest
import uuid

import firebase_admin

from src import app


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['TESTING'] = True
        cls.app = app.app.test_client()

    @classmethod
    def tearDownClass(cls):
        firebase_admin.delete_app(app.db.app)

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(200, response.status_code)

    def test_404(self):
        response = self.app.get('/TESTING404')
        self.assertEqual(404, response.status_code)

    def test_validate_input(self):
        for i, name in enumerate([None, "", "AAAAAAAAAAA", "A12"]):
            with self.subTest(i=i):
                self.assertTrue(type(app.validate_input(name)) is str)

        self.assertEqual(None, app.validate_input("Test"))

    def test_create_session(self):
        with app.app.test_request_context('/'):
            name = 'test'
            app.create_session(name, host=True)
            self.assertEqual(name, app.session.get('party', None))
            self.assertTrue('token' in app.session)

    def test_clear_session(self):
        with app.app.test_request_context('/'):
            name = 'test'
            app.create_session(name, host=True)
            self.assertEqual(name, app.session.get('party', None))
            self.assertTrue('token' in app.session)

            app.clear_session()
            self.assertNotEqual(name, app.session.get('party', None))

    def test_add_jukebox_auth_user_remove_jukebox_with_password(self):
        name = 'testingWithPassword'
        password = 'testing'

        self.assertEqual(None, app.db.get_jukebox(name))
        self.assertEqual(app.Firebase.errors['not_exists'], app.db.auth_user(name, password))

        self.assertEqual(None, app.db.add_jukebox(name, password, party=True, token=uuid.uuid4().hex))
        self.assertEqual(app.Firebase.errors['exists'], app.db.add_jukebox(name, password, party=True, token=uuid.uuid4().hex))
        self.assertNotEqual(None, app.db.get_jukebox(name))
        self.assertEqual(None, app.db.auth_user(name, password))
        self.assertEqual(app.Firebase.errors['bad_password'], app.db.auth_user(name, ''))

        app.db.remove_jukebox(name)
        self.assertEqual(None, app.db.get_jukebox(name))

    def test_add_jukebox_auth_user_remove_jukebox_no_password(self):
        name = 'testingWithoutPassword'
        password = None

        self.assertEqual(None, app.db.get_jukebox(name))
        self.assertEqual(app.Firebase.errors['not_exists'], app.db.auth_user(name, password))

        self.assertEqual(None, app.db.add_jukebox(name, password, party=True, token=uuid.uuid4().hex))
        self.assertEqual(app.Firebase.errors['exists'], app.db.add_jukebox(name, password, party=True, token=uuid.uuid4().hex))
        self.assertNotEqual(None, app.db.get_jukebox(name))
        self.assertEqual(None, app.db.auth_user(name, password))

        app.db.remove_jukebox(name)
        self.assertEqual(None, app.db.get_jukebox(name))

    def test_join_jukebox_exists(self):
        name = 'testJukeboxName'
        password = None

        expected = {'party_mode': True}

        # assert this is a new jukebox
        self.assertEqual(None, app.db.get_jukebox(name))
        self.assertEqual(app.Firebase.errors['not_exists'], app.db.auth_user(name, password))

        # create the jukebox
        self.assertEqual(None, app.db.add_jukebox(name, password, party=True, token=uuid.uuid4().hex))
        self.assertEqual(app.Firebase.errors['exists'],
                         app.db.add_jukebox(name, password, party=True, token=uuid.uuid4().hex))
        self.assertNotEqual(None, app.db.get_jukebox(name))
        self.assertEqual(None, app.db.auth_user(name, password))

        # join the jukebox
        self.assertEqual(expected, app.db.get_jukebox(name))
        # self.app.join_jukebox(name, password)

        # remove the jukebox
        app.db.remove_jukebox(name)
        self.assertEqual(None, app.db.get_jukebox(name))

    def test_join_jukebox_not_exists(self):
        name = 'testing_jukebox'
        password = None

        self.assertEqual(None, app.db.get_jukebox(name))
        self.assertEqual(app.Firebase.errors['not_exists'], app.db.auth_user(name, password))

        app.db.remove_jukebox(name)
        self.assertEqual(None, app.db.get_jukebox(name))


if __name__ == '__main__':
    unittest.main()
