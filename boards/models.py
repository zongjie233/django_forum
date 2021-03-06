from django.db import models
import math
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe


# Create your models here.

#板块类
class Board(models.Model): #所有的模型都是django.db.models.Model类的子类，每个类都被转换为数据库表
    name = models.CharField(max_length=30, unique=True) #规定最大长度。以及名字的唯一性
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

#主题类
class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateField(auto_now_add=True) #返回时间
    board = models.ForeignKey(Board, related_name='topics',on_delete=models.CASCADE) #与Board表建立联系，使用related_name 可以让调用变得更加自然;2.0之后需要显性指定on_delete
    starter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


#帖子类
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+',null=True,on_delete=models.CASCADE )#不需要指示关系

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)


    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

