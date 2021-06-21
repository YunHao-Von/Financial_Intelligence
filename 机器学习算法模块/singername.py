# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:29:33 2021

@author: hzzxq
"""
import json
import os
import requests
import re
import pandas as pd

login_url='http://localhost:3000/login/cellphone?phone=13408462303&password=shiyan123456789'
s=requests.Session()
responsesdata1=s.get(url=login_url)

def getSingerName(id):
    recharge_url='http://localhost:3000/artist/detail?id='+str(id)
    responsesdata2=s.get(url=recharge_url)
    result=json.loads(responsesdata2.text)
    if(result['code']==200):
        return result['data']['artist']['name']
    if(result['code']!=200):
        return 0
    
singer_ids = set(pd.read_csv('王.csv', encoding='utf-8')['歌手id'])|set(pd.read_csv('代2.csv', encoding='utf-8')['歌手id'])
frame = pd.DataFrame({'singer_id':[],'singer_name':[]})
i = 0
for id in singer_ids:
    print(i)
    i += 1
    name = getSingerName(id)
    if name != 0:
        temp_frame = pd.DataFrame({'singer_id':[id],'singer_name':[name]})
        frame = pd.concat([frame,temp_frame])
frame.to_csv('歌手姓名.csv',header=True, index=None) 
frame.to_excel('歌手姓名.xlsx',header=True, index=None) 