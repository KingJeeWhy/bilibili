#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time     :2021/02/21 16:14
# @Author   :KingJeeWhy
# @FileName :bilibili_browser.py


import json
import sys
import ssl

from urllib import request, error

# 全局取消证书验证 => 解决urllib报错的问题
ssl._create_default_https_context = ssl._create_unverified_context


class BiliBili:
    # 构造请求头
    __headers = {
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "referer": "https://www.bilibili.com/",
    }

    def __init__(self, url):
        self.url = url

    # 获取BVID
    def __bvid(self):
        bvid = self.url.split('/')[len(self.url.split('/')) - 1]
        if '?' in bvid:
            bvid = bvid.split('?')[0]
        return bvid

    # 获取CID
    def __cid(self):
        url = f"https://api.bilibili.com/x/player/pagelist?bvid={self.__bvid()}&jsonp=jsonp"
        req = request.Request(url, headers=self.__headers, method="GET")
        reponse = request.urlopen(req).read().decode("utf-8")
        return json.loads(reponse)['data'][0]["cid"]

    # 设置cookie
    def set_cookie(self, cookie):
        self.__headers['cookie'] = cookie

    # 获取视频url
    def video_url(self):
        url = f"https://api.bilibili.com/x/player/playurl?avid=&cid={self.__cid()}&bvid={self.__bvid()}&qn=120&type=&otype=json"
        req = request.Request(url, headers=self.__headers, method="GET")
        response = request.urlopen(req).read().decode("utf-8")
        return json.loads(response)['data']['durl'][0]['url']


# 进度条
def progressbar(cur, total=100):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %s" % ('=' * int(cur), percent))
    sys.stdout.flush()


# 进度条百分比
def schedule(blocknum, blocksize, totalsize):
    """
    blocknum:当前已经下载的块
    blocksize:每次传输的块大小
    totalsize:网页文件总大小
    """
    if totalsize == 0:
        percent = 0
    else:
        percent = blocknum * blocksize / totalsize
    if percent > 1.0:
        percent = 1.0
    percent = percent * 100
    # 格式：download：99.99%
    # print("download : %.2f%%" % (percent))
    # 格式: [===========             ] 50.00%
    progressbar(percent)


# 生成文件名
def get_filename(url):
    deal_with_url = url.split('/')[len(url.split('/')) - 1]
    if "?" in deal_with_url:
        filename = deal_with_url.split("?")[0] + '.flv'
    else:
        filename = deal_with_url + '.flv'
    return filename


# 下载视频
def download_by_urlretrieve(url, filename):
    try:
        opener = request.build_opener()
        opener.addheaders = ([("User-Agent",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"),
                              ('referer', 'https://www.bilibili.com/')])
        request.install_opener(opener)
        request.urlretrieve(url, filename, schedule)
    except error.HTTPError as e:
        print(e)
        print('\r\n' + filename + ' download failed!' + '\r\n')
    else:
        print('\r\n' + filename + ' download successfully!')


def main():
    url = input("请输入视频地址：")
    bilibili = BiliBili(url)
    is_cookie = input("是否设置cookie以获取更高的清晰度视频(Y/N):")
    if is_cookie.upper() == "Y":
        cookie = input("请将cookie粘贴到此处：\n")
        bilibili.set_cookie(cookie)
    else:
        pass
    video_url = bilibili.video_url()
    filename = get_filename(url)
    download_by_urlretrieve(video_url, filename)


if __name__ == '__main__':
    main()
