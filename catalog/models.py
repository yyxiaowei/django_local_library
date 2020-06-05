import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from datetime import date

# 书籍类别信息
class Genre(models.Model):
    name = models.CharField(
        max_length=200, 
        # help_text 表单中帮助用户的文本标签
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        return self.name
# 作者
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # blank为模型字段 如果blank=True 那么表单属性 require = false 否则为true
    date_of_birth = models.DateField(null=True, blank=True)
    # Died 表单中label的字段名称
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    
    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Book(models.Model):
    title = models.CharField(max_length=200)
    # SET_NULL 如果作者没被选择允许设置为Null值
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # 摘要
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    # 标签
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManManyToManyField 多对多 一本书有多种类型，一个类型也可以有许多本书
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # 返回模型详细记录的url
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    # 创建admin管理中Bookd页面的Genre字段
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    # 主键
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True) 
    # 这本书的印记(具体版本)
    imprint = models.CharField(max_length=200)
    # 书籍预期在借用或维护后可用
    due_back = models.DateField(null=True, blank=True)
    # 借用者
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # 状态
    LOAN_STATUS = (
        ('m', 'Maintenance'), # 维护
        ('o', 'On loan'), # 借出
        ('a', 'Available'), # 可用
        ('r', 'Reserved'), # 已预留
    )
    # choices 模型字段 表单字段widget会被设置为select
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    class Meta:
        ordering = ["due_back"]
        # 添加权限
        permissions = (("can_mark_returned", "Set book as returned"),) 
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)

