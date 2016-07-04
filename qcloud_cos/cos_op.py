#!/usr/bin/env python
# coding=utf-8

import os
import time
import json
import hashlib
import urllib
import cos_auth
import cos_config
from cos_err     import CosErr
from cos_request import UploadFileRequest
from cos_request import UploadSliceFileRequest
from cos_request import UpdateFileRequest
from cos_request import DelFileRequest
from cos_request import StatFileRequest
from cos_request import MoveFileRequest
from cos_request import CreateFolderRequest
from cos_request import UpdateFolderRequest
from cos_request import StatFolderRequest
from cos_request import DelFolderRequest
from cos_request import ListFolderRequest

################################################################################
# BaseOp基本操作类型                                                           #
################################################################################
class BaseOp(object):
    # cred: 用户的身份信息
    # config: cos_config配置类
    # http_session: http 会话
    # expired_period: 签名过期时间, 单位秒
    def __init__(self, cred, config, http_session):
        self._cred           = cred
        self._config         = config
        self._http_session   = http_session
        self._expired_period = self._config.get_sign_expired()

    # 设置用户的身份信息
    def set_cred(self, cred):
        self._cred = cred

    # 设置config
    def set_config(self, config):
        self._config = config
        self._expired_period = self._config.get_sign_expired()

    # 生成url
    def _build_url(self, bucket, cos_path):
        bucket    = bucket.encode('utf8')
        end_point = self._config.get_end_point().rstrip('/').encode('utf8')
        appid     = self._cred.get_appid()
        cos_path  = urllib.quote(cos_path.encode('utf8'), '~/')
        url       = '%s/%s/%s%s' % (end_point, appid, bucket, cos_path)
        return url

    # 发送http请求
    def send_request(self, method, bucket, cos_path, **args):
        url = self._build_url(bucket, cos_path)
        http_resp = {}
        try:
            if method == 'POST':
                http_resp = self._http_session.post(url, verify=False, **args)
            else:
                http_resp = self._http_session.get(url, verify=False, **args)

            status_code = http_resp.status_code
            if (status_code == 200 or status_code == 400):
                return http_resp.json()
            else:
                err_detail = 'url:%s, status_code:%d' % (url, status_code)
                return CosErr.get_err_msg(CosErr.NETWORK_ERROR, err_detail)
        except Exception as e:
            err_detail = 'url:%s, exception:%s' % (url, repr(e))
            return CosErr.get_err_msg(CosErr.SERVER_ERROR, err_detail)

    # 检查用户输入参数, 检查通过返回None, 否则返回一个代表错误原因的dict
    def _check_params(self, request):
        if not self._cred.check_params_valid():
            return CosErr.get_err_msg(CosErr.PARAMS_ERROR, self._cred.get_err_tips())
        if not request.check_params_valid():
            return CosErr.get_err_msg(CosErr.PARAMS_ERROR, request.get_err_tips())
        return None

    # 删除文件或者目录, is_file_op为True表示是文件操作
    def del_base(self, request):
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        sign     = auth.sign_once(bucket, cos_path)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['Content-Type']  = 'application/json'
        http_header['User-Agent']    = self._config.get_user_agent()

        http_body       = {}
        http_body['op'] = 'delete'

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                data=json.dumps(http_body), timeout=timeout)

    # 获取文件和目录的属性
    def stat_base(self, request):
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, cos_path, expired)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['User-Agent']    = self._config.get_user_agent()

        http_body       = {}
        http_body['op'] = 'stat'

        timeout = self._config.get_timeout()
        return self.send_request('GET', bucket, cos_path, headers=http_header,
                params=http_body, timeout=timeout)

