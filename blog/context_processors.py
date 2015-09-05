#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ljian'

from django.conf import settings
from blog.models import *
from django.db.models import  Count

def global_setting(request):
    # 分类数据
    category_list = Category.objects.all()

    # 文章归档数据
    archive_list = Article.objects.distinct_date()

    # # 广告数据
    # ad_list = Ad.objects.all()

    # 标签云数据
    tag_list = Tag.objects.all()

    # 友情链接
    link_list = Links.objects.all()

    # 评论排行
    # annotate ---> GROUP BY
    comment_count_list = Comment.objects.values('article').annotate(commnet_count=Count('article'))\
        .order_by('-commnet_count')

    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:6]

    # 浏览排行
    browse_article_list = Article.objects.all().order_by('-click_count')[:6]


    # 网站基本信息配置
    SITE_NAME = 'Ljian1992博客'
    SITE_DESC = '架构之路, 全栈人生'
    COPYRIGHT_INFO ='Ljian1992博客'

    # 关注我
    # WEIBO_SINA = 'http://weibo.com/'
    # PRO_RSS = 'http://baidu.com'
    # PRO_EMAIL = '1345@qq.com'


    return locals()


