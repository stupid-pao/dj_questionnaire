from django.shortcuts import render

# Create your views here.

from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Goods


class GoodsListView(APIView):
    def get(self, request, format=None):
        goods = Goods.objects.filter()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
