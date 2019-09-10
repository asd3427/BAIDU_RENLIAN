from aip import AipFace
import cv2
import base64
import sys
import os
import time
import sqlite3
import shutil
from aip import AipImageSearch, AipOcr
import re

face = AipFace(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
               secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")
image_search = AipImageSearch(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
                              secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")
ocr = AipOcr(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
             secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")


class Search:
    def __init__(self):
        pass

    def password(self):
        try:
            user_name, password = input('请输入使用者名称,登录密码').split(',')
            conn = sqlite3.connect('user_info.db')
            params = (user_name, password)
            check_user = conn.execute(
                "SELECT NAME, PASSWORD FROM USER_INFO WHERE  NAME=? and PASSWORD=?", params)
            check = [i for i in check_user]
            print(check)
            if check[0] is not False:
                return [True, user_name]
        except Exception as e:
            print(e)
            return [False]

    def paizhao(self):
        """
        pwd_check 0 is T or F 1 is username
        :return:
        """
        pwd_check = self.password()
        try:
            if pwd_check[0] is not True:
                print('登陆失败请重试')
                sys.exit()
        except Exception as e:
            print(e)
        print('账号密码验证成功')
        search_sfz = self.search_sfz()
        if search_sfz[0] is not True:
            print('身份证认证失败')
            sys.exit()
        print('{} 身份证验证成功'.format(search_sfz[1]))
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        face_cascade.load('./data\haarcascade_frontalface_default.xml')
        eye_cascade.load('./data\haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)
        user_conter = input("是否要进行脸部验证 Y or N :")

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

                cv2.imwrite(user_class + '\\' + user_class + str(i) + '.jpg', img[y:y + h, x:x + w],
                            [int(cv2.IMWRITE_JPEG_QUALITY), 1000])
                i += 1
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            cv2.imshow('img', img)
            if cv2.waitKey(30) & 0xFF == ord('q'):  # 获取多张图片直到你按停止
                break
            if i > 10:
                break

        cap.release()

        cv2.destroyAllWindows()
        self.search(user_class=user_class, user_name=pwd_check[1])

    def search(self, user_class, user_name):
        k = 0
        t = os.listdir(user_class)

        for i in range(0, len(t), 1):
            file_name = open(r'.\%s\%s%s.jpg' % (user_class, user_class, i), 'rb')

            # 参数images：图像base64编码
            # group_id_list 这里需要说明一下 这是指 人脸库 >>用户组 要输入用户组的名称且用户组名称不能为中文否则会报错
            img1 = base64.b64encode(file_name.read())
            options = {}
            options['user_id'] = user_name
            search_in_baidu = face.search(group_id_list=user_class, image=str(img1, 'utf-8'), image_type="BASE64",
                                          options=options)
            # print(search_in_baidu)
            file_name.close()
            if search_in_baidu['error_code'] == 0:
                result = search_in_baidu['result']
                score = result['user_list'][0]['score']
                if score >= 90:
                    k += 1
                    class_name = result['user_list'][0]['group_id']
                    user_name = result['user_list'][0]['user_id']
                    print('组别名称%s使用者名称%s相似度%s' % (class_name, user_name, score))

                    if k == 3:

                        print('成功比配3次')
                        del_ = input('比对完成 您是否要删除这比资料 请输入 Y or N :')
                        if del_ == 'Y':
                            group_id, user_id = input('请出入需要删除的 "组名"和 "使用者名称": ').split(',')
                            self.del_face_data(group_id=group_id, user_id=user_id)
                        else:
                            print('您选择不删除')
                            break
                else:
                    print('你不是本人噢请不要乱来相似度过低%s' % score)
                    file_name.close()
                    sys.exit()
            else:
                print(search_in_baidu['error_msg'])

        try:
            print('删除资料夹')
            shutil.rmtree(r'.\%s' % user_class)  # todo 优化代码
        except Exception as e:
            print(e)
        sys.exit()

    #@staticmethod
    def search_sfz(self):
        """
        搜寻身份证图片
        :return: True
        """
        print('入庫身分證資料')
        image_names = os.listdir('search/')
        if not image_search:
            print('找不到圖片')
            return False
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

            conn = sqlite3.connect('user_info.db')
            params = (name, ids)
            check_user = conn.execute(
                "SELECT Id_Card_name, Id_Card_num FROM USER_INFO WHERE  Id_Card_name like ? and Id_Card_num like ?",
                params)
            datas = check_user.fetchall()
            fp.close()
            print('刪除身分證資料')
            os.remove(r'./search/{}'.format(image_names[0]))
            if not datas:
                return [False]
            return [True,datas[0][0]]


        except Exception as e:
            print(e)
            return False

    @staticmethod
    def del_face_data(group_id, user_id):
        """
        删除百度人脸库里里面指定用户
        :param group_id: 使用者的组名为注册时的user_class EX:test
        :param user_id: 使用者名称
        :return:
        """
        del_baidu = face.deleteUser(group_id, user_id)
        if del_baidu['error_code'] == 0:

            print(del_baidu)
        else:
            print(del_baidu['error_msg'])


# todo 优化代码


a = Search()
a.paizhao()