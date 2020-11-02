from django.contrib import admin
from .models import Post, UserPostLike, Comment

admin.site.register(Post)
admin.site.register(UserPostLike)
admin.site.register(Comment)