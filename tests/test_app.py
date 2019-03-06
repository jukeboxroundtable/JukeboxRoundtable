import unittest
from src import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

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


if __name__ == '__main__':
    unittest.main()
