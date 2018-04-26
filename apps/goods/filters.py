#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  django_filters
from .models import Goods

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr= 'gte')  #gte => less than or equal to
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    #对string 进行模糊查询
    name = django_filters.CharFilter(name='shop_price', lookup_expr='icontains')  # contains=>包括关键字 i=>忽略大小写

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'name']

