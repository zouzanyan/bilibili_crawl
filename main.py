import requests
import re
import json
import os
import time
import threading


class Bilibili:
    def __init__(self):
        self.audio_url = None
        self.video_url = None
        os.chdir('./')
        if os.path.exists('cache'):  # 建立缓存目录
            pass
        else:
            os.mkdir('cache')
        if os.path.exists('downloads'):  # 建立下载目录
            pass
        else:
            os.mkdir('downloads')
        self.header = {
            'referer': 'https://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0'
                          '.4664.110 Safari/537.36'}  # 设置请求头,注意得加referer防盗链
        self.sign = None
        if re.findall('^BV', key_word):  # 判断输入的视频id是否合法
            self.url = f"https://www.bilibili.com/video/{key_word}"
            self.sign = 0
        elif re.findall('(^ep)|(^ss)', key_word):
            self.url = f"https://www.bilibili.com/bangumi/play/{key_word}"
            self.sign = 1
        else:
            print('视频ID格式错误!')
            exit()
        self.title = None

    def crawl(self):  # 爬取方法
        response = requests.get(self.url, headers=self.header)
        html_data = response.text    # 获取网页源代码
        if self.sign == 0:
            self.title = re.findall('<title data-vue-meta="true">(.*?)</title>', html_data)[0]  # 寻找视频标题
        if self.sign == 1:
            self.title = re.findall('<title>(.*?)</title>', html_data)[0]
        print(self.title + '\n正在下载视频中...\n')
        media_data = re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0]  # 寻找视频源数据
        json_data = json.loads(media_data)
        self.audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
        self.video_url = json_data['data']['dash']['video'][0]['baseUrl']

    def download_audio(self):
        print('音频下载开始>>>>>')
        audio_response = requests.get(self.audio_url, headers=self.header, stream=True)  # 注意设置stream=True
        with open('cache/a.mp3', 'wb') as f:  # 写入音频
            for i in audio_response.iter_content(10000):  # 设置断点下载,防止爆内存
                f.write(i)
        print('音频下载完成!')

    def download_video(self):
        print('视频下载开始>>>>>')
        video_response = requests.get(self.video_url, headers=self.header, stream=True)
        with open('cache/b.mp4', 'wb') as f:  # 写入视频
            for i in video_response.iter_content(10000):
                f.write(i)
        print('视频下载完成!')

    def compound(self):  # 利用ffmpeg进行音频和视频的合成方法
        cmd = 'ffmpeg -i cache/b.mp4 -i cache/a.mp3 -c:v copy -c:a aac -strict experimental downloads/c.mp4'
        os.system(cmd)
        os.remove("cache/a.mp3")
        os.remove("cache/b.mp4")
        os.chdir('downloads')
        os.rename('c.mp4', self.title + '.mp4')
        print('视频合成结束:', self.title)
        print('共花费时间为 : ' + format(time.time() - startTime, '.2f') + 's')
        os.chdir('..')


if __name__ == "__main__":
    while 1:
        key_word = input('输入bilibili视频链接ID:')
        startTime = time.time()
        a = Bilibili()
        a.crawl()
        t1 = threading.Thread(target=a.download_audio)
        t2 = threading.Thread(target=a.download_video)
        t1.start()
        t2.start()
        t2.join()
        a.compound()
