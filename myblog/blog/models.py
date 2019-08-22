from django.db import models
#导入内建的User模型
from django.contrib.auth.models import User
#timezone用于处理时间相关事务
from django.utils import timezone
from django.urls import reverse
class ArticlePosts(models.Model):
    #文章作者
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=20)
    #文章标题
    title = models.CharField(max_length=128)
    #文章正文
    body = models.TextField()
    #文章创建时间
    created_time = models.DateTimeField(default=timezone.now)
    #文章更新时间
    updated_time = models.DateTimeField(auto_now=True)
    #文章标签
    tags = models.CharField(max_length=20)
    #文章浏览量
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