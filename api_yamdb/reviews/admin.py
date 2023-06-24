from django.contrib import admin
from reviews.models import Comment, Review

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role',
    )
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    search_fields = ('title', 'author__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'reviews',
        'text',
        'author',
        'pub_date'
    )
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    search_fields = ('reviews', 'author__username')
