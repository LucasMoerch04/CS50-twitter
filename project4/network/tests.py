from django.test import TestCase
from network.models import User, Post, Comment

# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        #Create user
        user = User.objects.create(username="Test1", email="Mail1", password="AAA", followers=12, following=10,posts=1)
        
        #Create Post
        Post.objects.create(author=user, likes="1", comments="2", body="this is a test")
        
    def test_posts_count(self):
        pass
        
        
        
        