# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 18:22:26 2021

@author: hzzxq
"""

import pandas as pd
import numpy as np
import get_userId
music_simi_matrix=np.load('music_simi_matrix.npy')
music_data_list=np.load('music_data_list.npy')
user_music_list=np.load('user_music_list.npy',allow_pickle=True)




#def commend(nickname):
#    music_commend_list = []
#    uid = get_userId.User_api().search(nickname)['result']['userprofiles'][0]['userId']
#    if uid in userId_list:
#        song_list = 
#        for i in userId_list:
#    else:
commend_list = []
i = 0
for user in user_music_list:
    songs = user[1]
    tmplist = []
    print(i)
    i += 1
    for song in songs:
        song_id = song[0]
        idxs = np.where(music_data_list[:,0]==song_id)
        if len(idxs[0]) == 1:
            idx = idxs[0][0]
            tmplist.append(music_data_list[music_simi_matrix[idx,:].argmin()][0].astype(int))
    commend_list.append([user[0],tmplist])       
      
np.save('commend_list.npy',commend_list)
    

"""
daixxzz
"""
num_k = 3
song_ids = np.load('allsongs_id2.npy')
commend_list_dai = []
tmplist = []
distance = []
for song_id in song_ids:
        idxs = np.where(music_data_list[:,0]==song_id)
        if len(idxs[0]) == 1:
            idx = idxs[0][0]
            tmplist.append([music_data_list[music_simi_matrix[idx,:].argmin()][0].astype(int),music_simi_matrix[idx,:].min()])
tmplist0 = np.array(tmplist)
idex=np.lexsort([tmplist0[:,1]])
sorted_tmplist = tmplist0[idex, :]
count = 0
for i in sorted_tmplist:
    if i[0].astype(int) not in song_ids:
        commend_list_dai.append(i[0].astype(int))
        count += 1
    if count==num_k:
        break
    
        

tmplist1 = list(set(tmplist)-set(song_ids))
from collections import Counter   #引入Counter
tmplist2 = dict(Counter(tmplist1))
commend_list_dai = [key for key,value in tmplist2.items()if value > 1]
np.save('commend_list_dai.npy',commend_list_dai)



#a = np.load('commend_list.npy',allow_pickle=True)
#commend_list = pd.DataFrame({'userId':a[1:,0],'commend_list':a[1:,1]})
#commend_list.to_csv('commend_list.csv',index=None)



    