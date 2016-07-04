#!/usr/bin/env python
# coding=utf-8

"""the request type in tencent qcloud cos"""

from cos_params_check import ParamCheck
import collections

################################################################################
# BaseRequest基本类型的请求                                                    #
################################################################################
class BaseRequest(object):
    # bucket_name: bucket的名称
    # cos_path: cos的绝对路径, 即从bucket下的根/开始
    def __init__(self, bucket_name, cos_path):
        self._bucket_name  = bucket_name.strip()
        self._cos_path     = cos_path.strip()
        self._param_check   = ParamCheck()

    # 设置bucket_name
    def set_bucket_name(self, bucket_name=u''):
        self._bucket_name = bucket_name.strip()

    # 获取bucket_name
    def get_bucket_name(self):
        return self._bucket_name

    # 设置cos_path
    def set_cos_path(self, cos_path=u''):
        self._cos_path = cos_path.strip()
    
    # 获取cos_path
    def get_cos_path(self):
        return self._cos_path

    # 获取错误信息
    def get_err_tips(self):
        return self._param_check.get_err_tips()

    # 检查参数是否合法
    def check_params_valid(self):
        if not self._param_check.check_param_unicode('bucket', self._bucket_name):
            return False
        return self._param_check.check_param_unicode('cos_path', self._cos_path)

################################################################################
# CreateFolderRequest  创建目录类型的请求                                      #
################################################################################
class CreateFolderRequest(BaseRequest):
    # bucket_name: bucket的名称
    # cos_path:    cos的绝对路径, 从bucket根/开始
    # biz_attr:    目录的属性
    def __init__(self, bucket_name, cos_path, biz_attr=u''):
        super(CreateFolderRequest, self).__init__(bucket_name, cos_path)
        self._biz_attr = biz_attr

    # 设置biz_attr
    def set_biz_attr(self, biz_attr):
        self._biz_attr = biz_attr

    # 获取biz_attr
    def get_biz_attr(self):
        return self._biz_attr

    # 检查参数是否合法
    def check_params_valid(self):
        if not super(CreateFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_param_unicode('biz_attr', 
                self._biz_attr):
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=False):
            return False
        return self._param_check.check_not_cos_root(self._cos_path)

################################################################################
# UploadFileRequest  单文件上传请求                                            #
################################################################################
class UploadFileRequest(BaseRequest):
    # bucket_name:            bucket的名称
    # cos_path:               cos的绝对路径(目的路径), 从bucket根/开始
    # local_path:             上传的本地文件路径(源路径)
    # biz_attr:               文件的属性
    # insert_only:            是否覆盖写, 0覆盖, 1不覆盖,返回错误

    def __init__(self, bucket_name, cos_path, local_path, biz_attr=u'',
            insert_only=1):
        super(UploadFileRequest, self).__init__(bucket_name, cos_path)
        self._local_path          = local_path.strip()
        self._biz_attr            = biz_attr
        self._insert_only         = insert_only

    # 设置local_path
    def set_local_path(self, local_path):
        self._local_path = local_path.strip()

    # 获取local_path
    def get_local_path(self):
        return self._local_path

    # 设置biz_attr
    def set_biz_attr(self, biz_attr):
        self._biz_attr = biz_attr

    # 获取biz_attr
    def get_biz_attr(self):
        return self._biz_attr

    # 设置insert_only，0表示如果文件存在, 则覆盖
    def set_insert_only(self, insert_only):
        self._insert_only = insert_only

    # 获取insert_only
    def get_insert_only(self):
        return self._insert_only

    # 检查参数是否有效 
    def check_params_valid(self):
        if not super(UploadFileRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=True):
            return False
        if not self._param_check.check_param_unicode('biz_attr',
                self._biz_attr):
            return False
        if not self._param_check.check_param_unicode('local_path',
                self._local_path):
            return False
        if not self._param_check.check_local_file_valid(self._local_path):
            return False
        if not self._param_check.check_param_int('insert_only', 
                self._insert_only):
            return False
        return self._param_check.check_insert_only(self._insert_only)

