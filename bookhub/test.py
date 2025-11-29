# 示例：检测 Book 模型
def test_book_creation(self):
    book = Book.objects.create(title="Django指南", author="张三")
    self.assertEqual(book.title, "Django指南")
    self.assertTrue(isinstance(book, Book))
def test_book_list_view(self):
    response = self.client.get('/books/')
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Django指南")
def test_only_staff_can_delete_book(self):
    response = self.client.post('/books/1/delete/')
    self.assertEqual(response.status_code, 403)  # 普通用户应被拒绝