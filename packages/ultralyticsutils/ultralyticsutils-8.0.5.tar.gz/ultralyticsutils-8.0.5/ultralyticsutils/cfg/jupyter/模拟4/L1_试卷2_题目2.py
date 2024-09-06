#!/usr/bin/env python
# coding: utf-8

# In[2]:


#本数据取自心脏病UCI数据库包，引用了其中 14 个属性的子集。"target"字段是指患者中存在心脏病。它是介于 0（无存在）到 4 之间的整数值。
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix, f1_score
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
df = pd.read_csv('./heart.csv')
df = pd.get_dummies(df,columns = ['ctype','slo','tha'])
df.head()


# In[24]:


#1.分割特征和标签（2分）
y = df.target.values
X = df.drop(columns=['target'], axis=1)  # drop ['target'], axis=1


# In[25]:


# help(train_test_split)


# In[26]:


#2.划分训练集和测试集，分层抽样，保持划分后标签分布和划分前接近。（2分）
X_train,X_test,y_train,y_test = train_test_split(X,y, stratify=y, random_state=2022)   # train_test_split stratify=y


# In[27]:


#3.归一化(1分+1分+1分)
standardScaler = StandardScaler()
standardScaler.fit(X_train)  # fit
X_train = standardScaler.transform(X_train)  #
X_test = standardScaler.transform(X_test)  # transform


# In[28]:


# help(LogisticRegression)


# In[29]:


#4.建立逻辑回归模型，不使用正则化（3分）
model = LogisticRegression(penalty='none')  # LogisticRegression(penalty='none')
model.fit(X_train,y_train) # 


# In[14]:


#5.打印模型在训练集和测试集上的平均准确度mean accuracy (2分)
print(model.score(X_train,y_train))  #  score
print(model.score(X_test,y_test))


# In[30]:


# help(GridSearchCV)


# In[16]:


#6.使用10折网格搜索最佳模型参数（4分），打印得到的最佳模型，最佳模型参数，最佳得分（3分）
param_grid = [
    {
        'C':[0.01,0.1,1,10,100],
        'class_weight':['balanced',None]
    }
]
model_cv = GridSearchCV(LogisticRegression(),param_grid=param_grid,cv=10)  # param_grid=param_grid cv=10
model_cv.fit(X_train,y_train)
model_best = model_cv.best_estimator_
print(model_best)
print(model_cv.best_params_)#最佳模型参数
print(model_cv.best_score_)#最佳得分


# 

# #7.计算最佳模型在测试集上的宏平均F1值（2分）
# y_pred = model_best.predict(X_test)  
# print(f1_score(y_test,y_pred,average='macro'))  #  y_test,y_pred,

# In[36]:


y_pred = model_best.predict(X_test)  
print(f1_score(y_test,y_pred,average='macro'))  #  y_test,y_pred,


# In[37]:


#8.打印分类报告（2分）
print(classification_report(y_test, y_pred)) # classification_report(y_test, y_pred)


# In[20]:


#9.打印混淆矩阵（2分）
print(confusion_matrix(y_test, y_pred)) # confusion_matrix(y_test, y_pred)


# In[ ]:




