from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import ArticlePosts
from .forms import CommentForm
from django.http import HttpResponse
from .models import Comment
from django.urls import reverse
#发表评论
@login_required(login_url='/userprofile/login/')
# 新增参数 parent_comment_id
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePosts, id=article_id)

    if request.method == 'POST':
        #创建一个文章实例
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user


            #二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                #若回复层超过二级,则转换为二级
                new_comment.parent_id = parent_comment.get_root().id

                #被回复人
                new_comment.reply_to = parent_comment.author
                new_comment.save()
                return HttpResponse('200 OK')


            new_comment.save()
            #当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法。因此接下来马上修改article的模型
            return redirect(article)
        else:
            return HttpResponse('表单内容有误,请重新输入.')

    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
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
