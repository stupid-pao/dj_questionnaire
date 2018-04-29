from random import choice

from django.shortcuts import render

# Create your views here.

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from .serializers import SmsSerializer, UserRegSerializer
from utils.yunpian import YunPian
from dj_questionnaire.settings import APIKEY
from .models import VerifyCode


User = get_user_model()

class CoustomBackend(ModelBackend):
    """
    自定义用户token认证
     """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = "1234567890"
        randome_str = []
        for i in range(4):
            randome_str.append(choice(seeds))

        return ''.join(randome_str)

    #重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #自己的逻辑
        #validated_data ： serializer的 属性
        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code = code, mobile=mobile)

        if sms_status["code"] != 0 :
            return Response({
                "mobile":sms_status["msg"]
            }, status.HTTP_400_BAD_REQUEST)

        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            },status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()




