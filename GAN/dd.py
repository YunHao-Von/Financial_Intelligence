import pandas as pd











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
