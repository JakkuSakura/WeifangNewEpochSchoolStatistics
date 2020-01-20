from threading import Lock
from threading import Thread
import threading
from matplotlib import font_manager as fm, rcParams
import os
import exam
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
plt.rcParams['font.sans-serif'] = ['FangSong']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fm._rebuild()

mutex = Lock()


def draw_pic(name):
    if os.path.exists('temp/' + name + '.png'):
        print('used cached ', 'temp/' + name + '.png')
        return
    with mutex:
        for e in exam.tests.values():
            try:
                selected = exam.get_selected(e.loc[name])
                break
            except:
                pass
        else:
            print('not found', name)
            return

        fig, ax = plt.subplots()
        ax.set(xlabel='考试', ylabel='成绩', title="各科考试成绩")

        for subject in selected:
            if '总分' != subject:
                yList = []
                xList = []
                for exam_name in exam.tests_names:
                    try:
                        yList.append(exam.tests[exam_name].loc[name, subject])
                        xList.append(exam_name)
                    except:
                        pass
                        
                
                plt.plot(xList, yList, 'o-', label=subject)
                for x, y in zip(xList, yList):
                        plt.text(x, y+0.3, '%.0f' %
                                y, ha='center', va='bottom', fontsize=10.5)
                
        plt.grid()
        plt.legend()
        print('drew ', 'temp/' + name + '.png')
        fig.savefig('temp/' + name + '.png')        
    

def draw_pic_ranking(name):
    if os.path.exists('temp/' + name + '_ranking.png'):
        print('used cached', 'temp/' + name + '_ranking.png')
        return
    with mutex:
        for e in exam.tests.values():
            try:
                selected = exam.get_selected(e.loc[name])
                break
            except:
                pass
        else:
            print('not found', name)
            return

        fig, ax = plt.subplots()
        ax.set(xlabel='考试', ylabel='排名', title="各科考试排名")

        for subject in selected:
            if '总分' != subject:
                yList = []
                xList = []
                for exam_name in exam.tests_names:
                    try:
                        yList.append(exam.tests[exam_name].loc[name, subject+'排名'])
                        xList.append(exam_name)
                    except:
                        pass
                plt.plot(xList, yList, 'o-', label=subject)
                for x, y in zip(xList, yList):
                    plt.text(x, y+0.3, '%.0f' %
                            y, ha='center', va='bottom', fontsize=10.5)
        ax.invert_yaxis()
        plt.grid()
        plt.legend()
        print('drew', 'temp/' + name + '_ranking.png')
        fig.savefig('temp/' + name + '_ranking.png')



if __name__ == '__main__':
    draw_pic_ranking('邱江坤')
    plt.show()
