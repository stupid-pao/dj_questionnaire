from random import choice

from django.shortcuts import render

# Create your views here.

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
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


class UserViewSet(CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    #登陆验证
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    # 这样吧用户注册也给关了  要动态的去设置权限
    # permission_classes = (permissions.IsAuthenticated, )

    #为了注册成功就吧token给返回回去
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


    # RetrieveModelMixin 才有这个方法  目的： 让他知道这是那个用户登陆了
    # 重载了这个方法就意味着，url  ： users/ 后面的数字id 是什么都无所谓了，都会返回当前user
    def get_object(self):
        return self.request.user


    def get_permissions(self):
        #只有viewset才有这个action
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()] # 这个是必须带括号的
        elif self.action == "create":
            return []
        return []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

