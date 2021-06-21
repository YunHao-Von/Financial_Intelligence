# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 20:31:54 2021

@author: hzzxq
"""

import pandas as pd
import numpy as np
import os
path = r'D:\notebook\金融智能\歌单存储'
users =list(set(os.listdir(path)))
users.sort() #排序
user_music_list = []
i = 0
for user in users:
    tr = '\\'   #多增加一个斜杠
    path0 = path + tr + user
    files =list(set(os.listdir(path0)))
    files.sort() #排序
    tmplist = []
    print(i)
    i += 1
    for j in files:
        tmppath = path0 + tr + j
        tmplist.extend(pd.read_csv(tmppath, encoding='utf-8').values)
    user_music_list.append([user,tmplist])
np.save('user_music_list.npy',user_music_list)
#    user_music_list.append(filename)