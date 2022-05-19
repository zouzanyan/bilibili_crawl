import requests
import re


# 去除文件名中的特殊字符
def fixname(name):
    character = r'[?*/\|:><]'
    name = re.sub(character, "", name)  # 用正则表达式去除windows下的特殊字符，这些字符不能用在文件名
    return name


class BilibiliCrawl:
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Referer': 'https://www.bilibili.com/'
    }

    def get_aid(self, bv):  # 根据bv号获取aid号
        url_aid = f'https://api.bilibili.com/x/web-interface/view?bvid={bv}'
        response = requests.get(url=url_aid, headers=self.headers).json()
        avid = response["data"]["aid"]  # 获取视频avid
        title = response["data"]["title"]  # 获取视频标题
        # cover = response["data"]["pic"]     # 获取封面
        return avid, title

    def get_cid(self, avid):  # 根据aid号获取cid号
        url_cid = f'https://api.bilibili.com/x/player/pagelist?aid={avid}'
        response = requests.get(url=url_cid, headers=self.headers).json()
        cid = response["data"][0]["cid"]
        return cid

    def get_video(self, avid, cid):  # 根据avid和cid获取视频源地址
        url_resourse = f'https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&qn=32'
        response = requests.get(url=url_resourse, headers=self.headers).json()
        video_url = response["data"]["durl"][0]["url"]  # 获得视频源地址
        return video_url

    def download_video(self, video_url, title):     # 根据视频源地址下载视频存入本地
        video_data = requests.get(url=video_url, headers=self.headers, stream=True)
        print('下载中......\n')
        with open(f'{title}.flv', 'wb') as file:
            for i in video_data.iter_content(10000):
                file.write(i)
        print("下载完成!!!\n")

    def main(self):
        bvid = input("请输入bv号\n")
        avid = str(self.get_aid(bvid)[0])
        title = fixname(str(self.get_aid(bvid)[1]))
        cid = str(self.get_cid(avid))
        video_url = self.get_video(avid, cid)
        self.download_video(video_url, title)


bili = BilibiliCrawl()
bili.main()
