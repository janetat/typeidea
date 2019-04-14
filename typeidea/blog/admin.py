from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html

from .admin_filters import CategoryOwnerFilter
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # TODO 新增 文章时候 分类、标签只显示当前用户的
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]

    search_fields = ['title', 'category__name']

    actions_on_top = True
    # actions_on_bottom = True

    # save_on_top = True
    fields = (
        'category',
        'title',
        'desc',
        'status',
        'content',
        'tag'
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set.filter(owner=request.user)
