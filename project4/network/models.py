from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(blank=True, null=True)
    following = models.IntegerField(blank=True, null=True)
    posts = models.IntegerField(blank=True, null=True)
    pfp = models.TextField(default="https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg")
    
class Follow(models.Model):
    profile = models.IntegerField(blank=True, null=True)
    follower_list = models.ManyToManyField(User, null=True, blank=True, related_name="follower_list")
    following_list = models.ManyToManyField(User, null=True, blank=True, related_name="following_list")

    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postAuthor')
    likes = models.IntegerField(blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)
    body = models.CharField(max_length=600, blank=True, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    
    def like_count(self):
        return Like.objects.filter(post=self).count()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likeUser')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likePost')

    
    
class Comment(models.Model):
    body = models.CharField(max_length=600, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentAuthor')



    
