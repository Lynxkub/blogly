from unittest import TestCase

from app import app
from models import db, User, Post
from datetime import datetime
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()
now=datetime.now()
class UserTestCase(TestCase):
    """Tests for users"""

    def setUp(self):
        """Adds a sample user"""

        User.query.delete()

        user=User(first_name='John', last_name='Doe', image_url='https://images.unsplash.com/photo-1602664976515-0f159e7d08a9?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8am9obiUyMGRvZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60')
        post=Post(title='Test', content='Test Content', created_at=now)
        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()
        self.user_id=user.id
        self.post_id=post.id
    def tearDown(self):
        """Clean up any users"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp=client.get('/')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/users')

    def test_user_page(self):
        with app.test_client() as client:
            resp=client.get(f'/{self.user_id}')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>John Doe</h3>', html)

   
            

    def test_add_user_page(self):
        with app.test_client() as client:
            resp=client.get('/users/new')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('URL for Profile Picture', html)

    def test_edit_post(self):
        with app.test_client() as client:
            resp=client.get(f'/edit_post{self.post_id}')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)

    def test_delete_post(self):
        with app.test_client() as client:
            resp=client.post(f'/delete_post{self.post_id}')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            