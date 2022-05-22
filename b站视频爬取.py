import requests
import re


# 去除文件名中的特殊字符
def fixname(name):
    character = r'[?*/\|:><]'
    name = re.sub(character, "", name)  # 用正则表达式去除windows下的特殊字符，这些字符不能用在文件名
    return name


def regular_match(cvdata):  # 正则获取id
    bvid = re.findall('/BV(.{10})', cvdata)
    if bvid:
        return bvid[0], '0'
    else:
        pass
    epid = re.findall('/ep(.{6})', cvdata)
    if epid:
        return epid[0], '1'
    else:
        pass
    exit('请粘贴正确的视频链接地址!!!')


class BilibiliCrawl:
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Referer': 'https://www.bilibili.com/'
    }

    def get_aid_cid_from_epid(self, ep):  # 根据ep号获取aid和cid号
        url_aid_cid = f'https://api.bilibili.com/pgc/view/web/season?ep_id={ep}'
        response = requests.get(url=url_aid_cid, headers=self.headers).json()
        if response["code"] != 0:
            exit("资源不可达")
        list_ep = response["result"]["episodes"]  # 取得番剧列表
        for i in range(len(list_ep)):
            if list_ep[i]["id"] == int(ep):
                avid = list_ep[i]["aid"]
                cid = list_ep[i]["cid"]
                title = list_ep[i]["share_copy"]
                return avid, cid, title  # 返回aid,cid和标题
            else:
                continue

    def get_aid_cid_from_bvid(self, bv):  # 根据bv号获取aid号
        url_aid = f'https://api.bilibili.com/x/web-interface/view?bvid={bv}'
        response = requests.get(url=url_aid, headers=self.headers).json()
        if response["code"] != 0:
            exit("资源不可达")
        avid = response["data"]["aid"]  # 获取视频avid
        title = response["data"]["title"]  # 获取视频标题
        # cover = response["data"]["pic"]     # 获取封面
        url_cid = f'https://api.bilibili.com/x/player/pagelist?aid={avid}'
        response = requests.get(url=url_cid, headers=self.headers).json()
        cid = response["data"][0]["cid"]
        return avid, cid, title

    def get_video(self, avid, cid):  # 根据avid和cid获取视频源地址
        url_resourse = f'https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&qn=32'
        response = requests.get(url=url_resourse, headers=self.headers).json()
        video_url = response["data"]["durl"][0]["url"]  # 获得视频源地址
        return video_url

    def download_video(self, video_url, title):  # 根据视频源地址下载视频存入本地
        video_data = requests.get(url=video_url, headers=self.headers, stream=True)
        print('下载中......')
        with open(f'{title}.flv', 'wb') as file:
            for i in video_data.iter_content(10000):
                file.write(i)
        print("下载完成!!!\n")

    def main(self):
        while 1:
            iid = input("请在此粘贴视频地址\n")
            iid = regular_match(iid)
            if iid[1] == '0':
                bv = self.get_aid_cid_from_bvid(iid[0])
                bv_url = self.get_video(bv[0], bv[1])
                self.download_video(bv_url, bv[2])
            else:
                ep = self.get_aid_cid_from_epid(iid[0])
                ep_url = self.get_video(ep[0], ep[1])
                self.download_video(ep_url, ep[2])


bili = BilibiliCrawl()
bili.main()
