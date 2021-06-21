# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:07:26 2021

@author: hzzxq
"""

import requests
import json

uid = '1483982859'
'''进入登陆状态的session'''
login_url='http://localhost:3000/login/cellphone?phone=13408462303&password=shiyan123456789'
s=requests.Session()
responsesdata1=s.get(url=login_url)
#    recharge_url='http://localhost:3000/user/playlist?uid='+str(uid)
recharge_url='http://localhost:3000/user/record?uid='+str(uid)+'&type=0'
responsesdata2=s.get(url=recharge_url)
result1=json.loads(responsesdata2.text)
with open(str('用户歌单/')+str(uid)+"_record.json", "w",encoding='utf-8') as f:
    f.write(json.dumps(result1, ensure_ascii=False, indent=4, separators=(',', ':')))
#    with open('用户歌单/'+str(uid)+'.json','r',encoding='utf8')as fp:
#        t_data = json.load(fp)

recharge_url='http://localhost:3000/user/playlist?uid='+str(uid)
responsesdata2=s.get(url=recharge_url)
result2=json.loads(responsesdata2.text)
with open(str('用户歌单/')+str(uid)+"_playlist.json", "w",encoding='utf-8') as f:
    f.write(json.dumps(result2, ensure_ascii=False, indent=4, separators=(',', ':')))
    
    
import os
import requests
import re
import pandas as pd
def download_songs(list_id,uid):
    headers={
    'Referer':'https://music.163.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    }

    list_id = list_id
    list_url = 'https://music.163.com/playlist?id=%s' % list_id
    res = requests.get(list_url, headers=headers)
    list_title = re.findall(r'<title>(.*?)</title>',res.text)[0][:-13].replace('/', '_')
    song_list_folder_path =str(list_id)
    all_folder_path=str(uid)
    if not os.path.exists(all_folder_path):
        os.mkdir(all_folder_path)

    song_count = 0
    song_ids = re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', res.text)
    song_id=[]
    song_name=[]
    for i in song_ids:
        song_id.append(i[0])
        song_name.append(i[1])
    temp_data=pd.DataFrame({'song_id':song_id,'song_name':song_name})
    temp_data.to_csv(all_folder_path+'/'+song_list_folder_path+'.csv',encoding='utf-8',index=False)

def download_songs2(list_id,uid):
    headers={
    'Referer':'https://music.163.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    }

    list_id = list_id
    list_url = 'https://music.163.com/playlist?id=%s' % list_id
    res = requests.get(list_url, headers=headers)
    list_title = re.findall(r'<title>(.*?)</title>',res.text)[0][:-13].replace('/', '_')
    song_list_folder_path =str(list_id)
    all_folder_path=str(uid)
    if not os.path.exists(all_folder_path):
        os.mkdir(all_folder_path)

    song_count = 0
    song_ids = re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', res.text)
    song_id=[]
    song_name=[]
    for i in song_ids:
        song_id.append(i[0])
        song_name.append(i[1])
    temp_data=pd.DataFrame({'song_id':song_id,'song_name':song_name})
    temp_data.to_csv(all_folder_path+'/'+song_list_folder_path+'.csv',encoding='utf-8',index=False)
    
import shutil
def get_user_songlist_playlist(uid):
    with open('用户歌单/'+str(uid)+'_playlist.json','r',encoding='utf8')as fp:
        json_data = json.load(fp)
    temp_list_ids=[]
    for i in range(len(json_data['playlist'])):
        temp_list_ids.append(json_data['playlist'][i]['id'])
        download_songs(json_data['playlist'][i]['id'],uid)
    shutil.move(str(uid),'歌单存储')
    



import requests
def Music_download(song_id):
    headers={
    'Referer':'https://music.163.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    }
    song_id=str(song_id)
    download_url = "http://music.163.com/song/media/outer/url?id=%s" % song_id
    try:
        temp=requests.get(download_url, headers=headers).content
        with open(song_id +'.mp3', 'wb') as f:
            f.write(temp)
            return 1
    except:
        print("下载失败")
        return 0


