#!/usr/bin/env python
# coding=utf-8

################################################################################
# CosConfig 有关cos的配置
################################################################################
class CosConfig(object):
    def __init__(self):
        self._end_point    = 'http://web.file.myqcloud.com/files/v1'
        self._user_agent   = 'cos-python-sdk-v3.3'
        self._timeout      = 3 
        self._sign_expired = 300

    # 设置COS的域名地址
    def set_end_point(self, end_point):
        self._end_point = end_point

    # 获取域名地址
    def get_end_point(self):
        return self._end_point

    # 获取HTTP头中的user_agent
    def get_user_agent(self):
        return self._user_agent

    # 设置连接超时, 单位秒
    def set_timeout(self, time_out):
        assert isinstance(time_out, int)
        self._timeout = time_out

    # 获取连接超时，单位秒
    def get_timeout(self):
        return self._timeout

    # 设置签名过期时间, 单位秒
    def set_sign_expired(self, expired):
        assert isinstance(expired, int)
        self._sign_expired = expired

    # 获取签名过期时间, 单位秒
    def get_sign_expired(self):
        return self._sign_expired

    # 打开https
    def enable_https(self):
        self._end_point = 'https://web.file.myqcloud.com/files/v1'
