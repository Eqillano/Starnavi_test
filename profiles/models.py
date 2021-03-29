from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Profile(AbstractUser):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=220, null=True,
                             blank=True, unique=True)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def create_superuser(self, email, username=None, password=None):
        profile = self.create_user(
            email=email,
            username=username,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return profile
