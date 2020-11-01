from django.contrib import admin
from .models import Post, UserPostLike

admin.site.register(Post)
admin.site.register(UserPostLike)