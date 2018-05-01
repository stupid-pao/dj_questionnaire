# -*- coding: utf-8 -*-


from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart
from goods.serializers import GoodsSerializer

class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()  #一定要写括号实例化，外键关系，不写many默认false 这里 many=False
    class Meta:
        model = ShoppingCart
        fields = "__all__"


# 继承Serializer的原因 是 购物车添加同一个商品应该加1，ModelSerializer联合主键 在creat时会报错
# 相比于继承ModelSerializer 的弊端： creat ，update 全要自己写
class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        "min_value":"商品数量不呢个小雨一",
                                        "required":"选择数量"
                                    })
    # 通过查文档 擦到的这个外键的写法
    #这个拿到的是一个id
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())  #因为是Serializer， 不是ModelSerializer 所以要指定queryset


    #validated_data => 调用过 上面serializer之后的数据（验证过的数据）
    #initial_data => 直接拿没处理过的数据
    def create(self, validated_data):
        user = self.context["request"].user    #serializer 想获取到user 要这样， 在view里就直接self.request.user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance

