# bilibiliAutoDownload
# 本项目仅供个人交流学习使用，禁止用于商业用途。使用此脚本造成的一切纠纷本人概不负责
## 简介
### 功能&特性
#### -1- 按收藏夹名整理视频，分p视频保存在标题同名文件夹，视频标题为对应p视频标题
#### -2- 多线程下载，暂时不支持断点续传
#### -3- 增量下载，收藏夹视频删减仍保留本地视频
#### -4- xml格式弹幕下载，flv/MP4格式可选下载(MP4格式需要mmpeg4工具混流)
#### -5- 本地保留收藏夹信息原始数据
### 环境
### -1- python3
### -2- you-get
### -3- requests
## 使用方法
#### -1- 登录B站，打开想要下载到本地的收藏夹。复制浏览器地址栏的收藏夹id(纯数字)![avatar](./example/1.png)
#### -2- 打开 bilibili.py ，修改以下两个参数
```
        DOWNLOAD_PATH:  '收藏夹下载路径'
        FAV_LIST:       '收藏夹id'
```
![avatar](./example/2.png)
#### -3- 双击运行
