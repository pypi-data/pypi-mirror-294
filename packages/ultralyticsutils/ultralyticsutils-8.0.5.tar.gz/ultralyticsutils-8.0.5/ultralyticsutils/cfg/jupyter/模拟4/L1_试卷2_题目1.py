#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from sklearn.preprocessing import StandardScaler,LabelEncoder
#1.读取数据，训练集需使用gbk编码（3分）
train = pd.read_csv('train_dataset.csv',encoding='gbk')  # encoding='gbk'
test = pd.read_csv('test_dataset.csv')


# In[4]:


#2.打印训练集信息，包含非空字段数、字段类型、占用内存等（2分）
print(train.info())  # info()


# In[6]:


#3.设置pandas 显示最大列（2分）
pd.set_option('display.max_columns',30)  #  set_option
train.head(2)


# In[7]:


#4.打印训练集的协方差矩阵及相关性（4分）
print(train.cov())  # cov()
print(train.corr())  # corr()


# In[11]:


#5.打印用户年龄字段有多少种不同的年龄（2分）
train['用户年龄'].value_counts().shape[0]  # 用户年龄 value_counts


# In[14]:


#6.打印测试集空值数（2分）
print(test.isnull().sum())  # isnull() sum()


# In[16]:


#7.将测试集的信用分默认给-1,用于后续筛选出信用分为-1的数据作为test (2分)
test['信用分'] = -1  #  '信用分'  -1
#8.合并训练集train, 测试集test，并忽略索引(2分)
data = pd.concat([train, test], ignore_index=True)  # concat [train,test]  ignore_index=True


# In[17]:


#9.筛选出不包含 '用户编码'和'信用分'字段的内容作为最终特征(2分)
features = list(set(data.columns) - set(['用户编码','信用分']))  # columns ['用户编码','信用分']
#
print(features)
feats = features


# In[19]:


#10.筛选出离散变量（2分）
cat_col1 = [i for i in data.select_dtypes(object).columns if i not in ['用户编码','信用分']]   # select_dtypes


# In[20]:


#11.使用标签编码将字符型特征强转成数值型（2分）
for i in cat_col1:
    lbl = LabelEncoder()
    data[i] = lbl.fit_transform(data[i])


# In[ ]:




