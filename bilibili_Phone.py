#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time     :2021/02/21 15:37
# @Author   :KingJeeWhy
# @FileName :bilibili_Phone.py

import re
import sys
import ssl

from urllib import request, error

# 全局取消证书验证 => 解决urllib报错的问题
ssl._create_default_https_context = ssl._create_unverified_context


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


# 获取视频url
def get_video_url(url, headers):
    req = request.Request(url, headers=headers, method="GET")
    try:
        response = request.urlopen(req).read().decode('utf-8')
    except error.HTTPError as e:
        print(e)
        print('\r\n' + url + 'download failed' + '\r\n')
    video_url = re.search(r"readyVideoUrl: '(.*)?'", response)[0][16: -1]
    return video_url


# 下载视频
def download_by_urlretrieve(url, filename):
    try:
        opener = request.build_opener()
        opener.addheaders = ([("User-Agent",
                               "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36 Edg/88.0.705.74"),
                              ('referer', 'https://m.bilibili.com/')])
        request.install_opener(opener)
        request.urlretrieve(url, filename, schedule)
    except error.HTTPError as e:
        print(e)
        print('\r\n' + filename + ' download failed!' + '\r\n')
    else:
        print('\r\n' + filename + ' download successfully!')


def main():
    url = input("请输入视频地址：")
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36",
        "referer": "https://m.bilibili.com/"
    }
    # url = ""
    video_url = get_video_url(url, headers)
    deal_with_url = url.split("/")[len(url.split("/")) - 1]
    if "?" in deal_with_url:
        filename = deal_with_url.split("?")[0] + '.mp4'
    else:
        filename = deal_with_url + '.mp4'
    download_by_urlretrieve(video_url, filename)


if __name__ == '__main__':
    main()
