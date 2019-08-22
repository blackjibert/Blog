#引入表单类
from django import forms
from.models import ArticlePosts
#引入文章模型

#写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指明数据模型来源
        model = ArticlePosts
        #定义表单包含的类型
        fields = ('title', 'body', 'tags')
