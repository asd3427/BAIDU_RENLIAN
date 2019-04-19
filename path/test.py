# import urllib
# import ssl
# from urllib import request, parse
# import json
#
#
# # client_id 为官网获取的AK， client_secret 为官网获取的SK
# def get_token():
#     context = ssl._create_unverified_context()
#     client_id = '189kSDORqbGOIb74THb1cxft'
#     client_secret = 'jnYWGi6rk9BvCWLYMyQvAaiP1ajbhs5n'
#     host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
#     client_id, client_secret)
#     request = urllib.request.Request(host)
#     request.add_header('Content-Type', 'application/json; charset=UTF-8')
#     response = urllib.request.urlopen(request, context=context)
#     # 获取请求结果
#     content = response.read()
#     # 转换为字符
#     content = bytes.decode(content)
#     # 转换为字典
#     content = eval(content[:-1])
#     print(content['access_token'])
#     return content['access_token']
#
#
# # 转换图片
# # 读取文件内容，转换为base64编码
# # 二进制方式打开图文件
# def imgdata(file1path, file2path):
#     import base64
#     f = open(r'%s' % file1path, 'rb')
#     pic1 = base64.b64encode(f.read())
#     f.close()
#     f = open(r'%s' % file2path, 'rb')
#     pic2 = base64.b64encode(f.read())
#     f.close()
#     # 将图片信息格式化为可提交信息，这里需要注意str参数设置
#     params = json.dumps(
#         [{"image": str(pic1, 'utf-8'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
#          {"image": str(pic2, 'utf-8'), "image_type": "BASE64", "face_type": "IDCARD", "quality_control": "LOW"}]
#     )
#     return params.encode(encoding='UTF8')
#
#
# # 进行对比获得结果
# def img(file1path, file2path):
#     token = get_token()
#     # 人脸识别API
#     # url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token='+token
#     # 人脸对比API
#     context = ssl._create_unverified_context()
#     # url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' + token
#     params = imgdata(file1path, file2path)
#
#     request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
#     request_url = request_url + "?access_token=" + token
#     request = urllib.request.Request(url=request_url, data=params)
#     request.add_header('Content-Type', 'application/json')
#     response = urllib.request.urlopen(request, context=context)
#     content = response.read()
#     content = eval(content)
#     # # 获得分数
#     score = content['result']['score']
#     if score > 80:
#         return '照片相似度：' + str(score) + ',同一个人'
#     else:
#         return '照片相似度：' + str(score) + ',不是同一个人'
#
#
# if __name__ == '__main__':
#     file1path = r'.\img\chen00.jpg'
#     file2path = r'.\img\chen01.jpg'
#     res = img(file1path, file2path)
#     print(res)

# encoding:utf-8
import base64
import urllib
import requests

'''
人脸注册
'''

request_url = "https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/add"

f = open(r'.\img\achen0.jpg', 'rb')
# 参数images：图像base64编码
img1 = base64.b64encode(f.read())
# 二进制方式打开图文件
f = open(r'.\img\achen4.jpg', 'rb')
# 参数images：图像base64编码
img2 = base64.b64encode(f.read())
header = {'Content-Type': 'application/x-www-form-urlencoded'}
params = {"group_id": "test_group_2", "images": str(img1) + ',' + str(img2), "uid": "test_user_5", "user_info": "userInfo5"}
access_token = '24.0fd30f3e6395d8c657b58f847fcb840b.2592000.1558231931.282335-15914558'
req = requests.post(request_url + "?access_token=%s" % access_token, data=params, headers=header)
print(req.text)
