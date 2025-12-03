from django.urls import path
from .views import (
    login_view, register_view, logout_view,
    profile_view, update_profile_view, user_stats_view,
    my_shelf_view, my_reading_view, my_comments_view
)

urlpatterns = [
    # 认证相关
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    
    # 用户资料
    path('profile', profile_view, name='profile'),
    path('profile/update', update_profile_view, name='update-profile'),
    
    # 用户统计
    path('user/stats', user_stats_view, name='user-stats'),
    path('user/shelf', my_shelf_view, name='my-shelf'),
    path('user/reading', my_reading_view, name='my-reading'),
    path('user/comments', my_comments_view, name='my-comments'),
]
