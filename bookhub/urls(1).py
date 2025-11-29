# bookhub/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookhub.views import  (
UserViewSet,
UserProfileView,
BookViewSet,
ReviewViewSet,
ShelfViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'books', BookViewSet, basename='book')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'shelf', ShelfViewSet, basename='shelf')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
]