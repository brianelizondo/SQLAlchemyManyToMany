from app import app
from unittest import TestCase

class UsersTestCase(TestCase):
    # Integration Tests for Tags
    def test_tags_list(self):
        with app.test_client() as client:
            res = client.get('/tags')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)
    
    def test_tag_details(self):
        with app.test_client() as client:
            res = client.get('/tags/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<title>SQLAlchemy - Blogly - Tag Details</title>', html)
    
    def test_tag_form(self):
        with app.test_client() as client:
            res = client.get('/tags/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="name" class="form-label">Name</label>', html)
    
    def test_tag_process(self):
        with app.test_client() as client:
            res = client.post('/tags/new', data={'name': 'example'})

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/tags')
    
    def test_tag_edit_form(self):
        with app.test_client() as client:
            res = client.get('/tags/1/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Edit a tag</h1>', html)
    
    def test_tag_delete_process(self):
        with app.test_client() as client:
            res = client.get('/tags/5/delete')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/tags')

