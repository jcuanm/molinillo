from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly and that the home page loads
    def test_index(self):
	tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login page loads
    def test_login_page_loads(self):
	tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn('Please login', response.data)

    # Ensure login behaves correctly given correct credentials
    def test_correct_login(self):
	tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn('Logout', response.data)

    # Ensure login behaves correctly given incorrect credentials
    def test_incorrect_login(self):
	tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="baduser", password="baduser"),
            follow_redirects=True
        )
        self.assertIn('Invalid username or password. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_correct_logout(self):
	tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
	response = tester.get('/logout', follow_redirects=True)
        self.assertIn('Login', response.data)

if __name__ == '__main__':
    unittest.main()
