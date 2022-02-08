# 哔哩哔哩视频爬取

#### 1.使用方法

安装ffmpeg(https://github.com/BtbN/FFmpeg-Builds/releases),并且设置为系统环境变量

下载代码执行所需要的库requests,json,os,threading

运行后输入需要下载的视频编号,下载的视频自动存入项目的downloads目录下



#### 2.原理

使用requests.get获得通过re筛选过后的音频和视频链接ur以及l对应的媒体数据

使用ffmpeg开源工具合成音频和视频





