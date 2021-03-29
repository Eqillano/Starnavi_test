from django.contrib import admin

# Register your models here.
from . models import PostLike, Post

admin.site.register(Post)

admin.site.register(PostLike)
