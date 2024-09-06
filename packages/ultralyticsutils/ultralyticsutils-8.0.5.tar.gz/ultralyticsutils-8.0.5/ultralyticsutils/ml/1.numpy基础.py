#!/usr/bin/env python
# coding: utf-8

# # 基础
# ## 导入Numpy 包

# In[1]:


import numpy as np


# numpy 的版本

# In[2]:


np.__version__


# In[3]:


np.arange(10)


# In[6]:


a = np.arange(10)**3
a


# In[7]:


a.ndim


# ## numpy 知识点

# 是数组，是核心，可以上一维数组也可以是多维数组

#     ndarray.ndim 秩，即轴的数量或维度的数量 
#     ndarray.shape 数组的维度，对于矩阵，n 行 m 列 
#     ndarray.size 数组元素的总个数，相当于 .shape 中 n*m 的值 
#     ndarray.dtype ndarray 对象的元素类型 
#     ndarray.itemsize ndarray 对象中每个元素的大小，以字节为单位 
#     ndarray.flags ndarray 对象的内存信息 
#     ndarray.real ndarray元素的实部 
#     ndarray.imag ndarray 元素的虚部 
#     ndarray.data 包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。

# In[6]:


x=np.arange(10)


# In[7]:


x.ndim,x.shape,x.size,x.dtype,x.itemsize


# In[21]:


x=np.array([[1,2,3],[3,2,1]])


# In[22]:


x.ndim,x.shape,x.size,x.dtype,x.itemsize


# In[24]:


x2=x.reshape(3,2)


# In[25]:


x2


# In[8]:


'=='.join('how')


# ### 创建数组

# In[26]:


np.zeros((3,2),dtype=np.int)


# In[5]:


np.zeros((100,),dtype=np.int)


# In[27]:


np.ones((3,2),dtype=np.int)


# ### np.arange和np.linspace的用法

# In[9]:


np.arange(1,20,2)


# In[10]:


np.linspace(0, 10, num=5) #2是个数，等差数列


# In[ ]:


#np.logspace等比数列


# ### np.char
# - numpy 的字符串函数

# In[32]:


np.char.join(['-'],['hello','how'])


# In[33]:


np.char.replace('hello','o','')

