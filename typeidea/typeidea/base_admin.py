from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.  自动补充各Model的owner字段
    2.  过滤queryset，只显示当前用户的数据
    """
    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
