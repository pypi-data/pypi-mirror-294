#!/usr/bin/env python
# coding: utf-8

# In[32]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(r'input/qunar_freetrip.csv')
df.shape


# In[33]:


df.columns


# # 删除无用列字段

# In[34]:


df.drop(columns='Unnamed: 0',axis=1,inplace=True)
df


# # 获取列字段发现字段名内有空格

# In[35]:


cols = df.columns.values


# In[36]:


cols


# In[37]:


ccs = []
for col in cols:
    ccs.append(col.strip())
print(ccs)


# In[38]:


df.columns = [col.strip() for col in cols]


# # 重复数据查找

# In[39]:


df.duplicated()


# In[40]:


df.duplicated().sum()


# In[41]:


df.drop_duplicates().shape


# # 查看重复数据

# In[42]:


df[df.duplicated()]


# # 删除重复数据

# In[43]:


df.shape


# In[44]:


df.drop_duplicates(inplace=True)
df.shape  # 确认是否一删除


# ## 删除之后发现原数据的行索引不会自动重置

# In[45]:


df.tail()


# In[46]:


df1= df.copy()


# In[47]:


df.index
df.index = range(0,df.shape[0])
df.tail()


# ## 索引重置

# In[48]:


df1=df1.reset_index()


# In[49]:


df1.tail()


# # 异常值探索

# In[50]:


df.describe()


# ## 利用固定的算法公式去求证我们的猜想

# In[51]:


df


# In[52]:


# 判断的标准
sd = (df['价格'] - df['价格'].mean()) / df['价格'].std()  
# 利用逻辑索引筛选数据
df[(sd > 3) | (sd < -3)]


# ## 同理也可以筛选出节省的异常数据项(不一定要使用)

# In[53]:


# 判断的标准
sd1 = (df['节省'] - df['节省'].mean()) / df['节省'].std()  
# 利用逻辑索引筛选数据
df[(sd1 > 3)|(sd1 < -3)]


# ## 删除价格和节省都有异常的数据

# In[54]:


# 方式一
res = pd.concat([df[df['节省'] > df['价格']],df[abs(sd) > 3]])
res


# In[55]:


# 获取要删除的行数据 索引值
del_index = res.index
# 根据索引删除数据
df.drop(index=del_index,inplace=True)
# 再次重置索引
df.index = range(0,df.shape[0])


# # 缺失值处理

# ## 查找具有缺失值得字段列名称

# In[56]:


df.isnull().sum()


# ## 缺失数据筛选

# In[57]:


df[df.出发地.isnull()]


# ## 获取出发地缺失的数据的路线数据

# In[58]:


res=df[df.出发地.isnull()]


# In[59]:


res['路线名'].values


# ## 利用字符串切割替换出发地缺失数据

# In[60]:


for i in res['路线名'].values:
    print(i.split('-')[0])


# ## 出发地缺失填充

# In[61]:


df[df['出发地'].isnull()]


# In[62]:


df.loc[df.出发地.isnull(),'出发地'] = [i.split('-')[0] for i in df.loc[df.出发地.isnull(),'路线名'].values]


# In[63]:


df[df['出发地'].isnull()]


# In[ ]:





# In[ ]:




