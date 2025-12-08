from django.contrib import admin
from .models import Article, Tag, Comment, Bookmark


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # slug автоматом з name


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at', 'author', 'tags')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}  # slug з title
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)  # зручний вибір тегів


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('body', 'user__username', 'article__title')
    autocomplete_fields = ('article', 'user')  # зручно, якщо багато записів


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')
    autocomplete_fields = ('user', 'article')