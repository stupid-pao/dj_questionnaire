from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer
from .models import ShoppingCart

class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = "goods_id"

    # queryset = ShoppingCart.objects.all()
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

