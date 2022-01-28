from django.contrib import admin
from .models import Profile
from .models import Post
from .models import Comment


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'created']
    date_hierarchy = 'updated'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')