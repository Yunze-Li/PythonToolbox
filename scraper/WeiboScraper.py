import re
import sys
import time

import requests

from scraper import WordCloudGenerator
from scraper.constants import RESULT_PATH, WORD_CLOUD_PATH, YOUR_COOKIE


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
        'Cookie': YOUR_COOKIE
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
        line = ""
        matched_comment = re.findall(re.compile('<span class=\"ctt\">(.*?<\/span>)', re.S), matched)
        if len(matched_comment) == 1:
            matched_comment_content = matched_comment[0]
            if matched_comment[0].startswith("回复"):
                matched_comment_content = re.findall(re.compile('<\/a>:(.*?)<\/span>', re.S), matched_comment[0])[0]
            matched_comment_content_chinese = re.findall(re.compile('([^\x00-\xff]+)', re.S), matched_comment_content)
            for content in matched_comment_content_chinese:
                line += content + ' '
        # match 评论时间
        matched_comment_time = re.findall(re.compile('<span class=\"ct\">(.*?)(&nbsp|<\/span>)', re.S), matched)
        if len(matched_comment_time) == 1:
            line += matched_comment_time[0][0]
        print(line)
        with open(RESULT_PATH, 'a', encoding='utf-8') as fp:
            fp.writelines(str(line) + '\n')


if __name__ == '__main__':
    # 从urls.txt读取网址信息
    urls_file = open('data/urls.txt', 'r')
    urls = urls_file.readlines()

    # 默认 抓取30页 可以传入初始参数调整, 比如如果抓取100页就用：
    # python3 WeiboScraper.py 100
    page_scraped = 30 if len(sys.argv) != 2 else int(sys.argv[1])

    # 开始抓取
    for base_url in urls:
        for page in range(1, page_scraped):
            url = base_url.strip("\n") + str(page)
            html = get_one_page(url)
            if html is None:
                print('爬取失败，内容为空！')
                break
            else:
                print('正在爬取第 %d 页评论' % page)
                parse_one_page(html)
                time.sleep(3)

    # 生成词云，传入数据所在txt文件
    WordCloudGenerator.cut_scraped_word(RESULT_PATH)
    WordCloudGenerator.generate_word_cloud(WORD_CLOUD_PATH)
