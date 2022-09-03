import os
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt

from math import pi
from matplotlib.pylab import style
from utils.utils import label_s2t
# 需要对中文进行处理
style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False


# def plot_heatmap(hyp, keywords, scoress, file_path):
#     file_name = file_path.split('\\')[-1].replace('.txt', '')
#     fig = plt.figure(figsize=(25, 10), dpi=300)
#     #定义画布为1*1个划分，并在第1个位置上进行作图
#     ax = fig.add_subplot(111)
#     #作图并选择热图的颜色填充风格，这里选择hot
#     sns.heatmap(scoress, linewidths = 0.05, ax = ax, cmap=plt.cm.hot_r)

#     #定义横纵坐标的刻度
#     areas = hyp['areas']
#     keywords, areas = label_s2t(keywords, areas)
    
#     ax.set_yticks(np.arange(len(areas)) + 0.5)
#     plt.yticks(rotation=0)
#     ax.set_yticklabels(areas, size = 18)
#     ax.set_xticks(np.arange(len(keywords[:, 0].flatten().tolist())) + 0.5)
#     ax.set_xticklabels(keywords[:, 0].flatten().tolist(), size = 18)
#     plt.xticks(rotation=45)
#     ax.set_ylabel('研究領域')
#     ax.set_xlabel('關鍵詞')
    
#     save_dir = os.path.join(hyp["save_img_dir"], 'heatmap')
#     if not os.path.isdir(save_dir):
#         os.makedirs(save_dir)
#     plt.savefig(f'{save_dir}/{file_name}.png')
#     fig.clear()
#     plt.close(fig)
#     return

def plot_radar(hyp, keywords, scoress, file_path):
    file_name = file_path.split('\\')[-1].replace('.txt', '')
    save_dir = file_path.replace('data', 'output\\img').replace(file_path.split('\\')[-1], '')
    
    areas = hyp['areas']
    keywords, areas = label_s2t(keywords, areas)
    tt_scoress = scoress.sum(axis=1).tolist()

    # 变量类别个数
    N = len(areas)

    # plot the first line of the data frame.
    # 绘制数据的第一行
    # 将第一个值放到最后，以封闭图形
    tt_scoress += tt_scoress[:1]
    print(tt_scoress)

    # 设置每个点的角度值
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    # 初始化极坐标网格
    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    # 设置x轴的标签
    plt.xticks(angles[:-1], areas, color='grey', size=8)

    # Draw ylabels
    # 设置标签显示位置
    # 具体见https://www.bbsmax.com/A/x9J2DRwNd6/
    ax.set_rlabel_position(0)
    # 设置y轴的标签
    plt.yticks([5, 10, 15], ["5", "10", "15"], color="grey", size=7)
    plt.ylim(0, 15)

    # Plot data
    # 画图
    ax.plot(angles, tt_scoress, linewidth=1, linestyle='solid')

    # Fill area
    # 填充区域
    ax.fill(angles, tt_scoress, 'b', alpha=0.1)

    save_dir = os.path.join(save_dir, 'radar')
    
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    plt.savefig(f'{save_dir}/{file_name}.png')
    plt.clf()