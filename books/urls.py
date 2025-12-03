from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, CommentViewSet, BookShelfViewSet, ReadingProgressViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'bookshelf', BookShelfViewSet, basename='bookshelf')
router.register(r'reading-progress', ReadingProgressViewSet, basename='reading-progress')

urlpatterns = [
    path('', include(router.urls)),
]
