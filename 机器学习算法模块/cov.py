# =============================================================================
# # -*- coding: utf-8 -*-
# =============================================================================
"""
Created on Fri Jun 18 15:11:44 2021

@author: hzzxq
"""

import os
import numpy as np
from pydub import AudioSegment
import wave
import struct
import pandas as pd
import tensorflow as tf
def load_mp3(filename):
    '''
    输入mp3文件的名，返回特征数据
    '''
    MP3_File = AudioSegment.from_mp3(file=filename)
    MP3_File.export('shiyan.wav', format="wav")#生成wave文件
    #wav文件读取
    '''
    nchannels:声道数,
    sampwidth：采样宽度,
    framerate：帧速率,
    nframes：帧的总量，
    '''
    f = wave.open('shiyan.wav','rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)#读取音频，字符串格式
    waveData = np.frombuffer(strData,dtype=np.int16)#将字符串转化为int
    waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
    temp_result = np.reshape(waveData,[nframes,nchannels])
    f.close()
    nframes=5000000
    result=temp_result[:nframes]
    outData = result#待写入wav的数据，这里仍然取waveData数据
    outData=np.expand_dims(outData,axis=0)
    outData = tf.cast(outData, dtype=tf.float32)
    return outData

def make_songs(result):
    test=np.array(result)
    nframes=5000000
    nchannels=2
    waveData=test[:nframes]
    outData = waveData
    outData = np.reshape(outData,[nframes*nchannels,1])
    outfile = 'outy.wav'
    outwave = wave.open(outfile, 'wb')#定义存储路径以及文件名
    sampwidth = 2
    fs = 44100
    data_size = len(outData)
    framerate = int(fs)
    nframes = data_size
    comptype = "NONE"
    compname = "not compressed"
    outwave.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))
    outData=outData
    for i in range(len(outData)):
        v=outData[i]
        outwave.writeframes(struct.pack('h', int(v * 64000 / 2)))#outData:16位，-32767~32767，注意不要溢出
    outwave.close()
    
filename = 'wang_final_musicInfo.csv'
frame = pd.DataFrame({'matrix':[],'tag':[]})
data = pd.read_csv(filename)
music_ids = data['歌曲id'].tolist()
for i in range(0,30):
    print(i)
    tmpstr = '王之歌曲存储/'+str(music_ids[i])+'.mp3'
    matrix = load_mp3(tmpstr)
#    matrix1 = np.random.random(size=[1,5000000,2])
    temp_frame = pd.DataFrame({'matrix':[matrix],'tag':[0]})
    frame = pd.concat([frame,temp_frame])
for i in range(5):
    matrix1 = np.random.random(size=[1,5000000,2])
    temp_frame = pd.DataFrame({'matrix':[matrix1],'tag':[1]})
    frame = pd.concat([frame,temp_frame])

np.save('frame2.npy',frame)
  
np.load('frame.npy',allow_pickle=True)





idlist = music_ids[0:30]
path = r'D:\notebook\金融智能\0618\王之歌曲存储30'
songs =list(set(os.listdir(path)))
for song in songs:
    song_id = song.split(".")[0]
    file_name = '王之歌曲存储30/'+str(song_id)+'.mp3'
    if int(song_id) not in idlist:
        print(file_name)
        os.remove(file_name)