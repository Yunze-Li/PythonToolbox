import os
from pathlib import Path

import jieba
from wordcloud import WordCloud

RESULT_PATH = 'data/result.txt'
STOP_WORDS_PATH = 'data/stop_words.txt'
WORD_CLOUD_PATH = 'data/word_cloud.png'
FREQUENCY_OUTPUT_PATH = 'data/frequency.txt'

FONT_PATH = 'font/SimHei.ttf'


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
    # 删frequency.txt文件（如果存在）
    frequency_file = Path(FREQUENCY_OUTPUT_PATH)
    if frequency_file.is_file():
        os.remove(FREQUENCY_OUTPUT_PATH)

    # 生成词云，传入数据所在txt文件
    cut_scraped_word(RESULT_PATH)
    generate_word_cloud(WORD_CLOUD_PATH)
