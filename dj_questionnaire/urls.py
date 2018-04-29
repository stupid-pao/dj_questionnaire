"""dj_questionnaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from rest_framework.documentation import include_docs_urls

#静态图， media文件
from django.views.static import serve
from dj_questionnaire.settings import MEDIA_ROOT
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

# from goods.views_base import GoodsListView
from goods.views import GoodsListViewSet_importent, GoodsListViewSet_fillter2
from goods.views import GoodListView3
from users.views import SmsCodeViewset, UserViewSet
from user_operation.views import UserFavViewSet




# 这种最简单 需要在下面urlpatterns 用include 调用 实例router的 urls 方法完成注册
router = DefaultRouter()
router.register(r'goodsrouter', GoodsListViewSet_importent)  #register 配置自动将 get转到list上去
router.register(r'goodsfilter', GoodsListViewSet_fillter2)

router.register(r'codes', SmsCodeViewset, base_name="codes")
router.register(r'users', UserViewSet, base_name="users")
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")

goods_list = GoodsListViewSet_importent.as_view({
    #绑定方式灵活,  但是还有跟简单的 方式配置url  用DefaultRouter
    'get':'list',
})

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # url('xadmin/', xadmin.site.urls),

    url(r'docs/', include_docs_urls(title='b')),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'goods/$', GoodListView3.as_view(), name="goods-list"),
    #用 goods_list 替换
    url(r'goodsviewset/$', goods_list, name="goods-list"),

    #router定义方式
    url(r'^', include(router.urls)),

    url(r'^media/(?P<path>.*)$', serve, {"documentroot":MEDIA_ROOT}),

    # drf 自带的token验证方式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt 自己的方式
    url(r'^login/', obtain_jwt_token),

]
