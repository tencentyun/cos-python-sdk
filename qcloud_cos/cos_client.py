#!/usr/bin/env python
# coding=utf-8

import requests
from cos_cred import CredInfo
from cos_config import CosConfig
from cos_op import FileOp
from cos_op import FolderOp
from cos_request import UploadFileRequest
from cos_request import UploadSliceFileRequest
from cos_request import UpdateFileRequest
from cos_request import UpdateFolderRequest
from cos_request import DelFileRequest
from cos_request import MoveFileRequest
from cos_request import DelFolderRequest
from cos_request import CreateFolderRequest
from cos_request import StatFolderRequest
from cos_request import StatFileRequest
from cos_request import ListFolderRequest
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

################################################################################
# Cos客户端类                                                                  #
################################################################################
class CosClient(object):
    # 设置用户的相关信息
    def __init__(self, appid, secret_id, secret_key):
        self._cred         = CredInfo(appid, secret_id, secret_key)
        self._config       = CosConfig()
        self._http_session = requests.session()
        self._file_op      = FileOp(self._cred, self._config, self._http_session)
        self._folder_op    = FolderOp(self._cred, self._config, self._http_session)

    # 设置config
    def set_config(self, config):
        assert isinstance(config, CosConfig)
        self._config = config
        self._file_op.set_config(config)
        self._folder_op.set_config(config)

    # 获取config
    def get_config(self):
        return self._config

    # 设置用户的身份信息
    def set_cred(self, cred):
        assert isinstance(cred, CredInfo)
        self._cred = cred
        self._file_op.set_cred(cred)
        self._folder_op.set_cred(cred)

    # 获取用户的相关信息
    def get_cred(self):
        return self._cred

    # 上传文件(自动根据文件大小，选择上传策略, 强烈推荐使用)
    # 上传策略: 8MB以下适用单文件上传, 8MB(含)适用分片上传
    def upload_file(self, request):
        assert isinstance(request, UploadFileRequest)
        return self._file_op.upload_file(request)

    # 单文件上传接口, 适用用小文件8MB以下
    # 最大不得超过20MB, 否则会返回参数错误
    def upload_single_file(self, request):
        assert isinstance(request, UploadFileRequest)
        return self._file_op.upload_single_file(request)

    # 分片上传接口, 适用于大文件8MB及以上
    def upload_slice_file(self, request):
        assert isinstance(request, UploadSliceFileRequest)
        return self._file_op.upload_slice_file(request)

    # 删除文件
    def del_file(self, request):
        assert isinstance(request, DelFileRequest)
        return self._file_op.del_file(request)

    # 获取文件属性
    def stat_file(self, request):
        assert isinstance(request, StatFileRequest)
        return self._file_op.stat_file(request)

    # 更新文件属性
    def update_file(self, request):
        assert isinstance(request, UpdateFileRequest)
        return self._file_op.update_file(request)

    # 移动文件
    def move_file(self, request):
        assert isinstance(request, MoveFileRequest)
        return self._file_op.move_file(request)

    # 创建目录
    def create_folder(self, request):
        assert isinstance(request, CreateFolderRequest)
        return self._folder_op.create_folder(request)

    # 删除目录
    def del_folder(self, request):
        assert isinstance(request, DelFolderRequest)
        return self._folder_op.del_folder(request)

    # 获取folder属性请求
    def stat_folder(self, request):
        assert isinstance(request, StatFolderRequest)
        return self._folder_op.stat_folder(request)
    
    # 更新目录属性
    def update_folder(self, request):
        assert isinstance(request, UpdateFolderRequest)
        return self._folder_op.update_folder(request)

    # 获取目录下的文件和目录列表
    def list_folder(self, request):
        assert isinstance(request, ListFolderRequest)
        return self._folder_op.list_folder(request)
