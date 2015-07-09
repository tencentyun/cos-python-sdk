# -*- coding: utf-8 -*-

import time
import tencentyun_cos

appid = 'xxxx'
secret_id = 'xxxxx'
secret_key = 'xxxxx'

cos = tencentyun_cos.Cos(appid,secret_id,secret_key)
#cos = tencentyun_cos.Cos()

obj = cos.delete('bucket01', '123/a.mp4')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.upload('test.mp4','bucket01','123/a.mp4')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.createFolder('bucket01', 'python2', 1)
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.listFiles('bucket01', '123/')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.update('bucket01', '123/')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.stat('bucket01', '123/a.mp4')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.delete('bucket01', 'abc/a.mp4')
print obj, obj['message']
print '----------------------------------------------------------------------'

obj = cos.upload_slice('test3.mp4', 'bucket01', 'python/f.mp4', '', 2*1024*1024)
print obj, obj['message']
