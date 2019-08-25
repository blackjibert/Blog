from django.db import models
from django.contrib.auth.models import User
from blog.models import ArticlePosts
from ckeditor.fields import RichTextField

from mptt.models import MPTTModel, TreeForeignKey
class Comment(MPTTModel):
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
    # body = models.TextField()
    body = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)
    #必须的
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children'
                            )
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )


    class MPTTMeta:
        order_insertion_by = ['created_time']
    def __str__(self):
        return self.body[:20]