#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd


# #### 读取train和test文件，文件名分别是cs-training.csv和cs-test.csv（2分）

# In[27]:


train_data = pd.read_csv('cs-training.csv')
test_data = pd.read_csv('cs-test.csv')


# #### 将train_data和test_data合并成all_data（2分）

# In[28]:


all_data = pd.concat([train_data, test_data], axis=0)


# #### 查看all_data的字段信息（2分）

# In[29]:


all_data.info()  # info()


# In[30]:


#查看头5行数据
all_data.head(5)


# In[31]:


all_data['SeriousDlqin2yrs'].value_counts()


# #### 把MonthlyIncome和NumberOfDependents根据均值填充（2分）

# In[32]:


all_data['MonthlyIncome'] = all_data['MonthlyIncome'].fillna(all_data['MonthlyIncome'].mean())


# In[33]:


all_data['NumberOfDependents'] = all_data['NumberOfDependents'].fillna(all_data['NumberOfDependents'].mean())


# #### 导入sklearn中随机森林（分类）的函数，并预设rf的方法（2分）

# In[37]:


from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()


# #### 导入sklearn中数据集拆分的函数（1分）

# In[38]:


from sklearn.model_selection import train_test_split


# #### 导入sklearn中classification_report（1分）

# In[39]:


from sklearn.metrics import classification_report


# #### 重新拆分训练集和测试集（2分）

# In[40]:


test_data = all_data[all_data['SeriousDlqin2yrs']=='U']


# In[41]:


train_data = all_data[all_data['SeriousDlqin2yrs']!='U']
train_data['SeriousDlqin2yrs'] = train_data['SeriousDlqin2yrs'].astype('int')


# #### 从训练集中拆分出验证集，比例为7:3（2分）

# In[42]:


pre_columns = set(all_data.columns) - set(['CustomerID', 'SeriousDlqin2yrs'])


# In[43]:


X_train, X_val, y_train, y_val = train_test_split(train_data[pre_columns], train_data['SeriousDlqin2yrs'], test_size=0.3)


# #### 使用随机森林对X_train、y_train进行训练，再对X_val进行预测（2分）

# In[44]:


rf.fit(X_train, y_train)


# In[46]:


val_pred = rf.predict(X_val)


# #### 使用classification_report对val_pred和y_val进行效果评测（2分）

# In[48]:


print(classification_report(y_val, val_pred))


# #### 对test_data进行预测（2分）

# In[49]:


test_pred = rf.predict(test_data[pre_columns])


# #### 将test_data中的CustomerID和test_pred的结果合并为output_data，然后导出为output_data.csv，不要导出索引（3分）

# In[50]:


test_data['SeriousDlqin2yrs'] = test_pred


# In[51]:


output_data = test_data[['CustomerID','SeriousDlqin2yrs']]


# In[52]:


output_data.to_csv('output_data.csv', index=False)


# In[ ]:




