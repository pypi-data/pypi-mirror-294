#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# #### 读取train和test文件，文件名分别是df_training.csv和df_test.csv（2分）

# In[2]:


train_data = pd.read_csv('df_training.csv')
test_data = pd.read_csv('df_test.csv')


# #### 将train_data和test_data合并成all_data（2分）

# In[3]:


all_data = pd.concat([train_data, test_data], axis=0)  # concat([train_data, test_data], axis=0)


# #### 查看all_data的字段信息（2分）

# In[4]:


all_data.info()  # info()


# In[5]:


all_data.head()  # head()


# In[23]:


all_data['Purchase or not'].value_counts()


# #### 把Product using score、age、Point balance、Estimated salary根据均值填充（2分）

# In[24]:


for col in ['Product using score', 'age', 'Point balance', 'Estimated salary']:
    all_data[col] = all_data[col].replace('?', np.nan)  # replace('?', np.nan)
    all_data[col] = pd.to_numeric(all_data[col])
    all_data[col] = all_data[col].fillna(all_data[col].mean()) # fillna(all_data[col].mean())


# #### 把User area、gender中的字符串使用LabelEncoder（2分）

# In[25]:


from sklearn.preprocessing import LabelEncoder

all_data[['User area', 'gender']] = all_data[['User area', 'gender']].apply(LabelEncoder().fit_transform)  # LabelEncoder().fit_transform


# #### 把剩余的所有？用-1代替（1分）

# In[26]:


all_data = all_data.replace('?', '-1')  # replace('?', '-1')


# #### 把除了Purchase or not外的所有object列转为int（2分）

# In[27]:


object_cols = list(set(all_data.select_dtypes('object').columns) - set(['Purchase or not']))


# In[28]:


for col in object_cols:
    all_data[col] = pd.to_numeric(all_data[col])  # to_numeric(all_data[col])


# #### 导入sklearn中随机森林（分类）的函数，并预设rf的方法（1分）

# In[29]:


from sklearn.ensemble import RandomForestClassifier # RandomForestClassifier

rf = RandomForestClassifier()


# #### 导入sklearn中数据集拆分的函数（1分）

# In[30]:


from sklearn.model_selection import train_test_split  # train_test_split


# #### 导入sklearn中classification_report（1分）

# In[31]:


from sklearn.metrics import classification_report


# #### 重新拆分训练集和测试集（1分）

# In[42]:


test_data = all_data[all_data['Purchase or not']=='Withheld'] # 'Purchase or not']=='Withheld'


# In[43]:


train_data = all_data[all_data['Purchase or not']!='Withheld'] # all_data['Purchase or not']!='Withheld'
train_data['Purchase or not'] = train_data['Purchase or not'].astype('int')


# #### 从训练集中拆分出验证集，比例为7:3（2分）

# In[34]:


pre_columns = set(all_data.columns) - set(['ID', 'Purchase or not'])


# In[35]:


# train_data[pre_columns], train_data['Purchase or not'], test_size=0.3
X_train, X_val, y_train, y_val = train_test_split(train_data[pre_columns], train_data['Purchase or not'], test_size=0.3)  # 


# #### 使用随机森林对X_train、y_train进行训练，再对X_val进行预测（2分）

# In[36]:


rf.fit(X_train, y_train)


# In[40]:


val_pred = rf.predict(X_val)


# #### 使用classification_report对val_pred和y_val进行效果评测（1分）

# In[41]:


print(classification_report(val_pred, y_val))  #classification_report(val_pred, y_val)


# #### 对test_data进行预测（1分）

# In[36]:


test_pred = rf.predict(test_data[pre_columns]) # predict


# #### 将test_data中的ID和test_pred的结果合并为output_data，然后导出为output_data.csv，不要导出索引（2分）

# In[37]:


test_data['Purchase or not'] = test_pred


# In[38]:


output_data = test_data[['ID','Purchase or not']] # ['ID','Purchase or not']


# In[39]:


output_data.to_csv('output_data.csv', index=False) # to_csv('output_data.csv', index=False)