################################################################################
# UploadSliceFileRequest  分片文件上传请求                                     #
################################################################################
class UploadSliceFileRequest(UploadFileRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的绝对路径(目的路径), 从bucket根/开始
    # local_path:   上传的本地文件路径(源路径)
    # biz_attr:     文件的属性
    # slice_size:   分片大小(字节, 默认1MB)
    def __init__(self, bucket_name, cos_path, local_path, slice_size=1024*1024,
            biz_attr=u''):
        super(UploadSliceFileRequest, self).__init__(bucket_name, cos_path, local_path,
                biz_attr)
        self._slice_size = slice_size

    # 设置分片大小
    def set_slice_size(self, slice_size):
        self._slice_size = slice_size

    # 获取分片大小
    def get_slice_size(self):
        return self._slice_size

    # 检查参数是否有效 
    def check_params_valid(self):
        if not super(UploadSliceFileRequest, self).check_params_valid():
            return False
        return self._param_check.check_slice_size(self._slice_size)

################################################################################
# UpdateFolderRequest 更新目录请求                                             #
################################################################################
class UpdateFolderRequest(BaseRequest):
    # biz_attr:               目录属性 
    def __init__(self, bucket_name, cos_path, biz_attr=u''):
        super(UpdateFolderRequest, self).__init__(bucket_name, cos_path)
        self._biz_attr = biz_attr

    # 设置biz_attr
    def set_biz_attr(self, biz_attr):
        self._biz_attr = biz_attr

    # 获取biz_attr
    def get_biz_attr(self):
        return self._biz_attr

    # 检查参数是否有效 
    def check_params_valid(self):
        if not super(UpdateFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=False):
            return False
        if not self._param_check.check_not_cos_root(self._cos_path):
            return False
        return self._param_check.check_param_unicode('biz_attr',
                self._biz_attr)

################################################################################
# UpdateFileRequest 更新文件请求                                               #
################################################################################
class UpdateFileRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的绝对路径, 从bucket根/开始
    # biz_attr:     要更新的文件的属性
    # authority:              文件权限:
    #                         eInvalid(继承bucket), 
    #                         eWRPrivate(私有读写),
    #                         eWPrivateRPublic(私有写, 公有读)
    # customer_header:        用户自定义的HTTP请求头,包括以下成员
    # cache_control:          文件的缓存机制,参见HTTP的Cache-Control
    # content_type:           文件的MIME信息,参见HTTP的Content-Type
    # content_disposition:    MIME协议的扩展,参见HTTP的Content-Disposition
    # content_language:       文件的语言, 参见HTTP的Content-Language
    # _x_cos_meta_dict:       用户自定义的属性, key是以x-cos-meta-开头,value为属性值
    def __init__(self, bucket_name, cos_path):
        super(UpdateFileRequest, self).__init__(bucket_name, cos_path)
        self._flag                = 0
        self._biz_attr            = u''
        self._custom_headers      = {}
        self._authority           = u''
        self._cache_control       = u''
        self._content_type        = u''
        self._content_disposition = u''
        self._content_language    = u''
        self._x_cos_meta_dict     = {}

    # 获取flag
    def get_flag(self):
        return self._flag

    # 设置biz_attr
    def set_biz_attr(self, biz_attr):
        self._biz_attr = biz_attr
        self._flag |= 0x01

    # 获取biz_attr
    def get_biz_attr(self):
        return self._biz_attr

    # 设置authority, 合法取值如下所示
    # eInvalid(继承bucket), 
    # eWRPrivate(私有读写),
    # eWPrivateRPublic(私有写, 公有读)
    def set_authority(self, authority):
        self._authority = authority
        self._flag |= 0x80

    # 获取authority
    def get_authority(self):
        return self._authority

    # 设置缓存机制Cache-Control
    def set_cache_control(self, cache_control):
        self._cache_control = cache_control
        self._flag |= 0x40
        self._custom_headers[u'Cache-Control'] = cache_control

    # 设置Content-Type
    def set_content_type(self, content_type):
        self._content_type = content_type
        self._flag |= 0x40
        self._custom_headers['Content-Type'] = content_type

    # 设置Content-Disposition
    def set_content_disposition(self, content_disposition):
        self._content_disposition = content_disposition
        self._flag |= 0x40
        self._custom_headers['Content-Disposition'] = content_disposition

    # 设置Content-Language
    def set_content_language(self, content_language):
        self._content_language = content_language
        self._flag |= 0x40
        self._custom_headers['Content-Language'] = content_language

    # 设置自定义的x-cos-meta, key以x-cos-meta-开头
    # 例如自定义key为u'x-cos-meta-len', value为u'1024'
    def set_x_cos_meta(self, key, value):
        self._flag |= 0x40
        self._x_cos_meta_dict[key] = value
        self._custom_headers[key] = value

    # convert a dict's keys & values from `unicode` to `str`
    def _convert_dict(self, data):
         if isinstance(data, basestring):
             return str(data)
         elif isinstance(data, collections.Mapping):
             return dict(map(self._convert_dict, data.iteritems()))
         elif isinstance(data, collections.Iterable):
             return type(data)(map(self._convert_dict, data))
         else:
             return data

    # 获取自定义的HTTP头
    def get_custom_headers(self):
        return self._convert_dict(self._custom_headers)

    # 检查参数是否合法
    def check_params_valid(self):
        if not super(UpdateFileRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=True):
            return False
        if not self._param_check.check_update_flag(self._flag):
            return False
        if not self._param_check.check_param_unicode('biz_attr', 
                self._biz_attr):
            return False
        if not self._param_check.check_param_unicode('authority', 
                self._authority):
            return False
        if not self._param_check.check_file_authority(self._authority):
            return False
        if not self._param_check.check_param_unicode('cache_control', 
                self._cache_control):
            return False
        if not self._param_check.check_param_unicode('content_type',
                self._content_type):
            return False
        if not self._param_check.check_param_unicode('content_disposition',
                self._content_disposition):
            return False
        if not self._param_check.check_param_unicode('content_language',
                self._content_language):
            return False
        return self._param_check.check_x_cos_meta_dict(self._x_cos_meta_dict)

################################################################################
# MoveFileRequest 移动文件请求                                                 #
################################################################################
class MoveFileRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # src_cos_path: 要移动的文件源路径
    # dst_cos_path: 要移动到文件目的地路径
    # to_over_write:   是否覆盖, 0(默认): 不覆盖, 1: 覆盖
    def __init__(self, bucket_name, src_cos_path, dst_cos_path, to_over_write = 0):
        super(MoveFileRequest, self).__init__(bucket_name, src_cos_path)
        self._src_cos_path  = src_cos_path
        self._dst_cos_path  = dst_cos_path
        self._to_over_write = to_over_write

    # 设置src_cos_path
    def set_src_cos_path(self, src_cos_path):
        self._src_cos_path = src_cos_path

    # 获取src cos path
    def get_src_cos_path(self):
        return self._src_cos_path

    # 设置dst_cos_path
    def set_src_cos_path(self, dst_cos_path):
        self._dst_cos_path = dst_cos_path

    # 获取dst_cos_path
    def get_dst_cos_path(self):
        return self._dst_cos_path

    # 设置over_write标志
    def set_over_write(self, to_over_write):
        self._to_over_write = to_over_write

    # 获取over_write标志
    def get_over_write(self):
        return self._to_over_write

    # 检查参数是否合法
    def check_params_valid(self):
        if not super(MoveFileRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._src_cos_path, 
                is_file_path=True):
            return False
        if not self._param_check.check_param_unicode('dst_cos_path', 
            self._dst_cos_path):
            return False
        if not self._param_check.check_cos_path_valid(self._dst_cos_path, 
                is_file_path=True):
            return False
        if not self._param_check.check_param_int('over_write', 
            self._to_over_write):
            return False
        return self._param_check.check_move_over_write(self._to_over_write)

################################################################################
# StatRequest 获取文件属性请求                                                 #
################################################################################
class StatFileRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的文件路径, 从bucket根/开始, 不以/结束
    def __init__(self, bucket_name, cos_path):
        super(StatFileRequest, self).__init__(bucket_name, cos_path)

    # 检查参数是否合法
    def check_params_valid(self):
        if not super(StatFileRequest, self).check_params_valid():
            return False
        return self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=True)

