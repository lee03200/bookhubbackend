# bookhub/views.py
from rest_framework import viewsets, status, permissions, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import Book, UserProfile, UserBookShelf, Review
from .serializers import (
    UserSerializer, UserProfileSerializer, BookListSerializer,
    BookDetailSerializer, UserBookShelfSerializer, ReviewSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'genre']
    ordering_fields = ['heat', 'rating', 'publish_date']
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.request.content_params.get('category')
        if category and category != '全部':
            queryset = queryset.filter(genre=category)

        user = self.request.user
        if user.is_authenticated:
            try:
                is_vip = user.userprofile.is_vip and user.userprofile.vip_expire_date > timezone.now().date()
            except UserProfile.DoesNotExist:
                is_vip = False
        else:
            is_vip = False

        if not is_vip:
            queryset = queryset.filter(is_vip_only=False)

        return queryset

    @action(detail=False, methods=['get'])
    def popular(self, request):
        books = Book.objects.order_by('-heat')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def recommended(self, request):
        user_books = UserBookShelf.objects.filter(user=request.user).values_list('book', flat=True)
        if not user_books:
            books = Book.objects.order_by('-heat')[:10]
        else:
            rated_genres = Review.objects.filter(
                user=request.user, book_id__in=user_books
            ).values_list('book__genre', flat=True).distinct()
            if rated_genres:
                books = Book.objects.filter(genre__in=rated_genres).exclude(id__in=user_books).order_by('-rating')[:10]
            else:
                books = Book.objects.order_by('-heat')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class ShelfViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        shelf_items = UserBookShelf.objects.filter(user=request.user).select_related('book')
        books = [item.book for item in shelf_items]
        user_profile = getattr(request.user, 'userprofile', None)
        is_vip = user_profile and user_profile.is_vip and user_profile.vip_expire_date > timezone.now().date()
        max_capacity = "unlimited" if is_vip else 10

        serializer = BookListSerializer(books, many=True)
        return Response({
            "max_capacity": max_capacity,
            "books": serializer.data
        })

    @action(detail=False, methods=['post'])
    def add(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            raise ValidationError("book_id is required")

        book = Book.objects.get(id=book_id)

        current_count = UserBookShelf.objects.filter(user=request.user).count()
        user_profile = getattr(request.user, 'userprofile', None)
        is_vip = user_profile and user_profile.is_vip and user_profile.vip_expire_date > timezone.now().date()

        if not is_vip and current_count >= 10:
            raise PermissionDenied("普通用户最多收藏10本书")

        UserBookShelf.objects.get_or_create(user=request.user, book=book)
        return Response({"message": "已加入书架"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        UserBookShelf.objects.filter(user=request.user, book_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        book_id = self.request.content_params.get('book_id')
        if book_id:
            return Review.objects.filter(book_id=book_id).select_related('user')
        return Review.objects.none()

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        review, created = Review.objects.update_or_create(
            user=self.request.user,
            book=book,
            defaults={
                'rating': serializer.validated_data['rating'],
                'content': serializer.validated_data.get('content', '')
            }
        )
        avg_rating = Review.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
        book.rating = avg_rating or 0
        book.reviews_count = Review.objects.filter(book=book).count()
        book.save()