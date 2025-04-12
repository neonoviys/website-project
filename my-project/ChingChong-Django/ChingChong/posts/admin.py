from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rating', 'review', 'publish')

# @admin.register(PostInfo)
# class PostInfoAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'user', 'post', 'rating')