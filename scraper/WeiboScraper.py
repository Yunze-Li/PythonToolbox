import os
import re
import sys
import time
from pathlib import Path

import jieba
import pandas as pd
import requests
from wordcloud import WordCloud

RESULT_PATH = 'data/result.txt'
STOP_WORDS_PATH = 'data/stop_words.txt'
URLS_PATH = 'data/urls.txt'
WORD_CLOUD_PATH = 'data/word_cloud.png'
EXCEL_OUTPUT_PATH = 'data/result.xls'
FREQUENCY_OUTPUT_PATH = 'data/frequency.txt'

FONT_PATH = 'font/SimHei.ttf'

COMMENT_CONTENT_COLUMN = '评论内容'
COMMENT_TIME_COLUMN = '评论时间'
SHEET_NAME = '微博评论截取'

# 在这里改成你的Cookie
YOUR_COOKIE = 'SUB=_2A25yPn53DeRhGedI6VAV8SjEzTyIHXVRwQI_rDV6PUJbkdANLW2gkW1NV9FYfQFeyi1AnfnMjIvCSII9r_zlXr2Z; SUHB=0G0fB-QQPwe7EE; SCF=AlYHsXogIiV0HDS-PyxthZkqWFXTXE7uR8VqXQclcc-dhZSttJe3kNlqiV5MKnXDEnB-L_xzFmHx_UfxnMZDLm4.; _T_WM=1e7f68277ef7f3583600924a356ec041'
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


def cut_scraped_word(file_name: str):
    stop_words = []
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.strip())
    content = open(file_name, 'rb').read()
    # jieba 分词
    word_list = jieba.cut(content)
    words = []
    word_dict = {}
    for word in word_list:
        if word not in stop_words and is_all_chinese(word):
            words.append(word)
            if word in word_dict:
                word_dict[word] = word_dict[word] + 1
            else:
                word_dict[word] = 1
    # 统计词频，按高频到低频写入frequency.txt文件
    word_dict_sorted = {k: v for k, v in sorted(word_dict.items(), key=lambda item: item[1], reverse=True)}
    for key in word_dict_sorted.keys():
        with open(FREQUENCY_OUTPUT_PATH, 'a', encoding='utf-8') as fp:
            fp.writelines(f"{key}: {word_dict[key]}" + '\n')

    global word_cloud
    # 用逗号隔开词语
    word_cloud = '，'.join(words)


def is_all_chinese(word: str):
    for char in word:
        if not '\u4e00' <= char <= '\u9fa5':
            return False
    return True


def generate_word_cloud(generate_file_path: str):
    # 定义词云的一些属性
    wc = WordCloud(
        # 背景图分割颜色为白色
        background_color='white',
        # 统计搭配词设置关闭（避免重复关键词）
        collocations=False,
        # 显示最大词数
        max_words=300,
        # 显示中文
        font_path=FONT_PATH,
        # 最大尺寸
        max_font_size=100
    )
    global word_cloud
    # 词云函数
    x = wc.generate(word_cloud)
    # 生成词云图片
    image = x.to_image()
    # 展示词云图片
    image.show()
    # 保存词云图片
    wc.to_file(generate_file_path)


if __name__ == '__main__':
    # 删除result.txt文件，result.xls文件和frequency.txt文件（如果存在）
    result_file = Path(RESULT_PATH)
    if result_file.is_file():
        os.remove(RESULT_PATH)
    excel_result_file = Path(EXCEL_OUTPUT_PATH)
    if excel_result_file.is_file():
        os.remove(EXCEL_OUTPUT_PATH)
    frequency_file = Path(FREQUENCY_OUTPUT_PATH)
    if frequency_file.is_file():
        os.remove(FREQUENCY_OUTPUT_PATH)

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
    cut_scraped_word(RESULT_PATH)
    generate_word_cloud(WORD_CLOUD_PATH)
