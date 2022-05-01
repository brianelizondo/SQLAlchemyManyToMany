from app import app
from unittest import TestCase

class UsersTestCase(TestCase):
    # Integration Tests
    def test_users_redirect(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')

    def test_users_list(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
    
    def test_user_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_user_process(self):
        with app.test_client() as client:
            res = client.post('/users/new', data={'first_name': 'test first', 'last_name': 'test last', 'image_url': 'http://www.testurl.com'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')
    
    def test_user_details(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a class="btn btn-outline-secondary btn-sm" href="/users" role="button">Go Back</a>', html)
    
    def test_user_edit_form(self):
        with app.test_client() as client:
            res = client.get('/users/1/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)
    
    def test_user_delete_process(self):
        with app.test_client() as client:
            res = client.get('/users/1/delete')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')