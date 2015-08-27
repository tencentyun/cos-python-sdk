# -*- coding: utf-8 -*-
import pkg_resources
import platform

API_COS_END_POINT = 'http://web.file.myqcloud.com/files/v1/'
APPID = '您的APPID'
SECRET_ID = '您的SECRETID'
SECRET_KEY = '您的SECRETKEY'

cos_config = {
    'end_point':API_COS_END_POINT,
    'appid':APPID,
    'secret_id':SECRET_ID,
    'secret_key':SECRET_KEY,
}

def get_app_info():
	return cos_config

def set_app_info(appid=None,secret_id=None,secret_key=None):
    if appid:
        cos_config['appid'] = appid
    if secret_id:
        cos_config['secret_id'] = secret_id
    if secret_key:
        cos_config['secret_key'] = secret_key

def get_ua():
    try:
        version = pkg_resources.require("qcloud_cos")[0].version
    except Exception as e:
        version = ''
    return 'Qcloud-Cos-PYTHON/'+version+' ('+platform.platform()+')'
