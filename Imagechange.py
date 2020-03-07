"""
腾讯优图appid，secret_id，secret_key等需要自己申请
功能模块：
1.对图片进行缩小重新存放（腾讯优图只能对1M一下的图片进行分析）
2.上传图片返回得到字典类型数据
3.利用得到的脸部信息把动物头像贴放到固定位置
工具包函数介绍见readme.md
可优化：
1.侧脸时贴图不自然，有兴趣可以尝试
"""


import math,random,numpy
import cv2 as cv
from PIL import Image  #PIL为图像处理包
import TencentYoutuyun #腾讯优图依赖包

def compoundImg(img1,faces,fb):
    '''在原图的人脸上贴图'''
    img = Image.open(img1)  # 打开图像
    for face in faces:
        centre1, centre2, left, right = face["nose"][1], face["face_profile"][10], face["face_profile"][0], \
                                        face["face_profile"][20]  #分别为鼻梁，下巴，左右耳朵附件
        imgface = 'face' + str(random.randint(0, 6)) + '.png' # 随机选择动物头像
        img2 = Image.open(imgface)
        img2= img2.convert("RGBA")

        # 计算图片大小
        cmy = (centre2['y'] - centre1['y']) * 2
        b=cmy/img2.size[1]/fb #
        cmx=int(img2.size[0]*b*2)
        cmy=int(img2.size[1]*b*2)
        img2 = img2.resize((cmx,cmy),Image.ANTIALIAS)

        r=math.tan((centre2['y'] - centre1['y'])/(centre2['x'] - centre1['x']))
        r=(360-r)%360
        # print(r)
        img2=img2.rotate(r)
        img.paste(img2,(int(centre1['x']/fb-cmx/2),int(centre1['y']/fb-cmy/2*1.2)),mask=img2)
    # img.show(
    return cv.cvtColor(numpy.asarray(img),cv.COLOR_RGB2BGR)


def srinkimage(imgname):
    # 缩小图片重新存放
    im = Image.open(imgname)
    (x, y) = im.size  # read image size
    x_s = 600  # define standard width
    y_s = int(y * x_s / x)  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save('_' + imgname)
    return x_s/x


def findface(imgname):
    '''在图片中找出所有脸的位置'''
    appid = '********'  # 你的appid
    secret_id = '*************'  # 你的secret_id
    secret_key = '****************'  # 你的secret_key
    userid = 'rtx'  # 任意字符串
    # end_point = TencentYoutuyun.conf.API_TENCENTYUN_END_POINT  // 腾讯云
    # end_point = TencentYoutuyun.conf.API_YOUTU_VIP_END_POINT   // 人脸核身服务(需联系腾讯优图商务开通权限，否则无法使用)
    end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT  # 优图开放平台
    youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key)
    ret = youtu.FaceShape(image_path='_'+imgname, mode=0, data_type=0)
    print(ret)
    return ret["face_shape"]


if __name__ == '__main__':
    # 对单张图片贴图
    # for i in range(16):
    #     img='test'+str(i)+'.jpg' # 原图地址
    #     try:
    #         fb = srinkimage(img) # fb为原图和缩小图的缩放比例
    #         faces=findface(img)  # faces为脸部位点
    #         compoundImg(img,faces,fb)
    #     except Exception as e:
    #         print(e)
    #         continue


    cap = cv.VideoCapture(0)
    while 1:
        ret,frame = cap.read()
        cv.imwrite('1.jpg', frame, [int(cv.IMWRITE_JPEG_QUALITY), 95])
        img = "1.jpg"
        fb = srinkimage(img)
        faces=findface(img)
        frame = compoundImg(img,faces,fb)
        cv.namedWindow("video", cv.WINDOW_AUTOSIZE)
        cv.imshow("video",frame)
        if cv.waitKey(100) & 0xff == ord('q'):
                break
    cap.release()
    cv.destroyAllWindows()
