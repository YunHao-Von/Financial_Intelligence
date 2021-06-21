# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 14:46:37 2021

@author: hzzxq
"""

import requests
import json
import re
def get_lyric(id):
    '''
    :param
     id:输入指定歌曲的音乐id
    :return:
    返回当前歌曲的歌词
    '''
    headers = {
        "user-agent" : "Mozilla/5.0",
        "Referer" : "http://music.163.com",
        "Host" : "music.163.com"
    }
    url='http://localhost:3000/lyric?id='+str(id)
    temp=requests.get(url,headers=headers,timeout=5)
    temp=json.loads(temp.text)
    a=temp['lrc']['lyric']
    lyric = re.sub(r'[\d:.[\]]','', a)
    lyric=lyric.replace('\n', '').replace('\r', '').strip().replace(' ', '')
    lyric=re.sub('[^\u4e00-\u9fa5]+','',lyric)
    return lyric

import pandas as pd
def get_lyric_with_csv(filename):
    '''
    :param
    filename:文件名
    :return:
    自动生成带歌词的文件
    '''
    temp_data=pd.read_csv(filename)
    temp_music_ids=temp_data['歌曲id'].tolist()
    lyric=[]
    for i in range(len(temp_music_ids)):
        try:
            temp_lyric=get_lyric(str(temp_music_ids[i]))
            lyric.append(temp_lyric)
        except:
            temp_data.drop([i],inplace = True)
        if i%100 == 0:
            print(i)
    temp_data['歌曲歌词']=lyric
    return temp_data

a=get_lyric_with_csv('代.csv')
a.to_csv('代2.csv',header=True, index=None)
a = pd.read_csv('代2.csv', encoding='utf-8')
a = a.drop_duplicates(subset=['歌曲id'],keep='first')
temp_music_ids = np.load('allsongs_id2.npy')


"""
提取歌词库的歌词
"""
temp_data=pd.read_csv('data3.csv')[1:]
temp_music_ids=temp_data['id'].tolist()
lyric=[]
for i in range(len(temp_music_ids)):
    try:
        temp_lyric=get_lyric(str(temp_music_ids[i]))
        if str(temp_lyric) != 'nan' & str(temp_lyric) != 'NaN':
            lyric.append(temp_lyric)
        else:
            temp_data.drop([i+1],inplace = True)
            print('nan:',i)
    except:
        temp_data.drop([i+1],inplace = True)
        print('except',i)
    if i%100 == 0:
        print(i)
temp_data['歌曲歌词']=lyric
temp_data.to_csv('rep_mfcc_lyric.csv',header=True, index=None)

temp_data = pd.read_csv('rep_mfcc_lyric.csv')
for i in range(len(temp_data)):
    if str(temp_data['歌曲歌词'][i]) == 'nan':
        print(i)
        temp_data.drop([i],inplace = True)
temp_data.to_csv('rep_mfcc_lyric.csv',header=True, index=None)
