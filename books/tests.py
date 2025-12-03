from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Category, Comment, BookShelf, ReadingProgress


class BookAPITestCase(TestCase):
    """书籍API测试"""
    
    def setUp(self):
        """测试初始化"""
        self.client = APIClient()
        # 创建测试书籍
        self.book = Book.objects.create(
            title='测试书籍',
            author='测试作者',
            rating=4.5,
            reviews=100,
            genre='测试',
            heat=50,
            reading='1000',
            cover='http://example.com/cover.jpg',
            description='这是一本测试书籍',
            is_premium=False,
            publisher='测试出版社',
            pages=200,
            isbn='1234567890'
        )
    
    def test_get_books_list(self):
        """测试获取书籍列表"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_get_book_detail(self):
        """测试获取书籍详情"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '测试书籍')


class UserAPITestCase(TestCase):
    """用户API测试"""
    
    def setUp(self):
        """测试初始化"""
        self.client = APIClient()
    
    def test_user_register(self):
        """测试用户注册"""
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post('/api/register', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    def test_user_login(self):
        """测试用户登录"""
        # 先创建用户
        User.objects.create_user(username='testuser', password='testpass123')
        
        # 登录
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class BookShelfTestCase(TestCase):
    """书架测试"""
    
    def setUp(self):
        """测试初始化"""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.book = Book.objects.create(
            title='测试书籍',
            author='测试作者',
            rating=4.5,
            reviews=100,
            genre='测试',
            heat=50,
            reading='1000',
            cover='http://example.com/cover.jpg',
            description='这是一本测试书籍',
            is_premium=False,
            publisher='测试出版社',
            pages=200,
            isbn='1234567890'
        )
        # 认证
        self.client.force_authenticate(user=self.user)
    
    def test_add_to_bookshelf(self):
        """测试添加到书架"""
        data = {'book_id': self.book.id}
        response = self.client.post('/api/bookshelf/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_bookshelf(self):
        """测试获取书架"""
        # 先添加书籍
        BookShelf.objects.create(user=self.user, book=self.book)
        
        # 获取书架
        response = self.client.get('/api/bookshelf/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
