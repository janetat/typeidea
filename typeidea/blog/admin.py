from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html

from typeidea.custom_site import custom_site
from .admin_forms import PostAdminForm
from .admin_filters import CategoryOwnerFilter
from .models import Post, Category, Tag


class PostInline(admin.StackedInline):  # admin.TabularInline
    """ 对于需要在一个页面内完成两个关联模型编辑编辑的需求，inline admin非常合适 """
    fields = ('title', 'desc')
    extra = 2
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav')
    inlines = (PostInline,)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    # TODO 新增/编辑文章时候 分类、标签只显示当前用户的
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]

    form = PostAdminForm

    list_display_links = []
    list_filter = [CategoryOwnerFilter]

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

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                'title',
                'category',
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content'
            ),
        }),
        ('额外信息', {
            'fields': ('tag',),
            'classes': ('collapse',),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)
