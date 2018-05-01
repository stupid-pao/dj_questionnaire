# -*- coding: utf-8 -*-
import time
from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
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


class OrderGoodsSerializer(serializers.ModelSerializer):
    # order 是model的 order的related_name 的名字
    order = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):

    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trad_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generrate_order_sn(self):
        from random import Random
        rand_sn = Random()
        order_sn = "{}{}{}".format(time.strftime("%Y%m%d%H%M%S"), self.context["request"].user.id,
                                   rand_sn.randint(10,99))
        return order_sn


    def validate(self, attrs):
        attrs["order_sn"] = self.generrate_order_sn()
        return attrs


    class Meta:
        model = OrderInfo
        fields = "__all__"