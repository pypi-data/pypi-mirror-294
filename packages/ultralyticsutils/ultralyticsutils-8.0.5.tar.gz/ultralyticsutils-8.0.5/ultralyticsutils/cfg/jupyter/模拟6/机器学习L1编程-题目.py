#!/usr/bin/env python
# coding: utf-8

# 数据文件Default.csv包含客户的一些个人信用数据，共10000条数据，4个字段，任务是建立一个分类模型预测客户是否会出现信用违约。  
# 数据文件已被分为四部分，训练集Default_train.csv，训练集标签Default_train_labels.csv，测试集Default_test.csv，测试集标签Default_test_labels.csv。请按要求完成下列操作：
# 1、读入数据集，查看训练集基本信息， 并分别查看训练集、测试集标签取值分布；
# 2、建立逻辑回归模型（除参数random_state=10以外，其它参数设为默认值），并在测试集上做出预测，将测试集预测标签保存在变量pred_labels中，并依次输出下列评价指标的值（1为正类）：  
# 正确率（Accuarcy），保存在变量pred_accuarcy中；  
# 召回率（Recall），保存在变量pred_recall中：  
# F1值（F1-score），保存在变量pred_f1中。    
# 2、使用交叉验证网格搜索调整逻辑回归模型的参数（评价标准为recall值），进一步提升模型的分类性能，输出最优模型下测试集的AUC值，保存在变量pred_best_auc中。 

# # 载入数据集

# In[1]:


# 读取数据(每空1分)
import pandas as pd
X_train = pd.read_csv('Default_train.csv')   # read_csv
X_test = pd.read_csv('Default_test.csv')
y_train = pd.read_csv('Default_train_labels.csv')
y_test = pd.read_csv('Default_test_labels.csv')


# In[3]:


# 查看训练集集基本信息(每空1分)
X_train.info()  #  info


# In[4]:


# 查看训练集目标字段取值分布(每空1分)
y_train['default'].value_counts()  # value_counts


# In[5]:


# 查看测试集目标字段取值分布(每空1分)
y_test['default'].value_counts() # value_counts


# In[6]:


# 忽略警告信息
import warnings
warnings.filterwarnings('ignore')


# # 建立逻辑回归模型

# In[7]:


#(每空1分)

from sklearn.linear_model import LogisticRegression  # LogisticRegression

# 建立逻辑回归模型
model_LR = LogisticRegression(random_state=10)


# 训练模型
model_LR.fit(X_train, y_train)

# 测试集上做预测
pred_labels = model_LR.predict(X_test)


# In[8]:


# 输出分类指标
## 正确率
from sklearn.metrics import accuracy_score
pred_accuarcy = accuracy_score(y_pred=pred_labels, y_true=y_test)
pred_accuarcy


# In[9]:


# (每空1分)

from sklearn.metrics import recall_score  # recall_score
## 召回率
pred_recall = recall_score(y_pred=pred_labels, y_true=y_test)
pred_recall


# In[10]:


from sklearn.metrics import f1_score
## 
pred_f1 = f1_score(y_pred=pred_labels, y_true=y_test)
pred_f1


# # 使用网格搜索进行参数调优并计算AUC值

# In[18]:


# (每空1分)

from sklearn.model_selection import GridSearchCV

# 设置参数网格
weights_grid = ['balanced', None]
penalty_grid = ['l1', 'l2']
C_grid = [0.001, 0.01, 0.1, 0.2, 0.5, 1, 10]

grid_search = GridSearchCV(estimator=model_LR,   # model_LR
                           param_grid={'class_weight':weights_grid, 'penalty':penalty_grid, 'C':C_grid},
                           cv=5, scoring='recall')

# 交叉验证网格搜索
grid_search.fit(X_train, y_train)  # fit


# In[19]:


# (每空2分)
# 输出最优模型
grid_search.best_estimator_ # best_estimator_


# In[24]:


# (每空2分)
from sklearn.metrics import roc_curve, auc
# 输出最优模型下测试集的AUC值和Recall
y_prob_best = grid_search.best_estimator_.predict_proba(X_test)[:, 1]  # best_estimator_ predict

# 计算AUC
fpr, tpr, threshold = roc_curve(y_score=y_prob_best, y_true=y_test)
pred_best_auc = auc(fpr, tpr)
print("AUC值：", pred_best_auc)


# In[ ]:




