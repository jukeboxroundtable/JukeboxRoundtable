import unittest
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