################################################################################
# StatRequest 获取目录属性请求                                                 #
################################################################################
class StatFolderRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的目录路径, 从bucket根/开始, 以/结束
    def __init__(self, bucket_name, cos_path):
        super(StatFolderRequest, self).__init__(bucket_name, cos_path)

    # 检查参数是否合法
    def check_params_valid(self):
        if not super(StatFolderRequest, self).check_params_valid():
            return False
        return self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=False)

################################################################################
# DelFileRequest 删除文件请求                                                  #
################################################################################
class DelFileRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的文件路径, 从bucket根/开始, 不以/结束
    def __init__(self, bucket_name, cos_path):
        super(DelFileRequest, self).__init__(bucket_name, cos_path)

    # 检查参数是否合法
    def check_params_valid(self):
        if not super(DelFileRequest, self).check_params_valid():
            return False
        return self._param_check.check_cos_path_valid(self._cos_path,
                is_file_path=True)

################################################################################
# DelFolderRequest 删除目录请求                                                #
################################################################################
class DelFolderRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的目录路径, 从bucket根/开始, 以/结束
    def __init__(self, bucket_name, cos_path):
        super(DelFolderRequest, self).__init__(bucket_name, cos_path)

    # 检查参数合法
    def check_params_valid(self):
        if not super(DelFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path, 
                is_file_path=False):
            return False
        return self._param_check.check_not_cos_root(self._cos_path)

