#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function, division
import pandas as pd
pd.set_option("display.max_rows", 20)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
import time


# ## pandas.groupby学习

# ### groupby示意
# groupby就是按某个字段分组, 它也确实是用来实现这样功能的.   
# 比如, 将一份数据集按A列进行分组：  

# In[2]:


get_ipython().run_cell_magic('html', '', '<img src="img/t.webp", width=600, heigth=500>\n')


# ### 读取数据

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('./input/train_set.csv',nrows=1000)
print(df.head())


# In[4]:


print(set(df['job']))


# ### groupby对象
# DataFrame使用groupby()函数返回的结果是DataFrameGroupBy   
# 不是一个DataFrame或者Series  

# In[22]:


groupbyage = df.groupby('age')
print(type(groupbyage))
print(groupbyage)


# In[23]:


groupbyage.count()


# In[13]:


groupbyage.count()['ID']


# groupby分组不仅可以指定一个列名，也可以指定多个列名

# In[14]:


groupbyagemarital = df.groupby(['age','marital'])
print(groupbyagemarital.count()['ID'])


# In[21]:


groupbyagemarital = df.groupby(['age','marital'])
groupbyagemarital.count()['ID'].reset_index()  # to df 


# ### groupby常用的一些功能

# In[6]:


df.groupby('job')['age'].sum()


# In[16]:


df.groupby('job')['age']


# In[7]:


df.groupby('job')['age'].mean()


# In[8]:


df.groupby('job')['age'].count()

