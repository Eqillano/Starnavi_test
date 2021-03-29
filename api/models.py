from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from django.conf import settings

# Create your models here.


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    pub_date = models.DateField(format('%Y-%m-%d'), auto_now_add=True)


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Publication Date', auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='post_user', blank=True, through=PostLike)
    num_likes = models.IntegerField(default=0)
