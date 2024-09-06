#!/usr/bin/env python
# coding: utf-8

# # 实战
# ## 导入sklean包

# In[23]:


from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, KFold, RepeatedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler as std
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import f1_score


# ## datasets 模块

# |名字|	导入方法	|介绍	|任务	|数据规模|
# |---|---|---|---|---|
# |波士顿房价|	load_boston(return_X_y=False)|加载和返回一个boston房屋价格的数据集|	回归	|506 x 13|
# |乳腺癌	|load_breast_cancer(return_X_y=False)	|加载和返回一个乳腺癌“恶性/良性”（1/0）类别型数据集	|二分类|	569 x 30|
# |糖尿病	|load_diabetes(return_X_y=False)	|加载和返回一个糖尿病数据集	|回归|	442 x 10|
# |手写数据	|load_digits(return_X_y=False)	|加载和返回一个手写图片数据集	|多分类	|1797 x 64|
# |鸢尾花|	load_iris(return_X_y=False)	|加载和返回一个鸢尾花数据集	|多分类|	150 x 4|
# |红酒	|load_wine(return_X_y=False)	|加载和返回一个红酒数据集	|多分类|	178 x 13|
# |体能训练	|load_linnerud(return_X_y=False)	|加载和返回健身数据集|	回归|	20 x 3|
# 

# ## 手写数据

# In[24]:


from sklearn import datasets
digits_data = datasets.load_digits()

# print(digits_data.DESCR)    			# 描述
print(dir(digits_data),'\n')            # 数据集对象所含的成员 
print(digits_data.data.shape,'\n')      # 样本集形状
print(digits_data.target.shape,'\n')    # 标签集形状
print(digits_data.data[:1],'\n')        # 第一个数据
print(digits_data.target[:1],'\n')      # 第一个标签
print(digits_data.feature_names,'\n')   # 特征名
print(digits_data.target_names,'\n')    # 标签名
print(digits_data.images[:1],'\n')      # 以8x8形式显示图片数据，其实就是带格式的data


# In[25]:


X, y = datasets.load_digits(return_X_y = True)  # 独立导出数据集
print(X.shape)       
print(y.shape)


# In[29]:


from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import numpy as np

n_samples,n_features=digits_data.data.shape
fig = plt.figure(figsize=(6,6))
fig.subplots_adjust(left=0,right=1,bottom=0,top=1,hspace=0.05,wspace=0.05)

#绘制数字：每张图像8*8像素点
for i in range(64):
    ax = fig.add_subplot(8,8,i+1,xticks=[],yticks=[])
    ax.imshow(digits_data.images[i],cmap=plt.cm.binary,interpolation='nearest')
    #用目标值标记图像
    ax.text(0,7,str(digits_data.target[i]))
plt.show()


# ## 特征选择 - 鸢尾花

# In[16]:


from sklearn import datasets 
iris = datasets.load_iris()
iris


# ### Filter过滤法
# 

# 方差选择法 VarianceThreshold

# 方差越大的特征，那么我们可以认为它是比较有用的。如果方差较小，比如小于1，那么这个特征可能对我们的算法作用没有那么大。最极端的，如果某个特征方差为0，即所有的样本该特征的取值都是一样的，那么它对我们的模型训练没有任何作用，可以直接舍弃。

# ||阈值很小被过滤掉得特征比较少|阈值比较大被过滤掉的特征有很多|
# |---|---|---|
# |模型表现|不会有太大影响|可能变更好，代表被滤掉的特征大部分是噪音也可能变糟糕，代表被滤掉的特征中很多都是有效特征|
# |运行时间|可能降低模型的运行时间基于方差很小的特征有多少当方差很小的特征不多时对模型没有太大影响|一定能够降低模型的运行时间算法在遍历特征时的计算越复杂，运行时间下降得越多|
# 

# In[19]:


from sklearn.feature_selection import VarianceThreshold
#方差选择法，返回值为特征选择后的数据 
#参数threshold为方差的阈值
vardata = VarianceThreshold(threshold=1).fit_transform(iris.data) 
print(vardata[:10])  # 每一行的var


# ### SelectKBest

# In[11]:


from sklearn.feature_selection import SelectKBest 
from scipy.stats import pearsonr 
import numpy as np
#选择K个最好的特征，返回选择特征后的数据
#第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，
#输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。
#在此定义为计算相关系数 
f = lambda X, Y:np.array(list(map(lambda x:pearsonr(x, Y)[0], X.T))).T
#参数k为选择的特征个数
SelectKBest(f,k=2).fit_transform(iris.data, iris.target)[:10] 


# In[12]:


iris.feature_names


# In[13]:


iris.data[:10] 


# ### Wrapper包装法

# 递归消除特征法使用一个基模型来进行多轮训练，每轮训练后，消除若干权值系数的特征，再基于新的特征集进行下一轮训练。
# 

# In[15]:


from sklearn.feature_selection import RFE 
from sklearn.linear_model import LogisticRegression
#递归特征消除法，返回特征选择后的数据 
#参数estimator为基模型 
#参数n_features_ to_select为选择的特征个数
RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(iris.data, iris.target)[:10]


# ### Embedded嵌入法

# In[40]:


from sklearn.feature_selection import SelectFromModel 
from sklearn.ensemble import GradientBoostingClassifier
#GBDT作为基模型的特征选择 
SelectFromModel(GradientBoostingClassifier()).fit_transform(iris.data, iris.target)[:10]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




