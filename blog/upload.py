# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os, uuid, json, datetime

__author__ = 'Ljian'

@csrf_exempt
def upload_image(request, dir_name):
    # kindeditor文件上传返回数据格式
    # 成功时
    # {"error" : 0,"url" : "http://www.example.com/path/to/file.ext"}
    # 失败时
    # {"error" : 1, "message" : "错误信息"
    # }
    result = {'error': 1, 'message': '上传错误'}

    # 在kindeditor接图片文件form名称：imgFile
    # FILES：该对象包含了所有的上传文件
    files = request.FILES.get('imgFile', None)

    if files:
        result = image_upload(files, dir_name)

    return HttpResponse(json.dumps(result), content_type='application/json')

# 目录创建
def upload_create_dir(dir_name):
    today = datetime.datetime.today()
    dir_name = dir_name + '/%d/%d' %(today.year, today.month)

    dir_path = os.path.join(settings.MEDIA_ROOT, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_name

# 图片上传
def image_upload(files, dir_name):

    # 判断图片格式是否正确, 允许的图片格式为：'jpg', 'png', 'jpeg', 'gif','bmp'
    allow_suffix = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
    file_suffix = os.path.splitext(files.name)[-1]
    print(file_suffix)
    if file_suffix not in allow_suffix:
        return {'error': 1, 'message': '图片格式不正确'}

    relative_path_file = upload_create_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = str(uuid.uuid1()) + file_suffix
    file_path = os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + '/' + file_name

    # 保存图片
    with open(file_path, 'wb') as f:
        f.write(files.file.read())

    return {'error': 0, 'url': file_url}




