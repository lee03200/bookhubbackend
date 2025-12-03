from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """用户资料扩展"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    avatar = models.URLField('头像', max_length=500, blank=True, default='https://picsum.photos/id/64/200/200')
    bio = models.TextField('个人简介', blank=True, max_length=500)
    gender = models.CharField('性别', max_length=10, blank=True, choices=[
        ('male', '男'),
        ('female', '女'),
        ('other', '保密')
    ])
    interests = models.JSONField('阅读兴趣', default=list, blank=True)
    is_vip = models.BooleanField('是否VIP', default=False)
    vip_expire_date = models.DateField('VIP到期日期', null=True, blank=True)
    member_since = models.DateField('加入日期', auto_now_add=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f'{self.user.username} 的资料'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """用户创建时自动创建用户资料"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时同时保存用户资料"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
