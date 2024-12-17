import tkinter as tk
from tkinter import filedialog
from cloud import stopwordslist, get_plt, _wordcloud
import re
import jieba
from collections import Counter
from test import *
def do_submit():
    output_text.delete('0.0', 'end')
    output = switcher.get(v.get(), prCNN)(input_text.get('0.0', 'end'))
    output_text.insert(tk.END, output)

def show_wordcloud():
    # 通过文件对话框选择文件
    filepath = filedialog.askopenfilename(title="选择CSV文件", filetypes=[("CSV Files", "*.csv")])
    if filepath:
        # 从文件中读取文本并进行处理
        words_str = ""
        with open(filepath, encoding='utf-8') as f:
            for line in f:
                line = re.sub(u"[0-9\s+.!/,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）＞＜-]+", "", line)
                if line == "": continue
                line = line.replace("\n", "")  # 去掉换行符
                seg_list = jieba.cut(line, cut_all=False)
                words_str += (" ".join(seg_list))

        stopwords = stopwordslist()
        words = [word for word in words_str.split(" ") if word not in stopwords and len(word) > 1]

        word_counts = Counter()  # 词频统计
        for x in words:
            word_counts[x] += 1

        # 生成词频统计图并显示
        get_plt(word_counts.most_common(30), "词频统计图top30")

        # 生成词云并显示
        _wordcloud(word_counts)  # 直接显示词云图

# 主窗口设置
root_window = tk.Tk()
root_window.title("实体信息抽取-情感分析-数据统计")
root_window.geometry("1280x800")
root_window['background'] = '#7FFFD4'

# 算法选择框设置
model = [('CNN', 1), ('LSTM', 2)]
switcher = {1: prCNN, 2: prLSTM}
v = tk.IntVar()
# 按钮水平排列
for i, (name, num) in enumerate(model):
    btn = tk.Radiobutton(root_window, text=name, variable=v, value=num, indicatoron=False)
    # 设置按钮水平排列，调整 relx 以分布在同一行
    btn.place(relx=0.05 + 0.3 * i, rely=0.1, relwidth=0.25, relheight=0.1)

# 识别按钮也放在同一行
submit = tk.Button(root_window, text='识别', command=do_submit)
submit.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.1)

# 选择文件并生成词云和词频统计图按钮
wordcloud_btn = tk.Button(root_window, text="生成词云和词频统计图", command=show_wordcloud)
wordcloud_btn.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)

# 输入文本框和输出文本框改到下方
# 输入文本框设置
input_title = tk.Label(root_window, text="输入文本", fg="#000000")
input_title.place(relx=0.1, rely=0.3)  # 调整位置
input_text = tk.Text(root_window, autoseparators=True)
input_text.place(relx=0.1, rely=0.35, relwidth=0.38, relheight=0.3)  # 调整位置

# 输出文本框
output_title = tk.Label(root_window, text="输出结果", fg="#000000")
output_title.place(relx=0.5, rely=0.3)  # 调整位置
output_text = tk.Text(root_window, autoseparators=True)
output_text.place(relx=0.5, rely=0.35, relwidth=0.38, relheight=0.3)  # 调整位置

root_window.mainloop()
