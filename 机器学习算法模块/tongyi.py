# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 19:24:15 2021

@author: hzzxq
"""


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
 
filename = '王.csv'#剔除歌词为空的数据
filename_final = 'wang_final_musicInfo.csv'
music_filename = "王之歌曲存储/"
delete_nanlyric(filename,filename_final,music_filename)


#path = r'王之歌曲存储/'
#songs =list(set(os.listdir(path)))
#for song in songs:
#    song_id = song.split(".")[0]
#    file_name = '王之歌曲存储/'+str(song_id)+'.mp3'
#    if int(song_id) not in list(data['歌曲id']):
#        print(file_name)
#        os.remove(file_name)