# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta


from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dj_questionnaire.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    """
    为什么不用ModelSerializer 与数据库关联？
    因为只用到了手机号， 数据库字段便多了
    自己写逻辑
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        #手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        #验证手机验证码  用正则
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("号码重复")

        #验证频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距上次发未超过一分钟")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    usermodel 没code 字段，要自定义Serializer => 通过一些技巧也能享受到ModelSerializer的便利
    write_only 参数使这个code 不会被序列化，防止 删除了code后 ，Meta的field（）方法有code字段报错
    """
    code = serializers.CharField(write_only=True, required=True, max_length=4, min_length=4,
                                 error_messages={
                                     "required":"请输入验证码",
                                     "max_length":"验证码最多4位"
                                 },
                                 help_text="验证码")

    username = serializers.CharField(required=True, allow_blank= False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])


    def validate_code(self, code):
        # self.initial_data  在ModelSerializer中，可以获取到前端传递的值
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by()
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError(" 验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    # 这个验证作用于所有字段之上
    # attrs 将所有类似 validate_** 的方法返回的值 做成一个字典 => 上面的validate_code 返回的东西我们不需要，所以从attrs里删除
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]  # 加一个mobile ，处理用户不填手机号的 情况
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile")  # mobile 字段设计为可以为空，只需要用户填个用户名就好



