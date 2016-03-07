# qcloud_cos-python
python sdk for [腾讯云COS服务]

## 安装

### 使用pip
pip install qcloud_cos

### 下载源码
从github下载源码装入到您的程序中，并加载qcloud_cos包。(依赖requests扩展包，ver >= 2.4.1)

### 修改配置
修改qcloud_cos/conf.py内的appid等信息为您的配置

### 举例
```python

#下面接口中的 path 变量 可以为'/dir/test.mp4' 也可以为 'dir/test.mp4'，sdk会自动补齐

import qcloud_cos as qcloud

cos = qcloud.Cos()	#使用conf.py中配置的信息
#cos = qcloud.Cos(appid,secret_id,secret_key)	#自己设置配置信息
obj = cos.upload('test.mp4','bucket','dir/test.mp4')	
#obj = cos.upload_slice('test.mp4','bucket','dir/test.mp4', '', 3*1024*1024)	#分片上传，适用于较大文件
print obj

if obj['code'] == 0 :
    # 查询文件状态
    print cos.statFile('bucket', 'dir/test.mp4')
    
    # 删除文件
    print cos.deleteFile('bucket', 'dir/test.mp4')

#创建目录
obj = cos.createFolder('bucket', '/firstDir/')
if obj['code'] == 0 :
    print cos.upload('test.mp4', 'bucket', '/firstDir/firstfile.mp4')

#获取指定目录下文件列表
print cos.list('bucket', '/firstDir/', 20, 'eListFileOnly')

#获取bucket下文件列表
print cos.list('bucket', '/', 20, 'eListFileOnly')

#获取指定目录下以'abc'开头的文件
print cos.prefixSearch('bucket', '/firstDir/', 'abc', 20, 'eListFileOnly')

#查询文件属性
print cos.statFile('bucket', '/firstDir/firstfile.mp4')

#删除文件
print cos.deleteFile('bucket', '/firstDir/firstfile.mp4')
```
