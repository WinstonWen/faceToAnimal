"""
代码57行中 imgfacce变量 换头像
输入’q‘关闭
cv2 安装 cmd下 pip install opencv-python
记得更改39行处文件
"""

import math,random,numpy
import cv2 as cv
from PIL import Image  #PIL为图像处理包


def compoundImg(img1,imgface,faces):
    '''在原图的人脸上贴图'''
    img = Image.open(img1)  # 打开图像
    for face in faces:
        face = list(face)
        img2 = Image.open(imgface)
        img2= img2.convert("RGBA")
        img2 = img2.resize((face[2]*2,face[3]*2),Image.ANTIALIAS)
        img.paste(img2,(face[0]-int(face[2]/2),face[1]-int(face[3]/2)),mask=img2)
    # img.show()
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
    # 将文件路径换成自己电脑上的路径（我的python安装目录D:\software\python3.7.4\）
    faceCascade = cv.CascadeClassifier(
        r'D:\software\python3.7.4\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    img = cv.imread(imgname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(32, 32)
    )
    return faces


if __name__=='__main__':
    cap = cv.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        cv.imwrite('img/1.jpg', frame, [int(cv.IMWRITE_JPEG_QUALITY), 95])
        img = "img/1.jpg"
        imgface = "img/face1.png"
        faces = findface(img)
        frame = compoundImg(img,imgface, faces)
        cv.namedWindow("video", cv.WINDOW_AUTOSIZE)
        cv.imshow("video", frame)
        if cv.waitKey(100) & 0xff == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
