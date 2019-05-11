import xadmin

from django.contrib import admin

from django.shortcuts import reverse
from django.utils.html import format_html

from typeidea.base_adminx import BaseOwnerAdmin
from xadmin.layout import Row, Fieldset, Container

from .admin_forms import PostAdminForm
from .models import Post, Category, Tag


class PostInline:  # admin.TabularInline
    """ 对于需要在一个页面内完成两个关联模型编辑编辑的需求，inline admin非常合适 """
    form_layout = (
        Container(
            Row('title', 'desc', 'owner'),
        )
    )
    extra = 2
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav')
    inlines = (PostInline,)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # TODO 新增/编辑文章时候 分类、标签只显示当前用户的
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator', 'pv', 'uv'
    ]

    form = PostAdminForm

    list_display_links = []
    list_filter = ['category']  # 这里不是定义的filter类，是字段名

    search_fields = ['title', 'category__name']

    actions_on_top = True
    # actions_on_bottom = True
    # filter_horizontal = ('tag', )
    # filter_vertical = ('tag', )
    # save_on_top = True
    # fields = (
    #     'category',
    #     'title',
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content',
            'content_ck',
            'content_md'
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('xadmin:blog_post_change', args=(obj.id,))
            self.model_admin_url('change', obj.id)
        )

    operator.short_description = '操作'

