from django.contrib import admin

from blogapp.models import Post, Tag
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)