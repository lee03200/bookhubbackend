from rest_framework import serializers
from .models import Book, Category, Comment, BookShelf, ReadingProgress
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'rating', 'reviews', 'genre', 
            'heat', 'reading', 'cover', 'description', 'is_premium',
            'publisher', 'publish_date', 'pages', 'isbn', 'categories'
        ]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'username', 'book', 'content', 'rating', 'likes', 'dislikes', 'created_at', 'updated_at']
        read_only_fields = ['likes', 'dislikes', 'created_at', 'updated_at']


class BookShelfSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = BookShelf
        fields = ['id', 'book', 'book_id', 'added_at']
        read_only_fields = ['added_at']


class ReadingProgressSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ReadingProgress
        fields = ['id', 'book', 'book_id', 'progress', 'updated_at']
        read_only_fields = ['updated_at']
