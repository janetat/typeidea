from django.http import HttpResponse
from django.shortcuts import render

from .models import Post, Category, Tag


# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    post_list = []
    if category_id:
        post_list = Post.objects.filter(category=category_id, status=Post.STATUS_NORMAL, owner=request.user)
    elif tag_id:
        post_list = Post.objects.filter(tag=tag_id, status=Post.STATUS_NORMAL, owner=request.user)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL, owner=request.user)

    # TODO 模板中的post.category，是外键查询，每一条记录的请求都需要一次数据库访问来获取关联外键的问题。
    # 例如列表页要展示10条数据，每一个关联外键查询都会产生一次数据库请求，即1+N问题。

    return render(request, 'blog/list.html', context={'post_list': post_list})


def post_detail(request, post_id=None):
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            post = None
    else:
        post = None

    return render(request, 'blog/detail.html', context={'post': post})
