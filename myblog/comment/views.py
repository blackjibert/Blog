from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import ArticlePosts
from .forms import CommentForm
from django.http import HttpResponse
from .models import Comment
from django.urls import reverse
#发表评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePosts, id=article_id)

    if request.method == 'POST':
        #创建一个文章实例
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            #当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法。因此接下来马上修改article的模型
            return redirect(article)
        else:
            return HttpResponse('表单内容有误,请重新输入.')
    else:
        return HttpResponse('发表评论仅仅接受POST请求.')

#删除评论
@login_required(login_url='/userprofile/login/')
def deletet_comment(request, id):
    #获取要删除评论的id
    comment = Comment.objects.get(id=id)
    # 获取评论对应文章的id,这是正向查询
    article_id = comment.article.id
    #获取发表评论的用户id
    author_id = comment.author.id
    #验证登录用户,和发表评论用户是否相同
    if author_id == request.user.id:
        comment.delete()
        return redirect('blog:article_detail', article_id)
    else:
        return HttpResponse('你没有删除评论的权限.')
