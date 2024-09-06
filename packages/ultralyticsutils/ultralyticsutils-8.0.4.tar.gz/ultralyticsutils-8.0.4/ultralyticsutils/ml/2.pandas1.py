#!/usr/bin/env python
# coding: utf-8

# ### 导入pandas 包

# In[4]:


import pandas as pd


#     pandas :1.主要包含Series和DataFrame两个数据结构；2.经常和numpy配合使用
#     Series 带有标签的同构类型数组
#     DataFrame：一个DataFrame中可以包含若干个Series。

# In[5]:


# 获取版本信息
print(pd.__version__)


# ### 读取数据

# In[6]:


path='./'
train = pd.read_csv(path+'input/train_set.csv')
test = pd.read_csv(path+'input/test_set.csv')
print(train.info())
print(test.info())


# ### 获取数据类型

# In[7]:


train.dtypes.value_counts()


# ### 截取其中一列

# In[8]:


x=train[['age']]


# In[9]:


x


# In[10]:


print(train['age'].value_counts())


# In[11]:


train.head()


# In[12]:


train.tail()


# ### 查看列名

# In[13]:


#columns 
print(train.columns)


# ### 重命名dataframe的特定列

# In[14]:


train=train.rename(columns={'age':'age1'})


# In[15]:


train.head()


# ### 查看缺失值

# In[16]:


# 若有缺失值，则为Ture
train.isnull().values.any()


# In[17]:


train.isnull().sum()


# In[18]:


train.apply(lambda x: x.isnull().sum())


# ### 查看DF属性

# In[19]:


#columns 
print(train.columns)


# In[20]:


l1=list(train.columns)


# In[21]:


print(train.shape)


# In[22]:


print(train.size)


# In[23]:


train.shape[0] * train.shape[1]


# In[24]:


train.values


# In[28]:


train.dtypes


# In[29]:


train.ndim


# In[30]:


train['ID'].head()


# In[31]:


train['poutcome'].head(10)


# In[ ]:





# In[ ]:




