from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    UpdateProfileSerializer, UserProfileSerializer
)
from books.models import BookShelf, ReadingProgress, Comment
from books.serializers import BookShelfSerializer, ReadingProgressSerializer, CommentSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            # 获取或创建token
            token, created = Token.objects.get_or_create(user=user)
            
            # 返回用户信息和token
            user_serializer = UserSerializer(user)
            return Response({
                'token': token.key,
                'user': user_serializer.data
            })
        else:
            return Response(
                {'detail': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """用户注册"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # 创建token
        token = Token.objects.create(user=user)
        
        # 返回用户信息和token
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """用户登出"""
    # 删除token
    request.user.auth_token.delete()
    return Response({'detail': '登出成功'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """获取当前用户信息"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """更新用户资料"""
    profile = request.user.profile
    serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # 返回更新后的完整用户信息
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats_view(request):
    """获取用户统计信息"""
    user = request.user
    
    # 书架统计
    bookshelf_count = BookShelf.objects.filter(user=user).count()
    
    # 阅读进度统计
    reading_progress = ReadingProgress.objects.filter(user=user)
    total_books = reading_progress.count()
    
    # 计算本月阅读数（简化版，实际应该按月份统计）
    this_month = reading_progress.filter(progress__gte=50).count()
    
    # 评论统计
    comments_count = Comment.objects.filter(user=user).count()
    
    # 平均评分
    avg_rating = 0
    if comments_count > 0:
        ratings = Comment.objects.filter(user=user).values_list('rating', flat=True)
        avg_rating = round(sum(ratings) / len(ratings), 1)
    
    return Response({
        'total': total_books,
        'thisMonth': this_month,
        'avgRating': avg_rating,
        'bookshelfCount': bookshelf_count,
        'commentsCount': comments_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_shelf_view(request):
    """获取我的书架"""
    bookshelf = BookShelf.objects.filter(user=request.user)
    serializer = BookShelfSerializer(bookshelf, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_reading_view(request):
    """获取我的阅读进度"""
    reading = ReadingProgress.objects.filter(user=request.user)
    serializer = ReadingProgressSerializer(reading, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_comments_view(request):
    """获取我的评论"""
    comments = Comment.objects.filter(user=request.user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
