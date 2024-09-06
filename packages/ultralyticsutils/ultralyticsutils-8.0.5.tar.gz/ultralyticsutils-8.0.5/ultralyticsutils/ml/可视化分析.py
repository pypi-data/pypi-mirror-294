#!/usr/bin/env python
# coding: utf-8

#  

# # 可视化分析
# 
# ## 一、 背景介绍
# 数据集由480个学生记录和16个特征组成。这些特征分为三大类：
# 
# （1）性别和国籍等人口统计特征。  
# （2）学历背景特征，如教育阶段，年级和隶属教室。  
# （3）行为特征，如上课举手，访问资源，家长回答问卷调查，学校满意度等。
# 
# 数据集收集来自两个学期：第一学期收集了245个学生记录，第二学期收集了235个学生记录。最后学生依据其总成绩被分为三类： 低：0-69、中：70-89、高：90-100。我们的任务是根据收集的数据预测学生的成绩等级。

# ### 字段说明
# <img src="./img/分类字段说明.png" width = "700" height = "500" alt="图片名称" align=left />  

# # 一、课程目的
# 1. 熟悉一些pandas、numpy的操作；
# 2. 强调可视化分析是机器学习的一部分
# 3. 强调探索性数据分析的重要。

# ## 二、 可视化数据分析
#     主要包括两小块：读取数据；可视化分析【分析是否存在严重类别不平衡问题、分析变量与目标变量之间的关系，为构建模型做铺垫】。

# ### 2.1 数据读取

# In[1]:


import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


# In[2]:


df = pd.read_csv('data/StudentPerformance.csv') # 读取 csv 数据
df.head(10) # 查看前十行数据


# In[4]:


df.isnull().sum() # 查看数据是否缺失


# In[5]:


df.dtypes # 检查数据类型[有些数据是离散数值型的，需要和字符型字段区分开]。


# In[6]:


# 查看数据详细信息
df.describe(include='all')


# - 列名命名方式统一
# - 为方便我们统一，采用“大驼峰命名法”，改为首字母大写，其余小写。 

# In[7]:


# 修改列名
df.rename(index=str, columns={'gender':'Gender',
                              'NationalITy':'Nationality',
                              'raisedhands':'RaisedHands', 
                              'VisITedResources':'VisitedResources'}, inplace=True)


# In[8]:


df.head()


# ### 2.2 可视化分析
# 
# > 1. countplot：条形图
# - swarmplot：分簇散点图
# - boxplot：箱型图
# - heatmap：热力图 - 相关系数为例
# 

# #### countplot
# - 成绩等级的数量分布条形图

# In[9]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[10]:


df


# In[11]:


## 绘制条形图
sns.countplot(x='Class', order=['L','M','H'], data=df) # 检查数据集是否平衡


# 结论：虽然成绩中等的学生要比其余两个成绩等级的学生多一些，但数据集不存在明显的类别分布极端不平衡情况。

# - 不同学期，学生成绩等级的数量分布差异分析

# In[12]:


## 分类别绘制条形图
plt.figure(figsize=(8, 6))
sem = sns.countplot(x='Class', hue='Semester', order=['L', 'M', 'H'], data=df)
sem.set(xlabel='Class', ylabel='Count', title='Semester comparison')
plt.show()


# ### 结论  
#     学生在第一学期（F）的表现比第二学期（S）差一些【在第二学期，成绩中等的学生人数保持不变，但是成绩差的学生人数较少，而成绩好的学生人数较多】。

# - 性别对学生成绩的影响

# In[13]:


## 绘制条形图
plt.figure(figsize=(8, 6))
plot = sns.countplot(x='Class', hue='Gender', data=df, order=['L', 'M', 'H'], palette='coolwarm')
plot.set(xlabel='Class', ylabel='Count', title='Gender comparison')
plt.show()


# 学生中男生较多，并且与女生对比而言，男生低分成绩的人较多，高分成绩的人较少。

# #### swarmplot
# < 数据点不重叠的分类散点图 >
# - 不同性别下, 访问在线资源和成绩的相关性

# In[14]:


df['Gender'].value_counts()


# In[15]:


sns.set(rc={'figure.figsize': (15,10)})
sns.swarmplot(x='Class', y='VisitedResources', hue='Gender', palette='coolwarm', data=df, order=['L','M','H'])


# 1. 获得低分（L）的学生比获得中等分数（M）或高分（H）的学生访问的资源少的多。  
# 2. 获得高分（H）的女性几乎都访问了很多在线资源。

# #### boxplot
# < 显示一组数据分散情况 >
# - 上课讨论积极程度和成绩的关系
# 
# <img src="./img/boxplot.png" width = "700" height = "500" alt="图片名称" align=left />  
# IQR：四分位差也叫做四分位距，中间50%的数值的离散程度，差值越小，数据越集中

# In[16]:


sns.set(rc={'figure.figsize': (8,6)})
sns.boxplot(x='Class', y='Discussion', data=df, order=['L','M','H'])


# In[17]:


plt.figure(figsize=(15,6))
sns.boxplot(x='Class', y='Discussion', hue='Semester', data=df, order=['L','M','H'], width=0.5)


# #### heatmap
# - 相关性矩阵

# In[18]:


df.dtypes[ df.dtypes!=np.object ]


# In[19]:


corrDf = df[['RaisedHands','VisitedResources','AnnouncementsView','Discussion']].corr()
corrDf


# In[20]:


#绘制热力图
f, (ax) = plt.subplots(figsize = (8, 6))
sns.heatmap(corrDf, annot = True, cmap='YlGnBu');
ax.set_xticklabels(ax.get_xticklabels(), rotation=20)


# #### 全特征相关性绘图

# In[21]:


df = pd.read_csv('data/StudentPerformance.csv') # 读取 csv 数据

# 修改列名
df.rename(index=str, columns={'gender':'Gender',
                              'NationalITy':'Nationality',
                              'raisedhands':'RaisedHands', 
                              'VisITedResources':'VisitedResources'}, inplace=True)

df.head(10) # 查看前十行数据


# ### 将连续型变量与非连续型变量数据分开？

# In[27]:


# 离散型变量
df1 = df[ df.dtypes[ df.dtypes== object ].index ]
df2 = df[ df.dtypes[ df.dtypes!= object ].index ]


# In[28]:


df2


# In[29]:


X1 = df1.drop('Class', axis=1)
X1 = pd.get_dummies(X1) # 将所有的分类型特征转换为数字, 虚拟变量: dummy variables
X1.head(5)


# In[30]:


corrX = X1.corr()
corrX.head()
# sns.heatmap


# In[33]:


f, (ax) = plt.subplots(figsize = (25, 16))

cmap = sns.diverging_palette(220, 10, as_cmap=True) # 生成蓝-白-红的颜色列表
mask = np.zeros_like(corrX, dtype= bool) # 返回与相关性矩阵具有相同形状和类型的零数组作为掩码
mask[np.triu_indices_from(mask)] = True # 给相关性矩阵的上三角阵生成掩码

# sns.set(font_scale=1.5)
# 绘制热力图
sns.heatmap(corrX, annot = False, cmap='CMRmap_r', mask=mask, linewidths=.5);
ax.set_xticklabels(ax.get_xticklabels(), rotation=60)


# #### 结论
#     Nationality【国籍】与PlaceofBirth【出生地】相关性非常强。

# <br>
# <br>
# ## 基于boxplot进一步聊聊异常值问题！！！
# <br>

# In[ ]:





# In[ ]:





# In[ ]:




