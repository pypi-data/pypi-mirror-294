#!/usr/bin/env python
# coding: utf-8

# In[2]:


#本数据取自心脏病UCI数据库包，引用了其中 14 个属性的子集。"target"字段是指患者中存在心脏病。它是介于 0（无存在）到 4 之间的整数值。
import numpy as np
import pandas as pd


# In[3]:


#1.指定使用“|”作为分隔符（2分）
#df = pd.read_csv('./heart.csv',_____='|')
df = pd.read_csv('./heart.csv',sep='|')


# In[4]:


#2.查看最后10行数据（2分）
df.tail(10)


# In[5]:


#3.查看数据总体情况（2分）
df.info(max_cols=14)


# In[ ]:


#4.查看数据的各统计量（2分）
df.describe()


# In[7]:


#5.查看target字段的分布情况（2分）,按索引升序排列（2分）
# df.target._____(_____)
df.target.value_counts(ascending=True)


# In[8]:


#6.对特征中非连续型数值特征ctype进行onehot编码（3分），前缀为new_ctype（3分）
# ctype = pd._____(df['ctype'], _____)
ctype = pd.get_dummies(df['ctype'], prefix='new_ctype')


# In[9]:


#7.将编码结果拼接回原始数据中（2分+2分+1分）
# df = pd._____(_____, axis = _____ )
df = pd.concat([df, ctype], axis = 1 )


# In[10]:


#8.删除原来的ctype字段（2分）
# df = df.drop(_____ = 'ctype')
df = df.drop(columns = 'ctype')
df.head(3)

