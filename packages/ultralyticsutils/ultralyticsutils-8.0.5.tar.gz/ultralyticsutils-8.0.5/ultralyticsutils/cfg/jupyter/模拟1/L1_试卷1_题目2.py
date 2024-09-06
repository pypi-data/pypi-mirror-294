#!/usr/bin/env python
# coding: utf-8

# In[2]:


#使用随机森林算法建模预测最高气温
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomTreesEmbedding,RandomForestRegressor,GradientBoostingClassifier,RandomForestClassifier
df = pd.read_csv('temps.csv')
df.head(5)


# In[7]:


#1.打印数据行列数(2分)
# print(df._____)
print(df.shape)


# In[11]:


#2.描述性统计数据，要包括类别型特征"week"的统计结果(2分)
# df._____(_____)
df.describe(include='all')


# In[12]:


#3.独热编码(2分)
# df = pd._____(df)
df = pd.get_dummies(df)
df.head(5)


# In[14]:


#4.在特征中去掉标签actual（2分）
# X = df._____('actual', _____)
X = df.drop('actual', axis=1)
#5.单独存储特征名字（2分）
# feature_list = list(X._____)
feature_list = list(X.columns)
#6.将特征和标签转换为numpy的格式（2分）
X = np.array(X)
y = np.array(df['actual'])
#生成训练集和测试集
train_features, test_features, train_labels, test_labels = train_test_split(X, y, test_size = 0.25,
                                                                           random_state = 2022)


# In[16]:


#7.建立随机森林模型对气温进行预测（2分）
# model = _____(n_estimators= 1000, random_state=2022)
model = RandomForestRegressor(n_estimators= 1000, random_state=2022)

#8.训练并预测结果（2分）
model.fit(train_features, train_labels)
predictions = model.predict(test_features)

# 计算MAPE
print ('MAPE:',100 * np.mean( abs(predictions - test_labels)/ test_labels))


# In[18]:


#9.得到特征重要性（2分）
# importances = list(model._____)
importances = list(model.feature_importances_)

# 10.转换格式（1分）
feature_importances = [(feature, importance) for feature, importance in zip(feature_list, importances)] # zip
# 11.降序排列（2分）
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse=True) # sorted reverse=Ture
# 对应进行打印
tmp = [print('特征: {:20} 重要性: {}'.format(*pair)) for pair in feature_importances]


# In[20]:


#12.只选择最重要的那两个特征重新训练（2分）
important_indices = [feature_list.index('temp_1'), feature_list.index('average')]  # tmpe_1 average
train_important = train_features[:, important_indices]
test_important = test_features[:, important_indices]
#13.重新训练模型并预测结果（2分）
model.fit(train_important, train_labels) # fit
predictions = model.predict(test_important) # predict

# 评估结果
print ('MAPE:',100 * np.mean( abs(predictions - test_labels)/ test_labels))


# In[ ]:




