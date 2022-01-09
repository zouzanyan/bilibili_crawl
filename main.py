import requests
import re
import json
import os


class Bilibili:
    def __init__(self):
        os.chdir('./')
        if os.path.exists('cache'):
            pass
        else:
            os.mkdir('cache')
        if os.path.exists('downloads'):
            pass
        else:
            os.mkdir('downloads')
        self.header = {
            'referer': 'https://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0'
                          '.4664.110 Safari/537.36'}
        self.sign = None
        if re.findall('^BV', key_word):
            self.url = f"https://www.bilibili.com/video/{key_word}"
            self.sign = 0
        elif re.findall('(^ep)|(^ss)', key_word):
            self.url = f"https://www.bilibili.com/bangumi/play/{key_word}"
            self.sign = 1
        else:
            print('视频ID格式错误!')
        self.title = None

    def crawl(self):
        response = requests.get(self.url, headers=self.header)
        html_data = response.text    # 获取网页数据
        if self.sign == 0:
            self.title = re.findall('<title data-vue-meta="true">(.*?)</title>', html_data)[0]
        if self.sign == 1:
            self.title = re.findall('<title>(.*?)</title>', html_data)[0]
        print(self.title + '正在下载视频中...')
        media_data = re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0]
        json_data = json.loads(media_data)
        audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
        video_url = json_data['data']['dash']['video'][0]['baseUrl']
        # print(audio_url)
        audio_content = requests.get(audio_url, headers=self.header).content
        video_content = requests.get(video_url, headers=self.header).content

        with open('cache/a.mp3', 'wb') as f:
            f.write(audio_content)
        with open('cache/b.mp4', 'wb') as f:
            f.write(video_content)
        print(self.title, '下载成功!!!!')

    def compound(self):
        print('音视频合并开始')
        cmd = 'ffmpeg -i cache/b.mp4 -i cache/a.mp3 -c:v copy -c:a aac -strict experimental downloads/c.mp4'
        os.system(cmd)
        os.remove("cache/a.mp3")
        os.remove("cache/b.mp4")
        print('清除cache成功')
        os.chdir('downloads')
        os.rename('c.mp4', self.title + '.mp4')
        print('视频合成结束:', self.title)
        print('等待ing~~~~~~')
        os.chdir('..')


if __name__ == "__main__":
    while 1:
        key_word = input('输入bilibili视频链接ID:')
        a = Bilibili()
        a.crawl()
        a.compound()
