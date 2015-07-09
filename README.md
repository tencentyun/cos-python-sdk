# tencentyun_cos-python
python sdk for [腾讯云COS服务]

## 安装

### 使用pip
pip install tencentyun_cos

### 下载源码
从github下载源码装入到您的程序中，并加载tencentyun_cos包

### 修改配置
修改tencentyun_cos/conf.py内的appid等信息为您的配置

### 文件上传
```python
import tencentyun_cos

cos = tencentyun_cos.Cos()	#使用conf.py中配置的信息
#cos = tencentyun_cos.Cos(appid,secret_id,secret_key)	#自己设置配置信息
obj = cos.upload('test.mp4','bucket','dir/test.mp4')
#obj = cos.upload_slice('test.mp4','bucket','dir/test.mp4')		#分片上传，适用于较大文件
print obj

if obj['code'] == 0 :
    # 查询文件状态
    statRet = cos.stat('bucket', 'dir/test.mp4')
    print statRet
    
    # 删除文件
    print cos.delete('bucket', 'dir/test.mp4')

	
```
