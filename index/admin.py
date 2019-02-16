from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_title = 'MyDjango后台管理'
admin.site.site_header = 'MyDjango'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 设置管理列表显示的字段
    list_display = ['id', 'name', 'weight', 'size', 'type']
    # 设置可搜索的字段并在Admin后台数据生成搜索框,有外键使用下划线连接
    search_fields = ['id', 'name', 'type__type_name']
    # 设置过滤器,后台数据右侧生成导航栏,外键用双下划线连接
    list_filter = ['name', 'type__type_name']
    # 设置排序方式
    ordering = ['id']
    # 设置添加数据可添加字段,外间不用下划线
    fields = ['name', 'weight', 'size', 'type']
    # 设置只读字段
    readonly_fields = ['name']
    # 设置自定义字段
    list_display.append('colored_type')

    # 根据用户是不是管理员设置name是否可写
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ['name']
        return self.readonly_fields

    # 根据用户是不是管理员设置数据列表显示条数
    def get_queryset(self, request):
        qs = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(id__lt=6)

    # 新增数据时设置外键可选值
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'type':
            if not request.user.is_superuser:
                kwargs["quryset"] = Type.objects.filter(id__lt=4)
        return super(admin.ModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # 修改保存方法
    def save_model(self, request, obj, form, change):
        if change:
            # 获取用户名
            user = request.user
            # 使用模型获取数据,pk代表具有主键属性的字段
            name = self.model.objects.get(pk=obj.pk).name
            # 使用表单获取数据
            weight = form .cleaned_data['weight']
            # 写入日志文件
            f = open('/home/zhangyanqing/MyDjango_log.txt', 'a')
            f.write('产品：'+str(name)+'，被用户：'+str(user)+'修改'+'\r\n')
            f.close()
        else:
            pass
        super(ProductAdmin, self).save_model(request, obj, form, change)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']
