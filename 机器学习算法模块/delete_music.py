# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 17:22:05 2021

@author: hzzxq
"""

import pandas as pd
import librosa
data = pd.read_csv('代2.csv', encoding='utf-8')
path = r'D:\notebook\金融智能\daixxzz\所有歌曲'
songs =list(set(os.listdir(path)))
songs0 = []
time = []
file_size = 1024*1024  #更改成你想删除的界限，我这里是100kb
i = 0
for song in songs:
    song_id = song.split(".")[0]
    file_name = '所有歌曲/'+str(song_id)+'.mp3'
    if int(song_id) in list(data['歌曲id']):
        songs0.append(int(song_id))
        print(i)
        i += 1
#        size = os.path.getsize(file_name)
#        if size < file_size:
#            print('remove',size,file_name)
#            os.remove(file_name)
#        else:
#            songs0.append(int(song_id))
#            time.append(librosa.get_duration(filename=file_name))
    else:
        os.remove(file_name)
        print('remove',file_name)
        

for i in data['歌曲id']:
    if i not in songs0:
        idx = data['歌曲id'][data['歌曲id']==i].index.tolist()
        data.drop(index = idx,inplace = True)
        
data = data.drop_duplicates(subset=['歌曲id'],keep='first')
data.to_csv('daixxzz_歌曲基本信息.csv',header=True, index=None)
data2 = pd.read_csv('daixxzz_歌曲基本信息.csv', encoding='utf-8')


def delete_nanlyric(filename,filename_final,music_filename):
    data = pd.read_csv(filename, encoding='utf-8')
    for i in range(len(data)):
        if str(data['歌曲歌词'][i]) == 'nan':
            file_name = music_filename + str(data['歌曲id'][i]) + '.mp3'
            os.remove(file_name)
            data.drop([i],inplace = True)
        if i%100 == 0:
            print(i)
    data.to_csv(filename_final,header=True, index=None)
 
filename = 'daixxzz_歌曲基本信息.csv'#剔除歌词为空的数据
filename_final = 'dai_final_musicInfo.csv'
music_filename = "所有歌曲/"
delete_nanlyric(filename,filename_final,music_filename)
data3 = pd.read_csv('dai_final_musicInfo.csv', encoding='utf-8')


#from collections import Counter   #引入Counter
#a = data['歌曲id']
#b = dict(Counter(a))
#print ([key for key,value in b.items()if value > 1])  #只展示重复元素