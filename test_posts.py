from app import app
from unittest import TestCase

class UsersTestCase(TestCase):
    # Integration Tests for Posts
    def test_post_form(self):
        with app.test_client() as client:
            res = client.get('/users/1/posts/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="post_title" class="form-label">Title</label>', html)

    def test_post_process(self):
        with app.test_client() as client:
            res = client.post('/users/1/posts/new', data={'post_title': 'test title', 'post_content': 'test content'})

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users/1')

    def test_post_details(self):
        with app.test_client() as client:
            res = client.get('/posts/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<title>SQLAlchemy - Blogly - Post Details</title>', html)

    def test_post_edit_form(self):
        with app.test_client() as client:
            res = client.get('/posts/1/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)

    def test_post_delete_process(self):
        with app.test_client() as client:
            res = client.get('/posts/1/delete')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users/1')

