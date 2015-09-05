# -*- coding: utf8 -*-

from django.contrib import admin
import os
from blog.models import *


# Register your models here.

# 自定义后台显示
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # list_display = ()  文章列表显示
    list_display = ('title', 'desc', 'click_count')

    # 在列表显示当中，可以修改
    list_editable = ('click_count',)

    # 是否可以链接到文章对象
    list_display_links = ('title',)

    # 定义显示的列, 点进文章后显示
    # fields = ('title', 'desc', 'click_count')

    # exclude = () 除了这些列，其他都显示

    # fieldsets = () 设置，高级选项和普通选项
    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content', 'user', 'category', 'tag', )
        }),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend',)
        }),
    )

    class Media:
        # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
        js = (
            'js/editor/kindeditor-4.1.7/kindeditor-all.js',
            'js/editor/kindeditor-4.1.7/lang.zh_CN.js',
            'js/editor/kindeditor-4.1.7/config.js',
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'content', 'username', 'pid')
    list_display_links = ('article', 'content', 'pid')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(User)
admin.site.register(Links)
admin.site.register(Ad)
