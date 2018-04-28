from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins, generics

from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# 最重要的view
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from .models import Goods
from .filters import GoodsFilter


# 定制 分页
class GooodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    # 指定要多少 p 指明当前页码 ， 指定page_size 可以指定一页显示 多少个
    page_query_param = "p"
    max_page_size = 100


class GoodsListView(APIView):
    def get(self, request, format=None):
        goods = Goods.objects.filter()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)

    def post(self, request, format=None):
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodListView2(mixins.ListModelMixin, generics.GenericAPIView):
    '''
    列表相关的 mixin

    '''
    # 这个queryset和serializer_class都 为 GenericAPIView 里的定义好的名
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

    # get 方法要有 ListModelMixin的特点
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GoodListView3(generics.ListAPIView):
    '''
        加上分页=> 分页配置写到settings REST_FRAMWORK字段离去
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 加上自定义分页
    pagination_class = GooodsPagination  # 用这个 settiong 哪里page 要取消


class GoodsListViewSet_importent(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    这种方式要去url 里 重写as_view方法来 设置 get。post绑定方法
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GooodsPagination


class GoodsListViewSet_fillter(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    过滤  =>  基本方式， 太复杂 看下面用 fillter的实现方式
    '''
    # queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GooodsPagination

    def get_queryset(self):
        queryset = Goods.objects.all()
        price_min = self.request.query_params.get('price_min', 0)
        if price_min:
            queryset = queryset.filter(shop_price_gt=int(price_min))
        return queryset


class GoodsListViewSet_fillter2(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    '''
    利用 django-filter 需要进一步配置 查看drf的filter文档接口

    分页 ， 过滤 ， 搜索， 排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GooodsPagination
    authentication_classes = (TokenAuthentication, ) #自己验证Token

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    # 这种过滤是必须完全与输入匹配才能得到结果的 ，那如何模糊搜索呢？？  去django_fillter官网 看文档 => 新建一个filters。py文件
    filter_class = GoodsFilter
    # 增加搜索功能filter_baxkends 加上 rest_framework import 进来的 filters   数据量大用es搜索引擎
    search_fields = ('name', 'goods_brief')
    # 排序
    ordering_filds = ('sold_name')
