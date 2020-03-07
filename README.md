## faceToAnimal
### 主要流程：
打开图片，按比例缩小，重新存放；
上传缩小后图片，因上传的是缩小后图片，所有得到的也是缩小后的位点，需要同比例放大；
取我需要使用的四个点；
根据人脸大小计算动物头像大小，我是以下巴和鼻梁两点距离的两倍为脸的大小，然后同比例缩小放大头像到脸的两倍
根据两点之间的斜率求出脸的倾斜度，适当旋转头像；
以鼻梁的点为中心点和图片的大小，计算左上角位置贴上动物头像


*注意：动物头像必须为透明底的图片，在贴图时要转换weiRGN模式，否则会在图片空白处填充黑色

###  TencentYoutuyun介绍
TencentYoutuyun 依赖包 可到官网下载
api文档：
https://github.com/Tencent-YouTu/Python_sdk
本次代码使用部分，跟多内容都在上面链接
```
import time
import TencentYoutuyun

appid = 'xxx'
secret_id = 'xxxxxxx'
secret_key = 'xxxxxxxx'
userid= 'xxx'

#end_point = TencentYoutuyun.conf.API_TENCENTYUN_END_POINT  // 腾讯云
#end_point = TencentYoutuyun.conf.API_YOUTU_VIP_END_POINT   // 人脸核身服务(需联系腾讯优图商务开通权限，否则无法使用)
end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT        // 优图开放平台


youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

ret = youtu.FaceShape(image_path='you_path.jpg', mode = 0, data_type = 0)
print ret
```

### 人脸位点信息：
```
https://open.youtu.qq.com/#/open/developer/face-point
本次只我使用第34，68,78,88点，分别是nose[1],face_profile[0],face_profile[10],face_profile[20]
字典结构也在链接中
```

### PIL 图片处理
```
img = PIL.open(imagename) 打开图片
img.resize((x,y)) 改变图片大小
img.rotate(90) 逆时针90度
img.convert('RDBA') 图片转换为RGB模式
img.paste(img2,(x,y),mask=img2) 以img为背景把img2贴上，位置在(x,y)
img.show() 显示图片
img.size 图片大小
```


