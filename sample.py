# -*- coding: utf-8 -*-

import time
import qcloud_cos as qcloud

appid = 'xxxx'
secret_id = 'xxxxx'
secret_key = 'xxxxxx'

cos = qcloud.Cos(appid,secret_id,secret_key)
#cos = qcloud.Cos()

obj = cos.deleteFile('bucket01', 'abc')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.upload('test','bucket01','v.mp4', '0666')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.createFolder('bucket01', '123/')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.list('bucket01', '/123/', 3, 'eListFileOnly')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.updateFile('bucket01', '/v.mp4', '0666')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.deleteFile('bucket01', '/v.mp4')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.statFile('bucket01', 'v.mp4')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.upload_slice('test3.mp4', 'bucket01', 'v.mp4', '', 2*1024*1024)
print obj, obj['message']
