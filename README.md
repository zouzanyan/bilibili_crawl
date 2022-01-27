# 哔哩哔哩视频爬取
### 开发工具
windows10

pycharmcommunity

### 编译环境
Python 3.9.6 [MSC v.1929 64 bit (AMD64)] on win32

### 使用方法

安装windows下的ffmpeg(https://github.com/BtbN/FFmpeg-Builds/releases), 并且设置为系统环境变量

下载代码执行所需要的库requests,json,os

运行后输入需要下载的视频编号,下载的视频自动存入项目的downloads目录下

### 原理

使用requests.get获得通过re筛选过后的音频和视频链接ur以及l对应的媒体数据	(用json存的url数据)

使用ffmpeg工具合成音频和视频

#### 其他疑问请加qq1406823510



