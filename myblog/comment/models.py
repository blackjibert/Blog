from django.db import models
from django.contrib.auth.models import User
from blog.models import ArticlePosts
#这里一定要继承models.Model,否则无法迁移
class Comment(models.Model):
    article = models.ForeignKey(
        ArticlePosts,
        on_delete=models.CASCADE,
        #related_name是什么意思?
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('created_time',)
    def __str__(self):
        return self.body[:20]