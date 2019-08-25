from django.db import models
#导入内建的User模型
from django.contrib.auth.models import User
#timezone用于处理时间相关事务
from django.utils import timezone
from django.urls import reverse

#Django-taggit 处理多对多关系的管理器
from taggit.managers import TaggableManager


from ckeditor.fields import RichTextField
class ArticleColumn(models.Model):
    """
    文章分类的Model
    """
    #栏目的标题
    title = models.CharField(max_length=100, blank=True)
    #创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePosts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=20)
    # 增加文章栏目的"一对多"外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article',
    )
    #文章标签
    tags = TaggableManager(blank=True)

    title = models.CharField(max_length=128)
    body = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)
    # tags = models.CharField(max_length=20)
    total_views = models.PositiveIntegerField(default=0)

    #内部类Meta中的ordering 根据字段定义了数据的排列顺序
    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        #通过reverse()方法返回文章详情页面的url，实现了路由重定向。
        return reverse('blog:article_detail', args=[self.id])