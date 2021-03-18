from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_following = models.ManyToManyField("User", related_name="user_followers")
    user_likes = models.ManyToManyField("Post", related_name="post_likes")

class Post(models.Model):
    post_user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="posts")
    post_time = models.DateTimeField(auto_now_add=True)
    post_content = models.TextField()

    def __str__(self):
        return f"{self.post_user}: {self.post_content}"