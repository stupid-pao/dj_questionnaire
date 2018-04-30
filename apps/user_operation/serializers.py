# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()     #要加括号实例化
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    """
    直接利用Meta 生成表 发生的情况=> 1。列出了多有用户，而不是当前的登陆用户。2，列出了所有尚平，而不是我们要添加的商品

    如果不止只获得一个goods的id呢 想拿到更多关于goods的信息呢 => 1. modle 里设置联合主键。2.validators 写到meta类里作用于所有字段
    二者选其一都行
    """
    #拿到当前的用户  属于validates中的一个  =>fields 加一个id字段 方便以后删除
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        fields = ("user", "goods", "id")
