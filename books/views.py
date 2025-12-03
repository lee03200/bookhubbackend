from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from .models import Book, Category, Comment, BookShelf, ReadingProgress
from .serializers import (
    BookSerializer, CategorySerializer, CommentSerializer,
    BookShelfSerializer, ReadingProgressSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """书籍视图集"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # 按分类筛选
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(Q(genre=category) | Q(categories__slug=category))
        
        # 搜索
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )
        
        # 是否会员专享
        is_premium = self.request.query_params.get('is_premium', None)
        if is_premium is not None:
            queryset = queryset.filter(is_premium=is_premium.lower() == 'true')
        
        return queryset.distinct()
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """推荐书籍"""
        books = self.get_queryset().order_by('-rating', '-heat')[:20]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """热门书籍"""
        books = self.get_queryset().order_by('-heat', '-reviews')[:20]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        book_id = self.request.query_params.get('book_id', None)
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞评论"""
        comment = self.get_object()
        comment.likes += 1
        comment.save()
        return Response({'likes': comment.likes})
    
    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        """点踩评论"""
        comment = self.get_object()
        comment.dislikes += 1
        comment.save()
        return Response({'dislikes': comment.dislikes})


class BookShelfViewSet(viewsets.ModelViewSet):
    """用户书架视图集"""
    serializer_class = BookShelfSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BookShelf.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        book_id = serializer.validated_data.get('book_id')
        # 检查是否已存在
        existing = BookShelf.objects.filter(
            user=self.request.user, 
            book_id=book_id
        ).first()
        if existing:
            return Response(
                {'detail': '该书籍已在书架中'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user, book_id=book_id)
    
    @action(detail=False, methods=['delete'])
    def remove_book(self, request):
        """从书架移除书籍"""
        book_id = request.data.get('book_id')
        if not book_id:
            return Response(
                {'detail': '请提供book_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count, _ = BookShelf.objects.filter(
            user=request.user,
            book_id=book_id
        ).delete()
        
        if deleted_count > 0:
            return Response({'detail': '移除成功'})
        return Response(
            {'detail': '该书籍不在书架中'},
            status=status.HTTP_404_NOT_FOUND
        )


class ReadingProgressViewSet(viewsets.ModelViewSet):
    """阅读进度视图集"""
    serializer_class = ReadingProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ReadingProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        book_id = serializer.validated_data.get('book_id')
        progress = serializer.validated_data.get('progress', 0)
        
        # 更新或创建
        obj, created = ReadingProgress.objects.update_or_create(
            user=self.request.user,
            book_id=book_id,
            defaults={'progress': progress}
        )
        return Response(
            ReadingProgressSerializer(obj).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
