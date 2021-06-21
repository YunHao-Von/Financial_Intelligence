import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing # 规范化
from sklearn import svm
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.externals import joblib

# 1. 获得数据、分割数据和规范化数据
''''''
#numk = 50
filename1 = 'wang_mfcc_emotion.csv'
filename2 = 'rep_mfcc_emotion.csv'
''''''
#numk = 800
filename1 = 'dai_mfcc_emotion.csv'
filename2 = 'rep_mfcc_emotion.csv'

data1 = pd.read_csv(filename1, encoding='utf-8')
data1['tag'] = 1
data2 = pd.read_csv(filename2, encoding='utf-8')
data2['tag'] = 0
songids = [int(i) for i in data1['id']]
for i in range(len(data2)):
    if int(data2['id'][i]) in songids:
        data2.drop(index = i,inplace = True)
data = pd.concat([data1.iloc[0:140],data2.iloc[0:200]])
#data2.iloc[140:280].to_csv('wang_test.csv',index=False)
#data.to_csv('wang_train.csv',index=False)
#data2[800:].to_csv('datayuce2.csv',index=False)
#np.save('data.npy',data)
X= data.iloc[:,1:-1]
y= data.iloc[0:280,-1]
#规范化X 到[0,1]采用max-min规范化方法
min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X)

#radnom_state参数是固定一种划分方式，保证重复运行程序时，结果一样。
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X[0:280],y,test_size=0.25,random_state=12345)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100,max_features=11,random_state=12345)
rf = rf.fit(Xtrain,Ytrain)#用训练集训练模型
y_pred = rf.predict(Xtest)#用模型预测，测试集的目标属性
score = rf.score(Xtest, Ytest)
print("测试精度： ", score)
#X= data.iloc[2800:,1:-1]
#y= data.iloc[2800:,-1]
y_pred = rf.predict(X[280:])
X0 = data.iloc[280:,0:-1]
cmd_list = [ int(i) for i in X0[y_pred==1]['id']]
np.save('wang_rf_cmd_list.npy',cmd_list)



#2. SVM模型的构建、训练和测试
svm_classifier=svm.SVC(kernel='rbf',class_weight={1:1,0:8.5},gamma=0.2,C=2, decision_function_shape='ovo')


#开始训练
svm_classifier.fit(Xtrain,Ytrain)  
y_pred = svm_classifier.predict(Xtest)



#计算svm分类器的准确率
print("SVM-输出测试集的准确率为：",svm_classifier.score(Xtest,Ytest))
#保存模型
joblib.dump(svm_classifier, "dai_svm_classifier.m")
clf = joblib.load("dai_svm_classifier.m")
X= data.iloc[2800:,0:-1]
y= data.iloc[2800:,-1]
clf.predict(X)

#print("支持向量的个数SVs：", svm_classifier.n_support_)



# 性能评价：获得混淆矩阵、f1-score, precision, recall等指标 

#混淆矩阵的绘制函数
#参数：  cm: 使用confusion_matrix()计算的混淆矩阵
#def plot_confusion_matrix(cm, title='Confusion Matrix'):
#    sns.set()
#    f,ax=plt.subplots()
#    sns.heatmap(cm,annot=True,ax=ax, cmap="Blues", fmt="4d") #画热力图
#
#    ax.set_title('confusion matrix') #标题
#    ax.set_xlabel('predict') #x轴
#    ax.set_ylabel('true') #y轴
#    ax.set_xticks 
#    
#    plt.show()
#
##得到混淆矩阵
#cm = confusion_matrix(Ytest, y_pred,labels=[0,1])
#
##调用函数，绘制混淆矩阵图
#plot_confusion_matrix(cm )
#
#
##precision, recall, f1评价指标
#print('F1-score的值：', f1_score(Ytest, y_pred) )
#print('Precision的值：', precision_score(Ytest, y_pred)  )
#print('Recall的值：',recall_score(Ytest, y_pred)    )

'''预测数据提取'''
#df1 = pd.read_csv('wang_mfcc_emotion.csv', encoding='utf-8')
#df2 = pd.read_csv('dai_mfcc_emotion.csv', encoding='utf-8')
#songids = [int(i) for i in df2['id']]
#df3 = pd.read_csv('datayuce2.csv', encoding='utf-8').iloc[:,:-1]
#songids2 = [int(i) for i in df3['id']]
#for i in range(len(df1)):
#    if int(df1['id'][i]) in songids:
#        df1.drop(index = i,inplace = True)
#    elif int(df1['id'][i]) in songids2:
#        df1.drop(index = i,inplace = True)
#df1.to_csv('more_data_yuce.csv',index=False)

#data = pd.concat([df3,df1])
#set(data['id'])
#data.to_csv('more_data_yuce.csv',index=False)
#a=pd.read_csv('more_data_yuce.csv', encoding='utf-8')
#b=pd.read_csv('datayuce2.csv', encoding='utf-8')

