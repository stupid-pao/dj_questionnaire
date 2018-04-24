#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.base import View

from goods.models import Goods
from django.views.generic import ListView


class GoodsListView(View):
    def get(self, request):
        # json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = goods.name
        #     json_dict["category"] = goods.category.name
        #     json_dict["market_price"] = goods.market_price
        #     json_dict["add_time"] = good.add_time
        #     json_list.append(json_dict)
        #
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        from django.http import JsonResponse
        return JsonResponse(json_data, safe=False)

