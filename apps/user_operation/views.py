from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer
from utils import permissions



class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve：
        判断某个商品是否以收藏
    create：
        收藏商品

    """
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)
    # serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"  #外键生成默认会加_id


    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取留言
    Create：
        创建留言
    delete：
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user = self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    ModelViewSet = 整删改查全包
    """
    pass



