from aip import AipFace
import cv2
import base64
import sys
import os
import shutil

face = AipFace(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
               secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")


class FaceChick:
    def __init__(self):
        pass

    def face_eye(self):  #
        save_path = "img"

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassnifier('haarcascade_eye.xml')

        face_cascade.load('D:\python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        eye_cascade.load('D:\python\Lib\site-packages\cv2\data\haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)
        user_conter = input("是否要注册 Y or N :")

        if user_conter is not 'Y':
            sys.exit()

        class_name = input('输入类名:')
        user_name = input("输入使用者名称")
        user_pwd = input("输入使用者密码")

        if not os.path.isdir(user_name):
            os.makedirs(user_name)

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
                save_path = save_path + user_name
                cv2.imwrite(user_name + '\\' + user_name + str(i) + '.jpg', img[y:y + h, x:x + w],
                            [int(cv2.IMWRITE_JPEG_QUALITY), 1000])
                i += 1
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            cv2.imshow('img', img)
            if cv2.waitKey(30) & 0xFF == ord('q'):  # 获取多张图片直到你按停止
                break
            t = os.listdir(user_name)
            if len(t) > 10:
                break

        cap.release()

        cv2.destroyAllWindows()
        print("感谢%s完成注册您的密码是%s您的组名是%s" % (user_name, user_pwd, class_name))
        self.add_to_baidu(class_name=class_name, user_name=user_name)

    @staticmethod
    def add_to_baidu(class_name, user_name):
        """

        :param class_name: 祖名
        :param user_name: 个人名称
        :return: 新增成功
        """

        t = os.listdir(user_name)
        print(len(t))
        for i in range(0, len(t), 1):
            f = open(r'.\%s\%s%s.jpg' % (user_name, user_name, i), 'rb')
            # 参数images：图像base64编码
            img1 = base64.b64encode(f.read())

            s = face.addUser(image=str(img1, 'utf-8'), image_type="BASE64", group_id=class_name, user_id=user_name)
            if s['error_code'] == 0:
                print('以新增资料')
                f.close()
            else:
                f.close()
                print(s['error_msg'])
        try:
            print('删除资料夹')
            shutil.rmtree(r'.\%s' % user_name)  # todo 优化代码
        except Exception as e:
            print(e)


a = FaceChick()
a.face_eye()
