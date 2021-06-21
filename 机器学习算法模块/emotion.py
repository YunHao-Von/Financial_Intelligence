# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 21:49:39 2021

@author: hzzxq
"""

# coding:utf-8
import jieba
import numpy as np
import pandas as pd
 
 
#打开词典文件，返回列表
def open_dict(Dict = 'hahah', path=r'data/Textming'):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r', encoding='utf-8')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict
 
 
 
def judgeodd(num):
    if (num % 2) == 0:
        return 'even'
    else:
        return 'odd'
 


 
 
def sentiment_score_list(dataset):
    seg_sentence = dataset.split('。')
 
    count1 = []
    count2 = []
    for sen in seg_sentence: #循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=False)  #把句子进行分词，以列表的形式返回
        i = 0 #记录扫描到的词的位置
        a = 0 #记录情感词的位置
        poscount = 0 #积极词的第一次分值
        poscount2 = 0 #积极词反转后的分值
        poscount3 = 0 #积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化
 
            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in degree_word:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '！' or word == '!':  ##判断句子是否有感叹号
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1 # 扫描词位置前移
 
 
            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3
 
            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []
 
    return count2
 
def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        AvgPos = np.mean(score_array[:, 0])
        AvgPos = float('%.1f'%AvgPos)
        AvgNeg = np.mean(score_array[:, 1])
        AvgNeg = float('%.1f'%AvgNeg)
        StdPos = np.std(score_array[:, 0])
        StdPos = float('%.1f'%StdPos)
        StdNeg = np.std(score_array[:, 1])
        StdNeg = float('%.1f'%StdNeg)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]) #积极、消极情感值总和(最重要)，积极、消极情感均值，积极、消极情感方差。
    return score
 
def EmotionByScore(data):
    result_list=sentiment_score(sentiment_score_list(data))
    return result_list[0][0],result_list[0][1]
    
 
 
def JudgingEmotionByScore(Pos, Neg):
    if Pos > Neg:
        str='1'
    elif Pos < Neg:
        str='-1'
    elif Pos == Neg:
        str='0'
    return str
 
#注意，这里你要修改path路径。
deny_word = open_dict(Dict = '否定词', path= r'D:/notebook/金融智能/语料库/')
posdict = open_dict(Dict = 'positive', path= r'D:/notebook/金融智能/语料库/')
negdict = open_dict(Dict = 'negative', path= r'D:/notebook/金融智能/语料库/')
 
degree_word = open_dict(Dict = '程度级别词语', path= r'D:/notebook/金融智能/语料库/')
mostdict = degree_word[degree_word.index('extreme')+1 : degree_word.index('very')]#权重4，即在情感词前乘以4
verydict = degree_word[degree_word.index('very')+1 : degree_word.index('more')]#权重3
moredict = degree_word[degree_word.index('more')+1 : degree_word.index('ish')]#权重2
ishdict = degree_word[degree_word.index('ish')+1 : degree_word.index('last')]#权重0.5 




#songids = list(data1['歌曲id'][:])
#for i in data2['id']:
#    if i not in songids:
#        idx = data2['id'][data2['id']==i].index.tolist()
#        data2.drop(index = idx,inplace = True)
def emotion(data1,data2,outfilename):
    frame=pd.DataFrame({
        'id':[],
        'mfccs0':[],
        'mfccs1':[],
        'mfccs2':[],
        'mfccs3':[],
        'mfccs4':[],
        'mfccs5':[],
        'mfccs6':[],
        'mfccs7':[],
        'mfccs8':[],
        'mfccs9':[],
        'mfccs10':[],
        'mfccs11':[],
        'mfccs12':[],
        'mfccs13':[],
        'mfccs14':[],
        'mfccs15':[],
        'mfccs16':[],
        'mfccs17':[],
        'mfccs18':[],
        'mfccs19':[],
        'zero_crossings':[],
        'spectral_centroids':[],
        'spectral_rolloff':[],
        'pos_sum':[],
        'neg_sum':[],
        'pos_mean':[],
        'neg_mean':[],
        'pos_var':[],
        'neg_var':[]
    })
    for i in range(len(data1)):
        id = data1['歌曲id'][i]
        lyric = data1['歌曲歌词'][i]
        tmp_matrix = sentiment_score(sentiment_score_list(lyric))
        idx = data2['id'][data2['id']==id].index.tolist()[0]
        data2.iloc[idx,]
        tmpframe = pd.DataFrame({
            'id':[id],
            'mfccs0':[data2.iloc[idx,1]],
            'mfccs1':[data2.iloc[idx,2]],
            'mfccs2':[data2.iloc[idx,3]],
            'mfccs3':[data2.iloc[idx,4]],
            'mfccs4':[data2.iloc[idx,5]],
            'mfccs5':[data2.iloc[idx,6]],
            'mfccs6':[data2.iloc[idx,7]],
            'mfccs7':[data2.iloc[idx,8]],
            'mfccs8':[data2.iloc[idx,9]],
            'mfccs9':[data2.iloc[idx,10]],
            'mfccs10':[data2.iloc[idx,11]],
            'mfccs11':[data2.iloc[idx,12]],
            'mfccs12':[data2.iloc[idx,13]],
            'mfccs13':[data2.iloc[idx,14]],
            'mfccs14':[data2.iloc[idx,15]],
            'mfccs15':[data2.iloc[idx,16]],
            'mfccs16':[data2.iloc[idx,17]],
            'mfccs17':[data2.iloc[idx,18]],
            'mfccs18':[data2.iloc[idx,19]],
            'mfccs19':[data2.iloc[idx,20]],
            'zero_crossings':[data2.iloc[idx,21]],
            'spectral_centroids':[data2.iloc[idx,22]],
            'spectral_rolloff':[data2.iloc[idx,23]],
            'pos_sum':[tmp_matrix[0][0]],
            'neg_sum':[tmp_matrix[0][1]],
            'pos_mean':[tmp_matrix[0][2]],
            'neg_mean':[tmp_matrix[0][3]],
            'pos_var':[tmp_matrix[0][4]],
            'neg_var':[tmp_matrix[0][5]]
        })
        frame = pd.concat([frame,tmpframe])
    frame.to_csv(outfilename,header=True, index=None)
def emotion2(data1,data2,outfilename):
    frame=pd.DataFrame({
        'id':[],
        'mfccs0':[],
        'mfccs1':[],
        'mfccs2':[],
        'mfccs3':[],
        'mfccs4':[],
        'mfccs5':[],
        'mfccs6':[],
        'mfccs7':[],
        'mfccs8':[],
        'mfccs9':[],
        'mfccs10':[],
        'mfccs11':[],
        'mfccs12':[],
        'mfccs13':[],
        'mfccs14':[],
        'mfccs15':[],
        'mfccs16':[],
        'mfccs17':[],
        'mfccs18':[],
        'mfccs19':[],
        'zero_crossings':[],
        'spectral_centroids':[],
        'spectral_rolloff':[],
        'pos_sum':[],
        'neg_sum':[],
        'pos_mean':[],
        'neg_mean':[],
        'pos_var':[],
        'neg_var':[]
    })
    for i in range(len(data1)):
        id = data1['id'][i]
        lyric = data1['歌曲歌词'][i]
        tmp_matrix = sentiment_score(sentiment_score_list(lyric))
        idx = data2['id'][data2['id']==id].index.tolist()[0]
        data2.iloc[idx,]
        tmpframe = pd.DataFrame({
            'id':[id],
            'mfccs0':[data2.iloc[idx,1]],
            'mfccs1':[data2.iloc[idx,2]],
            'mfccs2':[data2.iloc[idx,3]],
            'mfccs3':[data2.iloc[idx,4]],
            'mfccs4':[data2.iloc[idx,5]],
            'mfccs5':[data2.iloc[idx,6]],
            'mfccs6':[data2.iloc[idx,7]],
            'mfccs7':[data2.iloc[idx,8]],
            'mfccs8':[data2.iloc[idx,9]],
            'mfccs9':[data2.iloc[idx,10]],
            'mfccs10':[data2.iloc[idx,11]],
            'mfccs11':[data2.iloc[idx,12]],
            'mfccs12':[data2.iloc[idx,13]],
            'mfccs13':[data2.iloc[idx,14]],
            'mfccs14':[data2.iloc[idx,15]],
            'mfccs15':[data2.iloc[idx,16]],
            'mfccs16':[data2.iloc[idx,17]],
            'mfccs17':[data2.iloc[idx,18]],
            'mfccs18':[data2.iloc[idx,19]],
            'mfccs19':[data2.iloc[idx,20]],
            'zero_crossings':[data2.iloc[idx,21]],
            'spectral_centroids':[data2.iloc[idx,22]],
            'spectral_rolloff':[data2.iloc[idx,23]],
            'pos_sum':[tmp_matrix[0][0]],
            'neg_sum':[tmp_matrix[0][1]],
            'pos_mean':[tmp_matrix[0][2]],
            'neg_mean':[tmp_matrix[0][3]],
            'pos_var':[tmp_matrix[0][4]],
            'neg_var':[tmp_matrix[0][5]]
        })
        frame = pd.concat([frame,tmpframe])
    frame.to_csv(outfilename,header=True, index=None)

""""""
filename1 = 'wang_final_musicInfo.csv'
filename2 = 'wang_mfcc.csv'
outfilename = 'wang_mfcc_emotion.csv'
data1 = pd.read_csv(filename1,encoding='utf-8')
data2 = pd.read_csv(filename2,encoding='utf-8')
emotion(data1,data2,outfilename)

""""""
data1 = pd.read_csv('rep_mfcc_lyric.csv',encoding='utf-8')
data2 = pd.read_csv('rep_mfcc_lyric.csv',encoding='utf-8')
outfilename = 'rep_mfcc_emotion.csv'
emotion2(data1,data2,outfilename)

""""""
data1 = pd.read_csv('dai_final_musicInfo.csv',encoding='utf-8')
data2 = pd.read_csv('dai_mfcc.csv',encoding='utf-8')
outfilename = 'dai_mfcc_emotion.csv'
emotion(data1,data2,outfilename)




#data1= '今天上海的天气真好！我的心情非常高兴！如果去旅游的话我会非常兴奋！和你一起去旅游我会更加幸福！'
#data2= '救命，你是个坏人，救命，你不要碰我，救命，你个大坏蛋！'
#data3= '美国华裔科学家,祖籍江苏扬州市高邮县,生于上海,斯坦福大学物理系,电子工程系和应用物理系终身教授!'
# 
# 
#print(sentiment_score(sentiment_score_list(data1)))
#print(sentiment_score(sentiment_score_list(data2)))
#print(sentiment_score(sentiment_score_list(data3)))
#
#data4='我很难受'
#print(sentiment_score(sentiment_score_list(data4)))
#a,b=EmotionByScore(data4)
#
#emotion=JudgingEmotionByScore(a,b)
#print(emotion)
    
















