#!/usr/bin/env python
# coding: utf-8

# In[3]:


#tqdm
# os.system('pip install tqdm')
from tqdm import tqdm_notebook
from tqdm import tqdm

import lightgbm as lgb

#base import 
import numpy as np
import pandas as pd

# about sklearn
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, KFold, RepeatedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler as std
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import f1_score
#about time
import time
import datetime 
from datetime import datetime, timedelta

#Garbage collection
import gc
# scipy
from scipy.signal import hilbert
# from scipy.signal import hann
from scipy.signal import convolve
from scipy import stats
import scipy.spatial.distance as dist
#other
from collections import Counter 
from statistics import mode 
    #warning
import warnings
warnings.filterwarnings("ignore")
import json 
import math
from itertools import product
import ast 
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
# 从sklearn 调入所需要的包
# from sklearn import datasets
from sklearn.model_selection import train_test_split #数据分隔出训练集和验证集
import lightgbm as lgb
import numpy as np
import pandas as pd
#导入精度和召回
from sklearn.metrics import precision_score, recall_score,roc_auc_score
path='./'
import os
import json
import gc
# os.system('pip install numba')
from numba import jit


# In[14]:


path='./'
train = pd.read_csv(path+'input/train_set.csv')
test = pd.read_csv(path+'input/test_set.csv')
print(train.info())
print(test.info())
test['y']=-1
print(len(test.columns))
data = pd.concat([train,test]).reset_index(drop=True)
print(data.head())
data.y.describe()


# In[5]:


cat_col = [i for i in data.select_dtypes(object).columns if i not in ['ID','y']]
for i in tqdm(cat_col):
    lbl = LabelEncoder()
    data[i] = lbl.fit_transform(data[i].astype(str))


# In[6]:


data


# In[7]:


feats = [i for i in data.columns if i not in ['ID','y']]
feats


# In[8]:


tar =data[data['y']!=-1][feats]
y =data[data['y']!=-1]['y']
testx= data[data['y']==-1][feats]
train = data[data['y']!=-1]


# In[9]:


print(len(train))


# In[10]:


def split_train(data,test_ratio):
    np.random.seed(43)
    shuffled_indices=np.random.permutation(len(data))
    test_set_size=int(len(data)*test_ratio)
    test_indices =shuffled_indices[:test_set_size]
    train_indices=shuffled_indices[test_set_size:]
    return data.loc[train_indices],data.loc[test_indices]


# In[11]:


train1,vali1 = split_train(train,0.3)


# # 自己设计随机森林

# In[15]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
# columns =feature_names
tree_count=10
#设置有放回的抽取样本数
bag_proportion=0.6
predictions=[] #设置预测发生概率初始值
for i in range(tree_count):
    bag=train1.sample(frac=bag_proportion,replace=True,random_state=i)
    #建模
    clf = DecisionTreeClassifier(random_state=1,min_samples_leaf=10,splitter='random')
    clf.fit(bag[feats],bag['y'])
    predictions.append(clf.predict_proba(vali1[feats])[:,1])
combined=np.sum(predictions,axis=0)/10
print(roc_auc_score(vali1['y'],combined))


# # 调用sklearn 随机森林

# In[18]:


predictions=[]
for i in range(0,10):
    clf = RandomForestClassifier(n_estimators=20,random_state=i,min_samples_leaf=5)
    clf.fit(train1[feats],train1['y'])
    predictions.append(clf.predict_proba(vali1[feats])[:,1])

combined=np.sum(predictions,axis=0)/10
print(roc_auc_score(vali1['y'],combined))


# In[ ]:





# In[ ]:




