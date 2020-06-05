from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):
    
    @classmethod
    # 用于类级别设置，在测试运行开始的时侯，会调用一次。您可以使用它来创建在任何测试方法中，都不会修改或更改的对象
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')
    # 在每个测试函数之前被调用，以设置可能被测试修改的任何对象（每个测试函数，都将获得这些对象的 “新” 版本）
    def setUp(self):
        self.author = Author.objects.get(id=1)
    
    def test_first_name_label(self):
        # verbose_name 字段标签名称
        field_label = self.author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')
    
    def test_date_of_death_label(self):
        field_label = self.author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'Died')

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        expected_object_name = '%s, %s' % (self.author.last_name, self.author.first_name)
        self.assertEquals(expected_object_name,str(self.author))

    def test_get_absolute_url(self):
        self.assertEquals(self.author.get_absolute_url(),'/catalog/author/1')