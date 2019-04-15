from django.contrib import admin

from .models import Comment

from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
