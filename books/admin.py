from django.contrib import admin
from .models import Book, Category, Comment, BookShelf, ReadingProgress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'rating', 'genre', 'is_premium', 'heat']
    list_filter = ['is_premium', 'genre']
    search_fields = ['title', 'author']
    filter_horizontal = ['categories']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'created_at', 'likes', 'dislikes']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title', 'content']

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'book__title']

@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'progress', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'book__title']
