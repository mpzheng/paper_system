import pandas as pd
from matplotlib.font_manager import FontProperties
import pandas as pd
import math
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
import matplotlib.pyplot as plt
import numpy as np

def plot_scale(lz,name,id_score):
    '''
    某个粒子的n个组的直方图
    :param lz: 某个粒子
            name:算法名称
            id_score:学号对应的绩点列表
    :return:
    '''
    col = math.ceil(len(lz)/2)
    # fig, axes = plt.subplots(2, 3, figsize=(20, 10))
    fig, axes = plt.subplots(2, col, figsize=(20, 15))
    for index, id_group in enumerate(lz):
        group_score = []
        for id_ in id_group[1]:
            group_score.append(id_score[id_])
        group_score = pd.Series(group_score)
        axes[int(index / col)][index % col].hist(group_score, bins=[1, 1.5, 2, 2.5, 3, 3.5, 4],density=True)
        # axes[int(index / 2)][index % 2].hist(group_score, bins=[0, 2, 2.5, 2, 2.5, 4],density=True)
        # title = "第" + str(index) + "组"
        axes[int(index / col)][index % col].set_title(u"第"+str(index+1)+u"组",fontproperties=font_set)
        axes[int(index / col)][index % col].set_xlabel(u"绩点区间",fontproperties=font_set)
        axes[int(index / col)][index % col].set_ylabel(u"频率/间距",fontproperties=font_set)

        plt.savefig("figure/"+name + "_distribution.jpg")
        plt.savefig("figure/"+name + "_distribution.svg",format="svg")
        # plt.savefig("static/image/"+"DE"+ i + "315.jpg")

        # plt.savefig("static/image/" + i + "_315.svg",format="svg")

def plot_fitness(y,name):
    '''
    x:迭代轮次
    y：适应度
    :param y: 纵坐标
    :param xlabel: 名称
    :param ylabel:
    :param legendName: 图例
    :param name: 算法名称
    :return:
    '''
    # mn = min(y)
    # mx = max(y)


    plt.figure()
    plt.xlabel("IterNum")
    plt.ylabel("Fitness")
    # plt.ylim(mn,mx)
    plt.ylim(0.85,1)
    plt.plot(y,label=name)
    plt.legend()
    # plt.show()
    plt.savefig("figure/"+name+"_"+"Fitness"+".jpg")

def plot_diversity(y,name):
    '''
    多样性图
    横坐标：轮次
    纵坐标 ：多样性
    :param y: 纵坐标
    :param xlabel: 名称
    :param ylabel:
    :param legendName: 图例
    :param name: 算法名称
    :return:
    '''
    # mn = min(y)
    # mx = max(y)


    plt.figure()
    plt.xlabel("IterNum")
    plt.ylabel("Diversity")
    # plt.ylim(mn,mx)
    # plt.ylim(0.85,1)
    plt.plot(y,label=name)
    plt.legend()
    # plt.show()
    plt.savefig("figure/"+name+"_"+"Diversity"+".jpg")
# d = [ 0,0.9371206986266329, 0.9371206986266329, 0.9371206986266329, 0.9371206986266329, 0.9371206986266329, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9511694798736501, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9512159982292654, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9535007873517451, 0.9585357155153396, 0.9585357155153396, 0.9585357155153396, 0.9585357155153396, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794, 0.9612422307033794]
# plot_iter(d,"DE")