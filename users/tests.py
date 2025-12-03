from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTestCase(TestCase):
    """用户资料测试"""
    
    def setUp(self):
        """测试初始化"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_user_profile_created(self):
        """测试用户资料自动创建"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_user_profile_fields(self):
        """测试用户资料字段"""
        profile = self.user.profile
        self.assertFalse(profile.is_vip)
        self.assertEqual(profile.bio, '')
        self.assertEqual(profile.gender, '')
