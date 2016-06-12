#!/usr/bin/env python
# coding=utf-8

################################################################################
# sdk错误码
################################################################################
class CosErr(object):
    PARAMS_ERROR  = -1 # 参数错误
    NETWORK_ERROR = -2 # 网络错误
    SERVER_ERROR  = -3 # server端返回错误
    UNKNOWN_ERROR = -4 # 未知错误
        
    @classmethod
    def get_err_msg(cls, errcode, err_info):
        err_msg = {}
        err_msg[u'code'] = errcode
        err_msg[u'message'] = err_info
        return err_msg
