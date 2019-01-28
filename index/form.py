from django import forms
from .models import *
from django.core.exceptions import ValidationError


def weight_validate(value):
    if not str(value).isdigit():
        raise ValidationError('请输入正确的数量')


class ProductForm(forms.ModelForm):
    # 添加模型外字段
    productID = forms.CharField(max_length=20, label='产品序号')

    # 模型与表单设置
    class Meta:
        # 绑定模型
        model = Product
        fields = '__all__'
        exclude = []
        # 设置label标签
        labels = {
            'name': '产品名称',
            'weight': '重量',
            'size': '尺寸',
            'type': '产品类型',
        }
        widgets = {'name': forms.widgets.TextInput(attrs={'class': 'c1'})}
        # 定义字段类型
        field_classes = {'name': forms.CharField}
        help_texts = {'name': ''}
        error_messages = {
            '__all__': {'required': '请输入内容',
                        'invalid': '请检查输入内容'},
            'weight': {'required': '请输入重量数值',
                       'invalid': '请检查数值是否正确'}
        }

    def clean_weight(self):
        data = self.cleaned_data['weight']
        return data+'g'
