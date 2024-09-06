#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd


# #### 读取csv文件，文件名为：flow_data.csv（1分）

# In[29]:


data = pd.read_csv('flow_data.csv')  # pd.read_csv('flow_data.csv')


# #### 查看data的行数和列数（2分）

# In[30]:


data.shape # shape


# #### 查看data前10行（2分）

# In[31]:


data.head(10)  # head(10)


# #### 计算客户个数（2分）

# In[32]:


len(data.user_id.unique())  # data.groupby('user_id')  user_id.unique()


# #### 查看每个客户交易次数（2分）

# In[33]:


data.user_id.value_counts()  # value_counts


# #### 删除unix_time列中值为0的行（2分）

# In[7]:


data = data[data['unix_time']!=0]  # data['unix_time']!=0
data.shape[0]


# #### 去除data中交易金额为\N的行（2分）

# In[8]:


data = data[data['payment']!='\\N']  # data['payment']=='\\N'
data.shape[0]


# In[21]:


help(pd.DataFrame())


# #### 请在data中新建一列pay_time，将data中unix_time列转换为标准时间格式且最小表示单位为秒，保存在data['pay_time']列中（3分）

# In[10]:


data['pay_time'] = pd.to_datetime(data['unix_time'], unit='s')  # to_datetime(data['unix_time'], unit='s')


# #### 把payment的单位从分转为元（2分）

# In[11]:


data['payment'] = data['payment'].astype('int')
data['payment'] = data['payment'] / 100  # data['payment'] / 100


# #### 去除data中的重复项（2分）

# In[12]:


data = data.drop_duplicates()  # drop_duplicates()
data.shape[0]


# #### 查看describe中前10个重现最多的值，并转化为列表（2分）

# In[38]:


describe_top10 = list(data['describe'].value_counts().index[:10])
describe_top10


# #### 在data中新增一列'describe_top10'，把describe_top10的值进行数值化（0,1,2....），根据describe进行映射，其余的则按10（3分）

# In[44]:


describe_top10_dict = {x:y for x,y in zip(describe_top10, range(10))}

data['describe_top10'] = data['describe'].map(describe_top10_dict)
data['describe_top10'] = data['describe_top10'].fillna(10)


# In[43]:


data


# In[ ]:




