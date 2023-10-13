# Jetson-lightGBM项目相关（部分）
* [下一步探索](./GroupMeeting.md)
## 代码结构
```
.
├── Jetson Nano电路图.pdf
├── Jetson-Nano相关参考资料.pdf
├── Jetson_Nano_User_Manual_cn.pdf
├── ads131m04.pdf(雷达电路图)
├── feature_and_trainModel
│   └── xxx.pkl(训练好的部分模型)
└── demo
|   ├── cloudfunctions（云函数相关）
|   └── miniprogram
|       ├── colorui(图标组件相关)
|       │   ├── components
|       │   ├── animation.wxss
|       │   ├── icon.wxss
|       │   └── main.wxss
|       ├── image
|       │    └── ... 部分图片
|       ├── pages（小程序各个功能页面）
|       │   ├── birthday
|       │   ├── day
|       │   ├── email
|       │   ├── forget
|       │   ├── heartrate
|       │   ├── home
|       │   ├── location
|       │   ├── login
|       │   ├── name
|       │   ├── number
|       │   ├── personal
|       │   ├── sex
|       │   ├── signup
|       │   ├── sleepheath
|       │   ├── sleepingBeats
|       │   ├── sleeptime
|       │   └── updatepassword
|       ├── app.js
|       ├── app.json
|       ├── app.wxss
|       ├── envList.js
|       └── sitemap.json
├── main
|   ├── upload (内容上传客户端相关)
|       │   ├── get_token.py(令牌获取)
|       │   ├── get_upload_url.py(报头传输)
|       │   ├── parse_form.py(表单解析)
|       │   ├── radar_sp_pbc_save_print.py(绘图并存储)
|       └── └── upload.py(上传)
|   ├── generate_distribution_features.py(生成新标签的训练数据)
|   ├── lightGBM-test.py(测试主程序)
|   ├── lightGBM.py
|   ├── model_train2.py(训练新标签的模型)
|   ├── radar_signal.py(处理雷达信号)
|   ├── radar_sp_pbc_print.py(输出PBC分布图和频谱)
|   ├── tag_get.py(旧标签处理)
└── └── tagChange.py(新标签处理)


```

## 备注
- 测试的主代码为lightGBM-test.py
- generate_distribution_features.py和radar_signal.py分别为对新标签的数据集进行特征生成和处理雷达信号的代码
- tagChange.py和tag_get2.py都是用于处理旧标签的代码，与程序无关
- radar_sp_pbc_print.py是用于输出PBC分布图和画频谱的代码
- model_train2.py是用于训练模型的代码
- upload中，get_token.py用于获取令牌，get_upload_url.py用于获取上传url，parse_form.py用于解析表单，upload.py用于上传文件

* [系统使用说明](./系统使用说明.md)