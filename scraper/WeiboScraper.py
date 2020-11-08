import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from scraper import WordCloudGenerator
from scraper.constants import COMMENT_CONTENT_COLUMN
from scraper.constants import COMMENT_TIME_COLUMN
from scraper.constants import EXCEL_OUTPUT_PATH
from scraper.constants import RESULT_PATH
from scraper.constants import SHEET_NAME
from scraper.constants import WORD_CLOUD_PATH
from scraper.constants import YOUR_COOKIE

writer = pd.ExcelWriter(EXCEL_OUTPUT_PATH, engine='xlsxwriter')


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


def parse_one_page(html, result_dict):
    """
    解析html内容并存入到文档result.txt中
    :param result_dict: dictionary of scraped results
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
            if matched_comment[0].startswith("回复") and len(
                    re.findall(re.compile('<\/a>:(.*?)<\/span>', re.S), matched_comment[0])) > 0:
                matched_comment_content = re.findall(re.compile('<\/a>:(.*?)<\/span>', re.S), matched_comment[0])[0]
            matched_comment_content_chinese = re.findall(re.compile('([^\x00-\xff]+)', re.S), matched_comment_content)
            for content in matched_comment_content_chinese:
                line += content + ' '
        result_dict[COMMENT_CONTENT_COLUMN].append(line)
        # match 评论时间
        matched_comment_time = re.findall(re.compile('<span class=\"ct\">(.*?)(&nbsp|<\/span>)', re.S), matched)
        if len(matched_comment_time) == 1:
            line += matched_comment_time[0][0]
            result_dict[COMMENT_TIME_COLUMN].append(matched_comment_time[0][0])
        else:
            result_dict[COMMENT_TIME_COLUMN].append("")
        print(line)

        # 写入result.txt 为制作词云做准备
        with open(RESULT_PATH, 'a', encoding='utf-8') as fp:
            fp.writelines(str(line) + '\n')


if __name__ == '__main__':
    # 删除result.txt文件和result.xls文件（如果存在）
    result_file = Path(RESULT_PATH)
    if result_file.is_file():
        os.remove(RESULT_PATH)
    excel_result_file = Path(EXCEL_OUTPUT_PATH)
    if excel_result_file.is_file():
        os.remove(EXCEL_OUTPUT_PATH)

    # 从urls.txt读取网址信息
    urls_file = open('data/urls.txt', 'r')
    urls = urls_file.readlines()

    # 默认 抓取30页 可以传入初始参数调整, 比如如果抓取100页就用：
    # python3 WeiboScraper.py 100
    page_scraped = 30 if len(sys.argv) != 2 else int(sys.argv[1])

    # 开始抓取
    result_dict = {COMMENT_CONTENT_COLUMN: [], COMMENT_TIME_COLUMN: []}
    for base_url in urls:
        for page in range(1, page_scraped):
            url = base_url.strip("\n") + str(page)
            html = get_one_page(url)
            if html is None:
                print('爬取失败，内容为空！')
                break
            else:
                print('正在爬取第 %d 页评论' % page)
                parse_one_page(html, result_dict)
                time.sleep(3)

    # result_dict的结果写入result.xls表格
    result_data_frame = pd.DataFrame.from_dict(result_dict)
    result_data_frame.to_excel(writer, sheet_name=SHEET_NAME, index=False)
    writer.save()

    # 生成词云，传入数据所在txt文件
    WordCloudGenerator.cut_scraped_word(RESULT_PATH)
    WordCloudGenerator.generate_word_cloud(WORD_CLOUD_PATH)
