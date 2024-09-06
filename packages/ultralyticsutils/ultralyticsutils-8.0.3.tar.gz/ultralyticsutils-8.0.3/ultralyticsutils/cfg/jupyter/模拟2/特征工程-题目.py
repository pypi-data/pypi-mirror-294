#!/usr/bin/env python
# coding: utf-8

# 数据集__world.scv__中包含从2021年1月20日至2021年3月6日，世界每日的新冠肺炎累计确诊人数，请按要求完成下列操作：  
# （1）读取数据，将结果保存在变量data中；将日期一列的数据类型转换为datetime，并将其重设为索引；将数据按照日期正序（2021年1月20日至2021年3月6日）进行排序  
# （2）对confirmedCount一列进行对数（以e为底）变换，结果保存在变量data_log中  
# （3）对data_log中的数据进行一阶差分，结果保存在变量data_log_diff中；对data_log_diff中的数据进行单位根检验，检验的P值保存在变量p_value_diff中  
# （4）假设根据ACF，PACF图获知p=2,q=2，在此基础上建立ARIMA模型  
# （5）将模型预测值还原为每日新冠肺炎累计确诊人数的预测值（2021年1月20日至2021年3月6日）
# （6）计算模型预测值与实际值的均方误差

# ### 载入必要库

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from statsmodels.tsa.stattools import adfuller
#from statsmodels.tsa.arima_model import ARIMA  
from statsmodels.tsa.arima.model import ARIMA  
from statsmodels.tsa.arima_model import ARMA


# ### 读取数据；日期类型转换；重设索引；正序排序

# （1）读取数据，将结果保存在变量data中；将日期一列的数据类型转换为datetime，并将其重设为索引；将数据按照日期正序（2021年1月20日至2021年3月18日）进行排序(每空2分)

# In[5]:


### 读取数据
data = pd.read_csv('./world.csv', encoding='gb18030')  # read_csv

## 转换日期为datetime类型
data['日期'] = pd.to_datetime(data['日期'], infer_datetime_format=True) # to_datetime
## dayfirst yearfirst
## 重设索引
data = data.set_index('日期') # set_index

## 数据翻转[start:end:step]
data = data[::-1]

data[]


# （2）对confirmedCount一列进行对数（以e为底）变换，结果保存在变量data_log中(每空2分)

# In[7]:


## 对数变换
data_log = np.log(data['confirmedCount'])  # log


# ### 一阶差分；单位根检验

# （3）对data_log中的数据进行一阶差分，结果保存在变量data_log_diff中；对data_log_diff中的数据进行单位根检验，检验的P值保存在变量p_value_diff中(每空2分)

# In[8]:


## 一阶差分
data_log_diff = data_log.diff().dropna()  # diff


# In[9]:


adfuller(data_log_diff)


# In[10]:


##单位根检验
p_value_diff = adfuller(data_log_diff)[1]
p_value_diff


# ### 建立ARIMA模型

# （5）假设根据ACF，PACF图获知p=2,q=2，在此基础上建立ARIMA模型

# In[11]:


import warnings
warnings.filterwarnings('ignore')

#(每空2分)
model = ARIMA(data_log, order=(2,1,2))  # 2,1,2

#(每空1分)
results_ARIMA = model.fit() # fit


# ### 得到预测值

# 将模型预测值还原为每日新冠肺炎累计确诊人数的预测值（2020年1月20日至2020年3月6日）(每空2分)

# In[12]:


#累计和，每个预测值与第一个值的差值
pred_sub = results_ARIMA.fittedvalues.cumsum()

#创建一个都为第一天值的序列
pred_log = pd.Series(data_log[0], index=data_log.index)  # Series

#与累计和按照索引对应位置相加，得到预测值
pred_log = pred_log.add(pred_sub, fill_value=0)

#指数还原
pred = np.exp(pred_log)  # exp

pred


# ### 计算模型预测值与实际值间的均方误差(每空2分)

# In[13]:


from sklearn.metrics import mean_squared_error # mean_squared_error

mse_predict = mean_squared_error(data['confirmedCount'], pred) # mean_squared_error
mse_predict


# In[ ]:




