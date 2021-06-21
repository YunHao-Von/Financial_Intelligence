# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 19:23:29 2021

@author: hzzxq
"""

import pandas as pd
import numpy as np
data1 = pd.read_csv('data1.csv', encoding='utf-8')[1:].iloc[:,0:21]
data2 = pd.read_csv('data2.csv', encoding='utf-8')[1:].iloc[:,0:21]
data3 = pd.read_csv('data3.csv', encoding='utf-8')[1:].iloc[:,0:21]
data = pd.concat([data1,data2,data3],axis=0)
data.drop_duplicates(subset='id',keep='first',inplace=True)
#a=pd.read_csv('data.csv', encoding='utf-8')[1:].values   a[0][0:1]和a[0:1][0:1]不一样
max_data = data.iloc[:,1:].max()
min_data = data.iloc[:,1:].min()
nmlz_data = ((data.iloc[:,1:]-min_data)/(max_data-min_data))
n = len(data)
result_matrix = np.ones((n,n))*20
for i in range(0,n):
    A = np.array(nmlz_data.iloc[i])
    print(i)
    for j in range(i+1,n):
        B = np.array(nmlz_data.iloc[j]) 
        tmp = np.linalg.norm(A-B)
        result_matrix[i][j] = tmp
        result_matrix[j][i] = tmp
np.save('music_simi_matrix.npy',result_matrix)
np.save('music_data_list.npy',data)



