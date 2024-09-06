#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# #### 读取csv文件，文件名为：cs-training.csv（2分）

# In[2]:


data = pd.read_csv('cs-training.csv')  # read_csv('cs-training.csv')


# #### 查看data的行数和列数（2分）

# In[3]:


data.shape # shape


# #### 查看data前10行（2分）

# In[5]:


data.head(10)m # head(10)


# #### 查看表的整体信息（2分）

# In[8]:


data.info() # info()


# #### 查看表的均值、中位数等信息（2分）

# In[9]:


data.describe()


# #### 查看SeriousDlqin2yrs值的分布比例（2分）

# In[10]:


data['SeriousDlqin2yrs'].value_counts()  # ['SeriousDlqin2yrs'].value_counts()


# #### 查看data中所有列的缺失值情况（2分）

# In[12]:


data.isnull().sum()  # isnull().sum()


# #### 把MonthlyIncome根据均值填充（2分）

# In[14]:


data['MonthlyIncome'] = data['MonthlyIncome'].fillna(data['MonthlyIncome'].mean())  # fillna(data['MonthlyIncome'].mean())


# #### 把age中小于22岁的填充为22岁，大于70岁的填充为70岁（3分）

# In[16]:


data['age'] = data['age'].apply(lambda x: 22 if x<22 else 70 if x>70 else x)  # .apply(lambda x: 22 if x<22 else 70 if x>70 else x) 


# #### 把NumberOfDependents根据-1填充（2分）

# In[17]:


data['NumberOfDependents'] = data['NumberOfDependents'].fillna(-1)  # fillna(-1)


# #### 把age进行等宽分箱（包括6个箱子：30以下，30-39，40-49,50-59,60-69,70及以上），产生新列age_box（2分）

# In[18]:


def age_box(df):
    if df.age<30:
        return '30以下'
    elif 30<=df.age<=39:
        return '30-39'
    elif 40<=df.age<=49:
        return '40-49'
    elif 50<=df.age<=59:
        return '50-59'
    elif 60<=df.age<=69:
        return '60-69'
    elif 70<=df.age:
        return '70及以上'

data['age_box'] = data.apply(age_box, axis=1)  # .apply(age_box, axis=1)


# #### 把整理好的data导出为data2.csv，不要索引（2分）

# In[19]:


data.to_csv('data2.csv', index=False)  # 


# In[ ]:




