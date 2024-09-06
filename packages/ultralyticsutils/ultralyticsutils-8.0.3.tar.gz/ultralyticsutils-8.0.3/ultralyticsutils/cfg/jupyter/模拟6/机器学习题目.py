#!/usr/bin/env python
# coding: utf-8

# 样本数据集train_dataset.csv,test_dataset.csv为某运营商公司提供的消费者人群信息，包括客户的各类通信支出、欠费情况、出行情况、消费场所、社交、个人兴趣等丰富的多维度数据。请使用该数据集完成以下探索性分析：  
# 1.分别读入训练集、测试集，编码格式为'gbk'，并查看样本详细信息；  
# 2.分别查看训练集前100行，测试集后100行数据情况；  
# 3.查看样本详细描述；  
# 4.查看训练集各特征间相关性；  
# 5.查看训练集、样本集形状信息；
# 6.判断样本数据中有多少不同值；  
# 7.对样本数据缺失值统计；  
# 8.合并训练集、测试集，并重建索引；  
# 9.对字符型特征或者类别特征进行LabelEncoder

# In[2]:


import numpy as np 
import pandas as pd 


# ## 读入训练集、测试集

# In[3]:



path='./'
# 使用'gbk'编码读取数据，2分
train = pd.read_csv(path+'input/train_dataset.csv',encoding='gbk')  # read_csv
test = pd.read_csv(path+'input/test_dataset.csv')


# In[4]:


#查看训练集详细信息，1分
train.info()  #info


# ## 查看训练集头部、训练集尾部

# In[5]:


pd.options.display.max_rows = 1000 #pandas 显示最大行
pd.options.display.max_columns = 200#pandas 显示最大列

train.head(100) #显示头100行，1分   # head(100)


# In[6]:


train.tail(100) #显示最后100行。1分 tail(100)


# ## 查看训练集、测试集描述

# In[7]:


train.describe()# 用于数据描述，数值特征才有数据描述。1分 describe


# In[33]:


test.describe()


# ## 训练集的相关性

# In[8]:


train.corr() # 计算相关系数。2分  corr


# ## 训练集和测试集的形状

# In[9]:


#输出：“训练集的形状为：(50000, 30) 测试集的形状为：(50000, 29)” 。8分
print("训练集的形状为：{}".format(train.shape),"测试集的形状为：{}".format(test.shape))  # format shape


# ## 判断训练集、测试集中有多少不同值

# In[10]:


for i,name in enumerate(train.columns):
    name_sum = train[name].value_counts().shape[0]   ## 2分 # value_counts
    print("{}.{}      特征中包含不一样的特征值共：{}种，占所有的{}".format(i + 1, name, name_sum,name_sum/50000))


# In[11]:


for i,name in enumerate(test.columns):
    name_sum = test[name].value_counts().shape[0]   #2分 # 
    print("{}.{}      特征中包含不一样的特征值共：{}种，占所有的{}".format(i + 1, name, name_sum,name_sum/50000))


# ## 训练集、测试集缺失值数据分析

# In[12]:


train.isnull().sum()


# In[13]:


test.isnull().sum()


# ## 合并训练集测试集并重建索引

# In[17]:


# 合并训练集测试集
test['信用分']=-1   #将测试集的信用分默认给-1
data = train.append(test).reset_index(drop=True) ## 1分  reset_index


# ## 对数据集字符型特征或者类别特征进行LabelEncode

# In[18]:


#所有特征
features = [i for i in train.columns if i not in['用户编码','信用分']]## 筛选出不包含['用户编码'，'信用分']的值作为最终特征
feats = features
feats


# In[25]:


cat_col1 = [i for i in data.select_dtypes(object).columns if i not in ['用户编码','信用分']] 
# 筛选除['用户编码'，'信用分']列的object形特征作为类别特征用于labelEncoder处理
for i in cat_col1:
    lbl = LabelEncoder()
    data[i] = lbl.fit_transform(data[i].astype(str))# 直接将字符型特征强转成数值型。 4分  # astypes


# In[24]:


data


# In[ ]:




