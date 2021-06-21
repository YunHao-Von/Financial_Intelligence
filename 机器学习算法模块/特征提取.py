# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 16:40:24 2021

@author: hzzxq
"""

import librosa
import sklearn
import pandas as pd
def Music_Feature_Get(id,time):
    x , sr = librosa.load("所有歌曲/"+str(id)+".mp3", sr=8000,duration=time)
    zero_crossings = librosa.zero_crossings(x[0:len(x)], pad=False)
    zero_crossings=sum(zero_crossings)/len(x)#计算过0率,归一化版本
    spectral_centroids = sum(librosa.feature.spectral_centroid(x[:len(x)], sr=sr)[0])/len(x)#计算频谱平均中心值，越高代表声音音调越高昂
    spectral_rolloff = sum(librosa.feature.spectral_rolloff(x, sr=sr)[0])/len(x)#我也不知道该咋描述
    mfccs = librosa.feature.mfcc(x, sr=sr)
    mfccs=mfccs.mean(axis=1)#行
    result=list(mfccs)
    result.append(zero_crossings)
    result.append(spectral_rolloff)
    result.append(spectral_centroids)
    frame=pd.DataFrame({
        'id':[id],
        'mfccs0':[result[0]],
        'mfccs1':[result[1]],
        'mfccs2':[result[2]],
        'mfccs3':[result[3]],
        'mfccs4':[result[4]],
        'mfccs5':[result[5]],
        'mfccs6':[result[5]],
        'mfccs7':[result[7]],
        'mfccs8':[result[8]],
        'mfccs9':[result[9]],
        'mfccs10':[result[10]],
        'mfccs11':[result[11]],
        'mfccs12':[result[12]],
        'mfccs13':[result[13]],
        'mfccs14':[result[14]],
        'mfccs15':[result[15]],
        'mfccs16':[result[16]],
        'mfccs17':[result[17]],
        'mfccs18':[result[18]],
        'mfccs19':[result[19]],
        'zero_crossings':[zero_crossings],
        'spectral_centroids':[spectral_centroids],
        'spectral_rolloff':[spectral_rolloff]
    })
    return frame

#frame1=pd.DataFrame({
#            'id':[0],
#            'mfccs0':[0],
#            'mfccs1':[0],
#            'mfccs2':[0],
#            'mfccs3':[0],
#            'mfccs4':[0],
#            'mfccs5':[0],
#            'mfccs6':[0],
#            'mfccs7':[0],
#            'mfccs8':[0],
#            'mfccs9':[0],
#            'mfccs10':[0],
#            'mfccs11':[0],
#            'mfccs12':[0],
#            'mfccs13':[0],
#            'mfccs14':[0],
#            'mfccs15':[0],
#            'mfccs16':[0],
#            'mfccs17':[0],
#            'mfccs18':[0],
#            'mfccs19':[0],
#            'zero_crossings':[0],
#            'spectral_centroids':[0],
#            'spectral_rolloff':[0]
#        })
#frame1.to_csv('mfcc.csv',index=None)

filename_final = 'dai_final_musicInfo.csv'  
data = pd.read_csv(filename_final, encoding='utf-8')
startnum = 2396
count = startnum
for id in data['歌曲id'][startnum:]:
    count += 1
    frame = Music_Feature_Get(id,120)
    frame.to_csv('mfcc.csv', mode='a', header=False, index=None)
    print(count)
data2 = pd.read_csv('mfcc.csv', encoding='utf-8')
