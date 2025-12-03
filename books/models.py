from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """书籍分类"""
    name = models.CharField('分类名称', max_length=50, unique=True)
    slug = models.SlugField('URL标识', max_length=50, unique=True)
    description = models.TextField('描述', blank=True)
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """书籍模型"""
    title = models.CharField('书名', max_length=200)
    author = models.CharField('作者', max_length=100)
    rating = models.FloatField('评分', default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    reviews = models.IntegerField('评价数', default=0)
    genre = models.CharField('类型', max_length=50)
    heat = models.IntegerField('热度', default=0)
    reading = models.CharField('阅读人数', max_length=20, default='0')
    cover = models.URLField('封面图片', max_length=500)
    description = models.TextField('简介')
    is_premium = models.BooleanField('会员专享', default=False)
    publisher = models.CharField('出版社', max_length=100, blank=True)
    publish_date = models.DateField('出版日期', null=True, blank=True)
    pages = models.IntegerField('页数', default=0)
    isbn = models.CharField('ISBN', max_length=20, blank=True)
    categories = models.ManyToManyField(Category, related_name='books', blank=True, verbose_name='分类')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = '书籍'
        ordering = ['-heat', '-rating']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """评论模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name='书籍')
    content = models.TextField('评论内容')
    rating = models.IntegerField('评分', default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    likes = models.IntegerField('点赞数', default=0)
    dislikes = models.IntegerField('点踩数', default=0)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} 对 {self.book.title} 的评论'


class BookShelf(models.Model):
    """用户书架"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookshelf', verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='in_shelves', verbose_name='书籍')
    added_at = models.DateTimeField('添加时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '书架'
        verbose_name_plural = '书架'
        unique_together = ['user', 'book']
        ordering = ['-added_at']
    
    def __str__(self):
        return f'{self.user.username} 的书架 - {self.book.title}'


class ReadingProgress(models.Model):
    """阅读进度"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_progress', verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_records', verbose_name='书籍')
    progress = models.IntegerField('进度', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '阅读进度'
        verbose_name_plural = '阅读进度'
        unique_together = ['user', 'book']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f'{self.user.username} 阅读 {self.book.title} - {self.progress}%'
