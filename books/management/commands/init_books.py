from django.core.management.base import BaseCommand
from books.models import Book, Category
from datetime import date


class Command(BaseCommand):
    help = '初始化书籍数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始初始化书籍数据...')
        
        # 创建分类
        categories_data = [
            {'name': '小说', 'slug': 'fiction'},
            {'name': '科技', 'slug': 'technology'},
            {'name': '心理学', 'slug': 'psychology'},
            {'name': '历史', 'slug': 'history'},
            {'name': '文学', 'slug': 'literature'},
            {'name': '科幻', 'slug': 'sci-fi'},
            {'name': '推理', 'slug': 'mystery'},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
        
        self.stdout.write(self.style.SUCCESS(f'已创建 {len(categories_data)} 个分类'))
        
        # 创建书籍数据
        books_data = [
            {
                'title': 'JavaScript高级程序设计',
                'author': '尼古拉斯·泽卡斯',
                'rating': 4.8,
                'reviews': 1243,
                'genre': '科技',
                'heat': 98,
                'reading': '12.3万',
                'cover': 'https://ts1.tc.mm.bing.net/th/id/R-C.65e79b2f99aa01c8d00f99dce25ab47f',
                'description': '一本深入浅出介绍 JavaScript 的经典书籍。',
                'is_premium': False,
                'publisher': '人民邮电出版社',
                'publish_date': date(2012, 10, 1),
                'pages': 756,
                'isbn': '9787115308672',
            },
            {
                'title': '人类简史',
                'author': '尤瓦尔·赫拉利',
                'rating': 4.6,
                'reviews': 2356,
                'genre': '历史',
                'heat': 95,
                'reading': '9.8万',
                'cover': 'https://img.alicdn.com/i2/2543812659/O1CN01AgGsjU1VVrswdhd42_!!2543812659.jpg',
                'description': '从认知革命到超月世界，重新解读人类发展史。',
                'is_premium': True,
                'publisher': '中信出版社',
                'publish_date': date(2014, 11, 1),
                'pages': 452,
                'isbn': '9787508647357',
            },
            {
                'title': '三体',
                'author': '刘慈欣',
                'rating': 4.9,
                'reviews': 5678,
                'genre': '科幻',
                'heat': 99,
                'reading': '15.2万',
                'cover': 'https://p1.ssl.qhimg.com/t0147ec1b07078c0cf8.jpg',
                'description': '地球文明与三体文明的首次接触，开启宇宙社会学的宏大叙事。',
                'is_premium': False,
                'publisher': '重庆出版社',
                'publish_date': date(2008, 1, 1),
                'pages': 302,
                'isbn': '9787536692930',
            },
            {
                'title': '活着',
                'author': '余华',
                'rating': 4.7,
                'reviews': 3456,
                'genre': '文学',
                'heat': 92,
                'reading': '8.9万',
                'cover': 'https://ts2.tc.mm.bing.net/th/id/OIP-C.8Mb1Jm08nNYWyVcoddsZqwHaJ3',
                'description': '一个人在苦难中坚持活下去的故事，感人至深。',
                'is_premium': False,
                'publisher': '作家出版社',
                'publish_date': date(1993, 1, 1),
                'pages': 191,
                'isbn': '9787506310797',
            },
            {
                'title': '解忧杂货店',
                'author': '东野圭吾',
                'rating': 4.8,
                'reviews': 7654,
                'genre': '推理',
                'heat': 91,
                'reading': '11.3万',
                'cover': 'https://ts1.tc.mm.bing.net/th/id/OIP-C.v-_BhEb7l5KWQyHuqOmmngHaHV',
                'description': '通过一店杂货店解开人生中的绳结。',
                'is_premium': False,
                'publisher': '南海出版公司',
                'publish_date': date(2012, 8, 1),
                'pages': 305,
                'isbn': '9787544268967',
            },
            {
                'title': '百年孤独',
                'author': '加西亚·马尔克斯',
                'rating': 4.7,
                'reviews': 4567,
                'genre': '文学',
                'heat': 89,
                'reading': '7.6万',
                'cover': 'https://so1.360tres.com/t017c401645dd63e333.png',
                'description': '布恩迪亚家族七代人在马孔多小镇的兴衰与孤独。',
                'is_premium': True,
                'publisher': '南海出版公司',
                'publish_date': date(2011, 1, 1),
                'pages': 458,
                'isbn': '9787544240900',
            },
            {
                'title': '思考，快与慢',
                'author': '丹尼尔·卡尼曼',
                'rating': 4.8,
                'reviews': 12543,
                'genre': '心理学',
                'heat': 987,
                'reading': '5.6万',
                'cover': 'https://picsum.photos/id/22/300/450',
                'description': '《思考，快与慢》是诺贝尔经济学奖得主丹尼尔·卡尼曼的经典著作。',
                'is_premium': True,
                'publisher': '中信出版社',
                'publish_date': date(2012, 7, 1),
                'pages': 424,
                'isbn': '9787508633558',
            },
        ]
        
        created_count = 0
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'已创建 {created_count} 本书籍'))
        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))
