from aip import AipFace
import cv2
import base64
import sys
import os
import time

face = AipFace(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
               secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")


class search:
    def __init__(self):
        pass

    def password(self):
        password = input('请输入登录密码')

    def paizhao(self):

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        face_cascade.load('D:\python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        eye_cascade.load('D:\python\Lib\site-packages\cv2\data\haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)
        user_conter = input("是否要登陆 Y or N :")

        if user_conter is not 'Y':
            sys.exit()

        user_class = input("输入组名")

        if not os.path.isdir(user_class):
            os.makedirs(user_class)

        i = 0
        while True:

            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                eyes = eye_cascade.detectMultiScale(roi_gray)

                cv2.imwrite(user_class + str(i) + '.jpg', img[y:y + h, x:x + w],
                            [int(cv2.IMWRITE_JPEG_QUALITY), 1000])
                i += 1
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            if i > 10:
                break

        cap.release()

        cv2.destroyAllWindows()
        self.search(user_class=user_class)

    @staticmethod
    def search(user_class):
        for i in range(0, 10, 1):
            file_name = r'%s%i.jpg' % (user_class, i)
            f = open(file_name, 'rb')

            # 参数images：图像base64编码
            # group_id_list 这里需要说明一下 这是指 人脸库 >>用户组 要输入用户组的名称且用户组名称不能为中文否则会报错
            img1 = base64.b64encode(f.read())
            search_in_baidu = face.search(group_id_list=user_class, image=str(img1, 'utf-8'), image_type="BASE64")
            if search_in_baidu['error_code'] == 0:
                f.close()
                try:
                    print('匹配成功5秒后删除图片%s' % file_name)
                    time.sleep(5)
                    os.remove(file_name)
                except:
                    pass
            else:
                print('你不是本人噢请不要乱来')


# todo 优化代码


a = search()
a.paizhao()
