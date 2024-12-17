import os
import re
import PIL
import wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import jieba.analyse
from collections import Counter

plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords

def get_plt(data, title):
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    fig, ax = plt.subplots(figsize=(8, 6))  # 设置图形大小
    ax.barh(range(len(x)), y, color='gold')
    ax.set_yticks(range(len(x)))
    ax.set_yticklabels(x)
    plt.rcParams['font.sans-serif'] = [u'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title(title, fontsize=10)
    plt.ylabel("词")
    plt.xlabel("次数")
    plt.show()  # 显示图形
    return fig  # 返回绘制的图像对象

def _wordcloud(word_counts):  # 词云生成
    mask = np.array(PIL.Image.open(r'./backgroup.png'))
    wc = WordCloud(font_path='C:\\Windows\\Fonts\\simhei.ttf', max_words=2000, mask=mask, repeat=False, mode='RGBA')
    wc.generate_from_frequencies(word_counts)
    image_colors = wordcloud.ImageColorGenerator(mask)  # 文字颜色跟随背景图颜色
    wc.recolor(color_func=image_colors)
    wc.to_file("./wc_result.png")  # 保存结果为图片文件
    plt.imshow(wc)  # 显示词云
    plt.axis('off')
    plt.show()  # 显示词云
    return wc  # 返回生成的词云对象

def generate_wordcloud_from_file(file_path):  # 从文件中读取内容并生成词云
    words_str = ""
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = re.sub(u"[0-9\s+.!/,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）＞＜-]+", "", line)  # 去掉多余字符
            if line == "": continue
            line = line.replace("\n", "")  # 去掉换行符
            seg_list = jieba.cut(line, cut_all=False)
            words_str += (" ".join(seg_list))

    stopwords = stopwordslist()
    words = [word for word in words_str.split(" ") if word not in stopwords and len(word) > 1]

    word_counts = Counter()  # 词频统计
    for x in words:
        word_counts[x] += 1

    # 生成词频统计图
    fig = get_plt(word_counts.most_common(30), "词频统计top30")

    # 生成词云
    wc = _wordcloud(word_counts)

    return fig, wc  # 返回词频统计图和词云对象
