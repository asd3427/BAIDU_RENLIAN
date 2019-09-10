from aip import AipFace
import cv2
import base64
import sys
import os
import shutil
import sqlite3
from aip import AipImageSearch, AipOcr
import re

face = AipFace(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
               secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")
image_search = AipImageSearch(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
                              secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")
ocr = AipOcr(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
             secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")


class FaceChick:
    def __init__(self):
        pass

    def face_eye(self):  #

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        face_cascade.load('./data\haarcascade_frontalface_default.xml')
        eye_cascade.load('./data\haarcascade_eye.xml')

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
        idcardinfo = self.ocr_image()
        self.add_to_database(user_name=user_name, user_pwd=user_pwd, class_name=class_name, idcardinfo=idcardinfo)
        self.add_to_baidu(class_name=class_name, user_name=user_name)

        self.upload_image(user_name=user_name)  # 这块功能未启用 百度要求实名认证 无法玩成

    @staticmethod
    def add_to_database(user_name, user_pwd, class_name, idcardinfo):
        """
        建立资料库，新增使用者资料到资料库
        :param user_name:
        :param user_pwd:
        :param class_name:
        :return:
        """
        if not idcardinfo:
            idcardinfo = []
            os._exit(0)

        conn = sqlite3.connect('user_info.db')
        params = (user_name, user_pwd, class_name, idcardinfo[0], idcardinfo[1], idcardinfo[2])
        c = conn.cursor()

        try:
            c.execute('''CREATE TABLE USER_INFO
                   (
                   NAME                  TEXT    NOT NULL,
                   PASSWORD              CHAR(50)     NOT NULL,
                   USER_CLASS            CHAR(50),
                   Id_Card_name CHAR(30),
                   Id_Card_num CHAR(30),
                   Id_Card_give_date CHAR(30))
                   
                   ;''')

        except Exception as e:
            print(e, '资料库已存在')

        conn.execute("INSERT INTO USER_INFO VALUES (?,?,?,?,?,?)", params)
        conn.commit()
        conn.close()

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

    @staticmethod
    def upload_image(user_name):  # todo 等待实名认证资料
        print("提示请先将文件放置于 upload 资料夹内")

        file_names = os.listdir('upload')
        if len(file_names) is 0:
            print('未将图片放置到指定资料夹')
            sys.exit()
        for file_name in file_names:
            if user_name in file_name:
                print(1)
            else:
                print(file_name)
                # with open('./upload/%s' % file_name, 'rb') as fp:
                #     image = fp.read()
                #     print('读取成功%s' % file_name)
                #     options = {}
                #     options["brief"] = {user_name}
                #     result = image_search.similarAdd(image=image, options=options)
                #     fp.close()
                #     if 'error_msg' not in result:
                #         print('恭喜你完成所有认证')

    def ocr_image(self):
        print('入庫身分證資料')
        image_names = os.listdir('search/')
        if not image_search:
            print('找不到圖片')
            return []
        try:
            with open(r'./search/{}'.format(image_names[0]), 'rb') as fp:
                image = fp.read()

            """ 调用通用文字识别, 图片参数为本地图片 """
            options = {}
            options["detect_direction"] = "true"
            # options["probability"] = "true"
            a = ocr.basicAccurate(image, options=options)
            cd = ''
            ret = (a['words_result'])
            for i in ret:
                cd += i['words']

            # cd = '米中華民國國民身分證姓名陳曙光出生民國81年5月12日年月日性别男發證日期民100年3月14日(中市)换發L190002001'
            name = re.findall('姓名(\w{3})', cd)[0]  # '^[\u4e00-\u9fa5_a-zA-Z0-9]+$'
            ids = re.findall('發(\w{10})', cd)[1]
            give_date = re.findall('發證日期(\w+)*', cd)[0]
            return [name, ids, give_date]
        except Exception as e:
            print(e)
            return []


a = FaceChick()
a.face_eye()