################################################################################
# FileOp 文件相关操作                                                          #
################################################################################
class FileOp(BaseOp):
    # cred: 用户的身份信息
    # config: cos_config配置类
    # http_session: http 会话
    def __init__(self, cred, config, http_session):
        BaseOp.__init__(self, cred, config, http_session)
        # 单文件上传的最大上限是20MB
        self.max_single_file = 20 * 1024 * 1024

    # 获取content的sha1
    def _sha1_content(self, content):
        sha1_obj = hashlib.sha1()
        sha1_obj.update(content)
        return sha1_obj.hexdigest()

    # 获取文件的sha1
    def _sha1_file(self, file_path):
        sha1_obj = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while True:
                block_data = f.read(4096)
                if not block_data:
                    break
                sha1_obj.update(block_data)
        return sha1_obj.hexdigest()

    # 更新文件
    def update_file(self, request):
        assert isinstance(request, UpdateFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        sign     = auth.sign_once(bucket, cos_path)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['Content-Type']  = 'application/json'
        http_header['User-Agent']    = self._config.get_user_agent()

        http_body             = {}
        http_body['op']       = 'update'

        update_flag = request.get_flag()
        http_body['flag'] = str(update_flag)
        if (update_flag & 0x01 != 0):
            http_body['biz_attr'] = request.get_biz_attr()
        if (update_flag & 0x80 != 0):
            http_body['authority'] = request.get_authority()
        if (update_flag & 0x40 != 0):
            http_body['custom_headers'] = request.get_custom_headers()

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                data=json.dumps(http_body), timeout=timeout)

    # 删除文件
    def del_file(self, request):
        assert isinstance(request, DelFileRequest)
        return self.del_base(request)

    # 获取文件的属性
    def stat_file(self, request):
        assert isinstance(request, StatFileRequest)
        return self.stat_base(request)

    # 移动文件
    def move_file(self, request):
        assert isinstance(request, MoveFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, cos_path, expired)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['Content-Type']  = 'application/json'
        http_header['User-Agent']    = self._config.get_user_agent()

        http_body                  = {}
        http_body['op']            = 'move'
        http_body['dest_fileid']   = request.get_dst_cos_path()
        http_body['to_over_write'] = request.get_over_write()

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                data=json.dumps(http_body), timeout=timeout)

    # 上传文件, 根据用户的文件大小,选择单文件上传和分片上传策略
    def upload_file(self, request):
        assert isinstance(request, UploadFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        local_path = request.get_local_path()
        file_size  = os.path.getsize(local_path)

        suit_single_file_zie = 8 * 1024 * 1024
        if (file_size < suit_single_file_zie):
            return self.upload_single_file(request)
        else:
            bucket     = request.get_bucket_name()
            cos_path   = request.get_cos_path()
            local_path = request.get_local_path()
            slice_size = 1024 * 1024
            biz_attr   = request.get_biz_attr()
            upload_slice_request = UploadSliceFileRequest(bucket, cos_path,
                    local_path, slice_size, biz_attr)
            upload_slice_request.set_insert_only(request.get_insert_only())
            return self.upload_slice_file(upload_slice_request)

    # 单文件上传
    def upload_single_file(self, request):
        assert isinstance(request, UploadFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        local_path = request.get_local_path()
        file_size = os.path.getsize(local_path)
        # 判断文件是否超过单文件最大上限, 如果超过则返回错误
        # 并提示用户使用别的接口
        if file_size > self.max_single_file:
            return CosErr.get_err_msg(CosErr.NETWORK_ERROR,
                    'file is to big, please use upload_file interface')

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, cos_path, expired)

        http_header = {}
        http_header['Authorization'] = sign
        http_header['User-Agent'] = self._config.get_user_agent()

        with open(local_path, 'rb') as f:
            file_content = f.read()

        http_body                = {}
        http_body['op']          = 'upload'
        http_body['filecontent'] = file_content
        http_body['sha']         = self._sha1_content(file_content)
        http_body['biz_attr']    = request.get_biz_attr()
        http_body['insertOnly']  = str(request.get_insert_only())

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                files=http_body, timeout=timeout)

    # 分片文件上传(串行)
    def upload_slice_file(self, request):
        assert isinstance(request, UploadSliceFileRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        control_ret = self._upload_slice_control(request)
        # 表示控制分片已经产生错误信息
        if control_ret[u'code'] != 0:
            return control_ret
        # 命中秒传
        if control_ret[u'data'].has_key(u'access_url'):
            return control_ret

        bucket     = request.get_bucket_name()
        cos_path   = request.get_cos_path()
        local_path = request.get_local_path()
        file_size  = os.path.getsize(local_path)
        slice_size = control_ret[u'data'][u'slice_size']
        offset     = control_ret[u'data'][u'offset']
        session    = control_ret[u'data'][u'session']

        with open(local_path, 'rb') as local_file:
            local_file.seek(offset)
            while offset < file_size:
                file_content = local_file.read(slice_size)
                retry_count = 0
                max_retry = 3
                # 如果分片数据上传发生错误, 则进行重试,默认3次
                while retry_count < max_retry:
                    data_ret = self._upload_slice_data(bucket, cos_path,
                            file_content, session, offset)
                    if data_ret[u'code'] == 0:
                        if data_ret[u'data'].has_key(u'access_url'):
                            return data_ret
                        else:
                            break
                    else:
                        retry_count += 1

                if retry_count == max_retry:
                    return data_ret
                else:
                    offset += slice_size
        return data_ret

    # 串行分片第一步, 上传控制分片
    def _upload_slice_control(self, request):
        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, cos_path, expired)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['User-Agent']    = self._config.get_user_agent()

        local_path  = request.get_local_path()
        sha1_digest = self._sha1_file(local_path)
        file_size   = os.path.getsize(local_path)
        slice_size  = request.get_slice_size()
        biz_atrr    = request.get_biz_attr()

        http_body               = {}
        http_body['op']         = 'upload_slice'
        http_body['sha']        = sha1_digest
        http_body['filesize']   = str(file_size)
        http_body['slice_size'] = str(slice_size)
        http_body['biz_attr']   = request.get_biz_attr()
        http_body['insertOnly'] = str(request.get_insert_only())

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                files=http_body, timeout=timeout)

    # 串行分片第二步, 上传数据分片
    def _upload_slice_data(self, bucket, cos_path, file_content, session, offset):
        auth     = cos_auth.Auth(self._cred)
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, cos_path, expired)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['User-Agent']    = self._config.get_user_agent()

        http_body                = {}
        http_body['op']          = 'upload_slice'
        http_body['filecontent'] = file_content
        http_body['session']     = session
        http_body['offset']      = str(offset)

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                files=http_body, timeout=timeout)

