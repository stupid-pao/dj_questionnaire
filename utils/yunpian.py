# -*- coding: utf-8 -*-
import json

import  requests

class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey":self.api_key,
            "mobile":mobile,
            "text":"跟模版字段一致， 然后用{}".format(code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        # print(re_dict)
        return re_dict

if __name__ == '__main__':
    yun_pian = YunPian("")
    yun_pian.send_sms("2017", "1855958955")


