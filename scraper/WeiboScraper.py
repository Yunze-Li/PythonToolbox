import os
import re
import sys
import time
from pathlib import Path

import requests


def get_one_page(url):
    """
    获取某一网页上的所有内容
    :param url: 网页的URL
    :return: 抓取出的HTML内容
    """
    headers = {
        'Connection': 'keep-alive',
        'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        'Host': 'weibo.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'NOTE: PLEASE REPLACED WITH YOUR COOKIE HERE!!!'
    }
    # 利用requests.get命令获取网页html
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:  # 状态为200即为爬取成功
        return response.text  # 返回值为html文档，传入到解析函数当中
    return None


def parse_one_page(html):
    """
    解析html内容并存入到文档result.txt中
    :param html: 抓取出的html内容
    """
    # 用正则表达式 match 实际的评论内容部分
    pattern = re.compile('<div class="c"( .*?)<\/div>', re.S)
    matched_all = re.findall(pattern, html)
    for matched in matched_all:
        # 用正则表达式 match 评论内容部分中的语句，存入result.txt
        # match 评论用户
        user_match = re.findall(re.compile('<a href="[a-zA-Z0-9:\/.]*">(.*?)<\/a>', re.S), matched)
        line = ""
        if len(user_match) == 1:
            line += user_match[0] + ': '
        # match 评论内容
        comment_match = re.findall(re.compile('<span class="ctt">(.*?)<\/span>', re.S), matched)
        if len(comment_match) == 1:
            line += comment_match[0] + ' '
        # match 评论时间
        time_match = re.findall(re.compile('<span class="ct">(.*?)&nbsp', re.S), matched)
        if len(time_match) == 1:
            line += time_match[0]
        print(line)
        with open('result.txt', 'a', encoding='utf-8') as fp:
            fp.writelines(str(line) + '\n')


if __name__ == '__main__':
    # 删除result.txt文件（如果存在）
    result_file = Path('result.txt')
    if result_file.is_file():
        os.remove('result.txt')

    # 默认 抓取30页 可以传入初始参数调整, 比如如果抓取100页就用：
    # python3 WeiboScraper.py 100
    page_scraped = 30 if len(sys.argv) != 2 else sys.argv[1]

    # 开始抓取
    for page in range(1, page_scraped):
        url = "https://weibo.cn/comment/J5UeFfDJC?&page=" + str(page)
        html = get_one_page(url)
        if html is None:
            print('爬取失败，内容为空！')
            break
        else:
            print('正在爬取第 %d 页评论' % page)
            parse_one_page(html)
            time.sleep(3)
