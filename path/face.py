from aip import AipFace
import cv2
import base64
import sys
import os
import random
import win32api, win32con

save_path = r".\\img\\"


def face_eye():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    face_cascade.load('D:\python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    eye_cascade.load('D:\python\Lib\site-packages\cv2\data\haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)
    user_conter = input("是否要注册 Y or N :")

    if user_conter is not 'Y':
        sys.exit()

    class_name = input('输入类名:')
    user_name = input("输入使用者名称")
    user_pwd = input("输入使用者密码")
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

            cv2.imwrite(save_path + user_name + str(i) + '.jpg', img[y:y + h, x:x + w])
            i += 1
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        cv2.imshow('img', img)
        if cv2.waitKey(30) & 0xFF == ord('q'):  # 获取多张图片直到你按停止
            break
        t = os.listdir(save_path)
        if len(t) > 10:
            break

    cap.release()

    cv2.destroyAllWindows()
    print("感谢%s完成注册您的密码是%s您的组名是%s" % (user_name, user_pwd, class_name))


def baidu():
    # 初始化aipFace

    filePath = r'.\img'  # 获取资料夹下所有图片的名称
    t = os.listdir(filePath)

    APP_ID = '15914558'
    API_KEY = '189kSDORqbGOIb74THb1cxft'
    SECRET_KEY = 'jnYWGi6rk9BvCWLYMyQvAaiP1ajbhs5n'

    aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

    a = random.choices(t, k=2)  # 图片数量多 所以随机取两张下去做比对

    options = {
        'max_face_num': 1,  # 人脸数量
        'face_fields': "expression,faceshape",
    }

    # 人俩比对部分
    result = aipFace.match([
        {
            'image': str(base64.b64encode(open(filePath + '\\' + a[0], 'rb').read()).decode()),
            'image_type': 'BASE64',
        },
        {
            'image': str(base64.b64encode(open(filePath + '\\' + a[1], 'rb').read()).decode()),
            'image_type': 'BASE64',
        }
    ])

    print(str(base64.b64encode(open(filePath + '\\' + a[0], 'rb').read()).decode()))
    print('\n')
    aaa = result['result']['score']
    print("相似得分为："), print(aaa)
    if aaa > 80:
        print("图1和图2是同一个人.\n")
    else:
        print("图1和图2不是同一个人.\n")


if __name__ == '__main__':
    t = os.listdir(save_path)

    if len(t) < 10:
        face_eye()  # 如果你要获取多张图片那下面的百度AI 就不会动 所以 我这里设定 50

    baidu()
