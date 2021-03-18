from django.contrib import admin
from .models import User, Post


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    filter_horizontal = ("user_following", "user_likes",)

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "post_user", "post_content", "post_time")

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)