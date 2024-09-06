#!/usr/bin/env python
# coding: utf-8

#  数据集redcard.csv.gz为某俱乐部2012-2013年间的球赛比赛数据，含球员2053名，裁判3147名，特征列表如下：
# 
# | Variable Name: | Variable Description: | 
# | -- | -- | 
# | playerShort | short player ID | 
# | player | player name | 
# | club | player club | 
# | leagueCountry | country of player club (England, Germany, France, and Spain) | 
# | height | player height (in cm) | 
# | weight | player weight (in kg) | 
# | position | player position | 
# | games | number of games in the player-referee dyad | 
# | goals | number of goals in the player-referee dyad | 
# | yellowCards | number of yellow cards player received from the referee | 
# | yellowReds | number of yellow-red cards player received from the referee | 
# | redCards | number of red cards player received from the referee | 
# | photoID | ID of player photo (if available) | 
# | rater1 | skin rating of photo by rater 1 | 
# | rater2 | skin rating of photo by rater 2 | 
# | refNum | unique referee ID number (referee name removed for anonymizing purposes) | 
# | refCountry | unique referee country ID number | 
# | meanIAT | mean implicit bias score (using the race IAT) for referee country | 
# | nIAT | sample size for race IAT in that particular country | 
# | seIAT | standard error for mean estimate of race IAT   | 
# | meanExp | mean explicit bias score (using a racial thermometer task) for referee country | 
# | nExp | sample size for explicit bias in that particular country | 
# | seExp |  standard error for mean estimate of explicit bias measure | 
# 
# 请对该数据集进行一下探索性分析，寻找裁判与球员间的故事：  
# 

# import numpy as np
# import pandas as pd

# ## 读入数据集，并查看其形状、详细描述、以及字段信息

# In[2]:


#读入数据集，解码格式为gzip。1+2分
import numpy as np
import pandas as pd
df = pd.read_csv("redcard.csv.gz", compression='gzip')  # read_csv compression


# In[3]:


#查看形状信息。 2分
df.shape


# In[4]:


#查看前几行
df.head()


# In[7]:


#查看每个特征的统计信息，4分
df.describe().T  # describe() T


# In[13]:


#查看每个字段类型。 2分
df.dtypes  # dytpes


# In[14]:


#将数据集字段信息转换为列表。2分
all_columns = df.columns.tolist() #  tolist
all_columns


# ## 统计每个player在2012-2013年间的平均体重

# In[16]:


## 4分
df.groupby('playerShort').weight.mean() # goupby mean


# ## 统计每个player的'birthday','height','weight','position','photoID','rater1','rater2特征有多少不同值

# In[20]:


#取出相关列
player_index = 'playerShort'
player_cols = ['birthday',
               'height',
               'weight',
               'position',
               'photoID',
               'rater1',
               'rater2',
              ]


# In[22]:


#统计每个player的'birthday','height','weight','position','photoID','rater1','rater2特征有多少不同值。 4分
all_cols_unique_players = df.groupby(player_index).agg({col:'nunique' for col in player_cols})  # groupby agg


# In[51]:


all_cols_unique_players.head()


# ## 查看每个player的'birthday','height','weight','position','photoID','rater1','rater2中不同值大于1的特征有多少个

# In[58]:


all_cols_unique_players[all_cols_unique_players > 1].dropna().shape[0]


# ## 查看每个player的'birthday','height','weight','position','photoID','rater1','rater2'中的最大值

# In[25]:


## 4分
df.groupby(player_index).agg({col:'max' for col in player_cols})  # groupby agg


# In[ ]:




