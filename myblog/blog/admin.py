from django.contrib import admin

# Register your models here.
from .models import ArticlePosts
from .models import ArticleColumn
admin.site.register(ArticlePosts)
#注册文章栏目
admin.site.register(ArticleColumn)