################################################################################
# FolderOp 目录相关操作                                                        #
################################################################################
class FolderOp(BaseOp):
    def __init__(self, cred, config, http_session):
        BaseOp.__init__(self, cred, config, http_session)

    # 更新目录
    def update_folder(self, request):
        assert isinstance(request, UpdateFolderRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        sign     = auth.sign_once(bucket, cos_path)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['Content-Type']  = 'application/json'
        http_header['User-Agent']    = self._config.get_user_agent()

        http_body             = {}
        http_body['op']       = 'update'
        http_body['biz_attr'] = request.get_biz_attr()

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                data=json.dumps(http_body), timeout=timeout)

    # 删除目录
    def del_folder(self, request):
        assert isinstance(request, DelFolderRequest)
        return self.del_base(request)

    # 获取目录属性
    def stat_folder(self, request):
        assert isinstance(request, StatFolderRequest)
        return self.stat_base(request)

    # 创建目录
    def create_folder(self, request):
        assert isinstance(request, CreateFolderRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        cos_path = request.get_cos_path()
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, cos_path, expired)

        http_header = {}
        http_header['Authorization'] = sign
        http_header['Content-Type'] = 'application/json'
        http_header['User-Agent'] = self._config.get_user_agent()

        http_body             = {}
        http_body['op']       = 'create'
        http_body['biz_attr'] = request.get_biz_attr()

        timeout = self._config.get_timeout()
        return self.send_request('POST', bucket, cos_path, headers=http_header,
                data=json.dumps(http_body), timeout=timeout)

    # list目录
    def list_folder(self, request):
        assert isinstance(request, ListFolderRequest)
        check_params_ret = self._check_params(request)
        if check_params_ret != None:
            return check_params_ret

        http_body            = {}
        http_body['op']      = 'list'
        http_body['num']     = request.get_num()
        http_body['pattern'] = request.get_pattern()
        http_body['order']   = request.get_order()
        http_body['context'] = request.get_context()
        http_body['prefix']  = request.get_prefix()

        auth     = cos_auth.Auth(self._cred)
        bucket   = request.get_bucket_name()
        list_path = request.get_cos_path() + request.get_prefix()
        expired  = int(time.time()) + self._expired_period
        sign     = auth.sign_more(bucket, list_path, expired)

        http_header                  = {}
        http_header['Authorization'] = sign
        http_header['User-Agent']    = self._config.get_user_agent()

        timeout = self._config.get_timeout()
        return self.send_request('GET', bucket, list_path, headers=http_header,
                params=http_body, timeout=timeout)
