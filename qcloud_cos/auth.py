# -*- coding: utf-8 -*-

import time
import random
import hmac, hashlib
import binascii
import base64
from urlparse import urlparse
from qcloud_cos import conf

class Auth(object):

    def __init__(self, secret_id, secret_key):
        self.AUTH_URL_FORMAT_ERROR = -1
        self.AUTH_SECRET_ID_KEY_ERROR = -2

        self._secret_id,self._secret_key = secret_id,secret_key

    def get_info_from_url(self, url):
        app_info = conf.get_app_info()
        end_point = app_info['end_point']
        info = urlparse(url)
        end_point_info = urlparse(end_point)
        if (info.hostname == urlparse(conf.API_COS_END_POINT).hostname) :
            if info.path :
                parts = info.path.split('/')
                if len(parts) >= 5:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    bucket = parts[4]
                    fileid = ''
                    for i in range(3, len(parts)) :
                        fileid += '/' + parts[i]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'bucket':bucket, 'fileid':fileid}
                else:
                    return {}
            else:
                return {}
        else :
            return {}

    def app_sign(self, bucket, fileid, expired):
        app_info = conf.get_app_info()
        if not self._secret_id or not self._secret_key or not app_info['appid']:
            return self.AUTH_SECRET_ID_KEY_ERROR

        now = int(time.time())
        rdm = random.randint(0, 999999999)
        plain_text = 'a=' + app_info['appid'] + '&k=' + self._secret_id + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm) + '&f=' + fileid + '&b=' + bucket 
        bin = hmac.new(self._secret_key, plain_text, hashlib.sha1)
        s = bin.hexdigest()
        s = binascii.unhexlify(s)
        s = s + plain_text
        signature = base64.b64encode(s).rstrip()    #生成签名
        return signature

    def sign_once(self, bucket, fileid):
        return self.app_sign(bucket, fileid, 0)

    def sign_more(self, bucket, expired):
        return self.app_sign(bucket, '', expired)
