# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from blog.models import *
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from blog.forms import *
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
import logging


logger = logging.getLogger('blog.views')




# Create your views here.




# 分页代码
def get_page(request, article_list, number=10):
    paninator = Paginator(article_list, number)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paninator.page(page)

    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paninator.page(1)

    return article_list


def index(request):
    try:


        # 最新的文章数据,并分页
        article_list = get_page(request, Article.objects.all(), number=10)
    except Exception as e:
        logger.error(e)

    return render_to_response('base.html', locals(), context_instance=RequestContext(request))
    # return render_to_response('base.html', context_instance=RequestContext(request, processors=[global_setting]))
    # return render(request, 'index.html', locals())

def archive(request):
    # 文章归档
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        article_list = get_page(request, Article.objects.filter(date_publish__icontains=year+'-'+month), number=10)
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html', locals())


def article(request):
    # 文章显示
    try:

        id = request.GET.get('id', None)

        # 文章内容
        try:
            article = Article.objects.get(pk=id)

            # 文章浏览+1
            article.click_count += 1
            article.save()
        except Article.DoesNotExist as e:
            logger.error(e)
            return render(request, 'failure.html', {'reason': '没有想应的文章'})
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id
                                   } if request.user.is_authenticated() else {'article': id})

        # 评论信息, 设置父级评论和子级评论
        comments =Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            # 设置子评论, 数据库中先有父评论，才有子评论
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])

                if comment.pid == item:
                    item.children_comment.append(comment)
                    break

            # 没有子评论，则为父评论
            if comment.pid is None:
                comment_list.append(comment)

    except Exception as e:
        logger.error(e)


    print("")
    return render(request, 'article.html', locals())

def category(request):
    # 分类
    try:
        category_id = request.GET.get('category_id')
        try:
            category = Tag.objects.get(pk=category_id)
            article_list = get_page(request, category.article_set.all(), number=10)

        except Tag.DoesNotExist as e:
            logger.error(e)
            return render(request, 'failure.html', {'reason': '没有想对应的分类'})


    except Exception as e:
        logger.error(e)

    return render(request, 'category.html', locals())




def do_reg(request):
    # 注册
    try:
        # GET提交，转去注册页面，POST提交，则进行注册
        if 'POST' == request.method:
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():

                # cleaned_data: 提交的数据自己，已经进行了python数据转换
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),)

                user.save()

                # 指定默认的登录验证方式
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                # 登陆返回
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()

    except Exception as e:
        logger.error(e)
    return  render(request, 'reg.html', locals())


def do_login(request):
    # 登陆
    try:
        if 'POST' == request.method:

            login_form = LoginForm(request.POST)

            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
            else:
                user = None

            if user is not None and user.is_active:
                print("do_login2")
                # 指定默认的登录验证方式, 该认证方式，只支持username认证
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                # 登陆返回
                login(request, user)
                print("login success")
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': '登录验证失败'})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)

    return render(request, 'login.html', locals())


def do_logout(request):
    # 注销
    try:
        logout(request)
    except Exception as e:
        logger.error(e)

    return redirect(request.META['HTTP_REFERER'])



def comment_post(request):
   #  提交评论
   try:
       comment_form = CommentForm(request.POST)
       if comment_form.is_valid():
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)

            comment.save()
       else:
           return render(request, 'failure.html', {'reason': comment_form.errors})
   except Exception as e:
       logger.error(e)

   return redirect(request.META['HTTP_REFERER'])

def tag(request):
    try:
        tag_id = request.GET.get('tag_id')
        try:
            tag = Tag.objects.get(pk=tag_id)
            article_list = get_page(request, tag.article_set.all(), number=10)

        except Tag.DoesNotExist as e:
            logger.error(e)
            return render(request, 'failure.html', {'reason': '没有想对应的标签'})


    except Exception as e:
        logger.error(e)

    return render(request, 'tag.html', locals())

