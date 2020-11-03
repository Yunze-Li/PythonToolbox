import jieba
from wordcloud import WordCloud

from scraper.constants import FONT_PATH, STOP_WORDS_PATH


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
    for word in word_list:
        if word not in stop_words and is_all_chinese(word):
            words.append(word)
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
