#!/usr/bin/env python
# coding=utf-8
import os

################################################################################
# BaseRequest基本类型的请求                                                    #
################################################################################
class ParamCheck(object):
    def __init__(self):
        self._err_tips=u''

    # 获取错误信息
    def get_err_tips(self):
        return self._err_tips

    # 检查参数是否是unicode
    # param_name 参数名
    # param_value 参数值
    def check_param_unicode(self, param_name, param_value):
        if param_value == None:
            self._err_tips = param_name + ' is None!'
            return False
        if not isinstance(param_value, unicode):
            self._err_tips = param_name + ' is not unicode!'
            return False
        return True

    # 检查参数是否是int
    # param_name 参数名
    # param_value 参数值
    def check_param_int(self, param_name, param_value):
        if param_value == None:
            self._err_tips = param_name + ' is None!'
            return False
        if not isinstance(param_value, int):
            self._err_tips = param_name + ' is not int!'
            return False
        return True

    # 检查cos_path是否合法, 必须以/开始
    # 文件路径则不能以/结束, 目录路径必须以/结束
    # 路径合法返回True, 否则返回False
    def check_cos_path_valid(self, cos_path, is_file_path):
        if cos_path[0] != u'/':
            self._err_tips = 'cos path must start with /'
            return False

        last_letter = cos_path[len(cos_path) - 1]
        if is_file_path and last_letter == u'/':
            self._err_tips = 'for file operation, cos_path must not end with /'
            return False
        elif not is_file_path and last_letter != u'/':
            self._err_tips = 'for folder operation, cos_path must end with /'
            return False
        else:
            return True

    # 检查不是cos的跟路基
    # 不等进行根路径操作的有 1 update 2 cretate 3 delete
    def check_not_cos_root(self, cos_path):
        if cos_path == u'/':
            self._err_tips = 'bucket operation is not supported by sdk,'
            ' please use cos console: https://console.qcloud.com/cos'
            return False
        else:
            return True

    # 检查本地文件有效(存在并且可读)
    def check_local_file_valid(self, local_path):
        if not os.path.exists(local_path):
            self._err_tips = 'local_file %s not exist!' % local_path
            return False
        if not os.path.isfile(local_path):
            self._err_tips = 'local_file %s is not regular file!' % local_path
            return False
        if not os.access(local_path, os.R_OK):
            self._err_tips = 'local_file %s is not readable!' % local_path
            return False
        return True

    # 检查分片大小有效
    def check_slice_size(self, slice_size):
        min_size = 512 * 1024           # 512KB
        max_size = 20 * 1024 * 1024     # 20MB
        if slice_size >= min_size and slice_size <= max_size:
            return True
        else:
            self._err_tips = 'slice_size is invalid, only accept [%d, %d]' \
                    % (min_size, max_size)
            return False

    # 检查文件上传的insert_only参数
    def check_insert_only(self, insert_only):
        if insert_only != 1 and insert_only != 0:
            self._err_tips = 'insert_only only support 0 and 1'
            return False
        else:
            return True

    # 检查move的over write标志
    def check_move_over_write(self, to_over_write):
        if to_over_write != 1 and to_over_write != 0:
            self._err_tips = 'to_over_write only support 0 and 1'
            return False
        else:
            return True

    # 检查文件的authority属性
    # 合法的取值只有eInvalid, eWRPrivate, eWPrivateRPublic和空值
    def check_file_authority(self, authority):
        if  authority != u'' and \
            authority != u'eInvalid' and \
            authority != u'eWRPrivate' and \
            authority != u'eWPrivateRPublic':
                self._err_tips = 'file authority valid value is:' 
                'eInvalid, eWRPrivate, eWPrivateRPublic'
                return False
        else:
            return True

    # 检查x_cos_meta_dict, key和value都必须是UTF8编码
    def check_x_cos_meta_dict(self, x_cos_meta_dict):
        prefix_len = len('x-cos-meta-')
        for key in x_cos_meta_dict.keys():
            if not self.check_param_unicode('x-cos-meta-key', key):
                return False
            if not self.check_param_unicode('x-cos-meta-value', 
                    x_cos_meta_dict[key]):
                return False
            if key[0:prefix_len] != u'x-cos-meta-':
                self._err_tips = 'x-cos-meta key must start with x-cos-meta-'
                return False
            if len(key) == prefix_len:
                self._err_tips = 'x-cos-meta key must not just be x-cos-meta-'
                return False
            if (len(x_cos_meta_dict[key]) == 0):
                self._err_tips = 'x-cos-meta value must not be empty'
                return False
        return True

    # 检查更新文件的flag
    def check_update_flag(self, flag):
        if flag == 0:
            self._err_tips = 'no any attribute to be updated!'
            return False
        else:
            return True

    # 检查list folder的order
    # 合法取值0(正序), 1(逆序)
    def check_list_order(self, list_order):
        if list_order != 0 and list_order != 1:
            self._err_tips = 'list order is invalid, please use 0(positive) or 1(reverse)!'
            return False
        else:
            return True

    # 检查list folder的pattern
    # 合法取值eListBoth, eListDirOnly, eListFileOnly
    def check_list_pattern(self, list_pattern):
        if list_pattern != u'eListBoth' and \
            list_pattern != u'eListDirOnly' and \
            list_pattern != u'eListFileOnly':
                self._err_tips = 'list pattern is invalid,'
                ' please use eListBoth or eListDirOnly or eListFileOnly'
                return False
        else:
            return True
