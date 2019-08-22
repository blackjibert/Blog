from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.http import HttpResponse

from .models import ArticlePosts
import markdown
from .forms import ArticlePostForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

#引入Q对象
from django.db.models import Q


#引入分页模块
from django.core.paginator import Paginator
from comment.models import Comment
#文章列表
def article_list(request):

    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            article_list = ArticlePosts.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePosts.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        #将search参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePosts.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePosts.objects.all()

    #每页显示10篇
    paginator = Paginator(article_list, 10)
    #获取url中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    #把order也传递进context,将search也传递进context.(传递这两个参数是为了a的href,可以看一下list.html)
    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'blog/list.html', context)

#文章详情页
def article_detail(request, id):
    #取出响应的文章
    article = ArticlePosts.objects.get(id=id)

    #浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
         extensions=[
             # 包含 缩写、表格等常用扩展
             'markdown.extensions.extra',
             # 语法高亮扩展
             'markdown.extensions.codehilite',
             #目录
             'markdown.extensions.toc',
         ])
    #用convert()方法将正文渲染为html页面
    article.body = md.convert(article.body)
    #需要传递给末班的额对象

    #取出文章评论
    comments = Comment.objects.filter(article=id)
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'blog/detail.html', context)

#写文章视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    #判断用户是否提交数据
    if request.method == 'POST':
        #将提交的数据复制到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            #保留数据,但是不提交到数据库中
            new_article = article_post_form.save(commit=False)
            #指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)

            #将新文章报窜到数据库中
            new_article.save()
            return redirect('blog:article_list')
        else:
            return HttpResponse('表单内容有误,请重新填写')
    #如果用户请求获取数据
    else:
        #创建表单类实例
        article_post_form = ArticlePostForm()
        #赋值上下文
        context = {'article_post_form': article_post_form}
        return render(request, 'blog/create.html', context)


# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePosts.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("blog:article_list")

#更新文章
def article_update(request, id):
    # 判断用户是否提交数据
    article = ArticlePosts.objects.get(id=id)
    if request.method == 'POST':
        # 将提交的数据赋值
        article_post_form =ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            #保存新写入的文章
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.tags = request.POST['tags']
            # 将修改后的文章保存到数据库中
            article.save()
            #完成后返回修改的页面.需要传入问斩的id
            return redirect('blog:article_detail', id=id)
        #如果数据不合法,则返回
        else:
            return HttpResponse('表单内容有误,请重新填写')
    # 如果用户GET请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文,将article文章对象也传递进来
        context = {'article': article, 'article_post_form': article_post_form}
        #将响应返回到模板
        return render(request, 'blog/update.html', context)