################################################################################
# ListFolderRequest 获取目录列表的请求                                         #
################################################################################
class ListFolderRequest(BaseRequest):
    # bucket_name:  bucket的名称
    # cos_path:     cos的绝对路径, 从bucket根/开始
    # num:          搜索数量
    # pattern:      搜索的类型, 合法取值eListBoth, eListDirOnly, eListFileOnly
    # prefix:       搜索前缀
    # context:      搜索上下文
    # order:        搜索顺序(0 正序, 1逆序)
    def __init__(self, bucket_name, cos_path, num=199, 
            pattern = u'eListBoth', prefix=u'', context=u'', order=0):
        super(ListFolderRequest, self).__init__(bucket_name, cos_path)
        self._num     = num
        self._pattern = pattern
        self._prefix  = prefix
        self._context = context
        self._order   = order

    # 设置List数量
    def set_num(self, num):
        self._num = num

    # 获取List数量
    def get_num(self):
        return self._num

    # 获取List类型
    def set_pattern(self, pattern):
        self._pattern = pattern

    # 获取List类型
    def get_pattern(self):
        return self._pattern

    # 设置前缀
    def set_prefix(self, prefix):
        self._preifx = prefix
        
    # 获取前缀
    def get_prefix(self):
        return self._prefix

    # 设置搜索上下文
    def set_context(self, context):
        self._context = context
    
    # 获取搜索上下文
    def get_context(self):
        return self._context

    # 设置搜索顺序
    def set_order(self, order=0):
        self._order = order

    # 获取搜索顺序
    def get_order(self):
        return self._order

    # 检查参数是否有效 
    def check_params_valid(self):
        if not super(ListFolderRequest, self).check_params_valid():
            return False
        if not self._param_check.check_cos_path_valid(self._cos_path,
                is_file_path=False):
            return False
        if not self._param_check.check_param_unicode('prefix', self._prefix):
            return False
        if not self._param_check.check_param_unicode('context', self._context):
            return False
        if not self._param_check.check_list_order(self._order):
            return False
        return self._param_check.check_list_pattern(self._pattern)
