# 使用百度AI 来完成多重登陆验证

`安装依赖 pip install -r requirements.txt `

如何使用:

1.首先完成人脸库的注册 运行 `face.py` 会拍摄10张照片 并上传到百度人脸库

2.资料上传完成之后 运行`serarch_baidu.py`也会拍10张照片之后与人脸库里的资料作比对

注意:
在face.py里需要注意以下两点

1.这部份需要替换成你的百度AI 的资料

`face = AipFace(appId='16058688', apiKey="AyGxQXLmWTfftUueyVSyjVVe",
               secretKey="oPR4BQ5sdhUwvxxsClUxWTpIeqf8dTXW")`

2.这部份也需要注意这里的类名一定要记得还要注意类名不能使用中文!!

`class_name = input('输入类名:')`

在search.py里需要注意个group_id_list=user_class 这里就是face.py里面的类名如果忘记了
请登录百度AI控制台>>>产品服务 / 人脸识别 - 人脸库管理 / test_for_paper

`search_in_baidu = face.search(group_id_list=user_class, image=str(img1, 'utf-8'), image_type="BASE64")`

search_baidu 输出如下

`组别名称test使用者名称chen相似度97.488624572754

匹配成功5秒后删除图片test0.jpg
`

## 注意所有拍摄的资料都会在上传以及识别后删除
TODO:

* 1.优化代码

* 2.增加指纹识别功能

* 3.增加身份证识别功能

* 4.将代码界面化 并打包成EXE
