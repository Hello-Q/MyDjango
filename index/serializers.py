from rest_framework import serializers
from .models import Product, Type
# 定义Serializer 类
# 设置下拉内容
type_id = Type.objects.values('id').all()
TYPE_CHOICES = [item['id'] for item in type_id]


class MySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    weight = serializers.CharField(required=True, allow_blank=False, max_length=100)
    size = serializers.CharField(required=True, allow_blank=False, max_length=100)
    type = serializers.ChoiceField(choices=TYPE_CHOICES, default=1)

    # 重写create，将API数据更新到数据表
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    # 重写update，将api更新的数据更新到表
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.weight = validated_data.get('weight', instance.weight)
