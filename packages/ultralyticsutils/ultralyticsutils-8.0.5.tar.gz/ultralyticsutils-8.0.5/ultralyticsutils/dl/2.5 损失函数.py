#!/usr/bin/env python
# coding: utf-8

# # 2.5 损失函数losses

# 在深度学习广为使用的今天，我们可以在脑海里清晰的知道，一个模型想要达到很好的效果需要**学习**，也就是我们常说的训练。一个好的训练离不开优质的负反馈，这里的损失函数就是模型的负反馈。
# 
# 
# 
# 所以在PyTorch中，损失函数是必不可少的。它是数据输入到模型当中，产生的结果与真实标签的评价指标，我们的模型可以按照损失函数的目标来做出改进。
# 
# 下面我们将开始探索PyTorch的所拥有的损失函数。这里将列出PyTorch中常用的损失函数（一般通过torch.nn调用），并详细介绍每个损失函数的功能介绍、数学公式和调用代码。当然，PyTorch的损失函数还远不止这些，在解决实际问题的过程中需要进一步探索、借鉴现有工作，或者设计自己的损失函数。
# 
# 

# 常用的一些内置损失函数说明如下。
# 
# * nn.MSELoss（均方误差损失，也叫做L2损失，用于回归）
# 
# * nn.L1Loss （L1损失，也叫做绝对值误差损失，用于回归）
# 
# * nn.SmoothL1Loss (平滑L1损失，当输入在-1到1之间时，平滑为L2损失，用于回归)
# 
# * nn.BCELoss (二元交叉熵，用于二分类，输入已经过nn.Sigmoid激活，对不平衡数据集可以用weigths参数调整类别权重)
# 
# * nn.BCEWithLogitsLoss (二元交叉熵，用于二分类，输入未经过nn.Sigmoid激活)
# 
# * nn.CrossEntropyLoss (交叉熵，用于多分类，要求label为稀疏编码，输入未经过nn.Softmax激活，对不平衡数据集可以用weigths参数调整类别权重)
# 
# * nn.NLLLoss (负对数似然损失，用于多分类，要求label为稀疏编码，输入经过nn.LogSoftmax激活)
# 
# * nn.KLDivLoss (KL散度损失，也叫相对熵，等于交叉熵减去信息熵，用于标签为概率值的多分类，要求输入经过nn.LogSoftmax激活)
# 
# * nn.CosineSimilarity(余弦相似度，可用于多分类)
# 
# * nn.AdaptiveLogSoftmaxWithLoss (一种适合非常多类别且类别分布很不均衡的损失函数，会自适应地将多个小类别合成一个cluster)

# In[1]:


import torch
import torch.nn as nn


# ## 2.5.1 二分类交叉熵损失函数

# In[2]:


torch.nn.BCELoss(weight=None, size_average=None, reduce=None, reduction='mean')


# 
# **功能**：计算二分类任务时的交叉熵（Cross Entropy）函数。
# 
# **主要参数**：
# 
# `weight`:每个类别的loss设置权值
# 
# `size_average`:数据为bool，为True时，返回的loss为平均值；为False时，返回的各样本的loss之和。
# 
# `reduce`:数据类型为bool，为True时，loss的返回是标量。
# 
# 计算公式如下：
# $
# \ell(x, y)=\left\{\begin{array}{ll}
# \operatorname{mean}(L), & \text { if reduction }=\text { 'mean' } \\
# \operatorname{sum}(L), & \text { if reduction }=\text { 'sum' }
# \end{array}\right.
# $

# In[3]:


m = nn.Sigmoid()
loss = nn.BCELoss()


# In[4]:


input = torch.randn(3, requires_grad=True)


# In[5]:


input


# In[6]:


target = torch.empty(3).random_(2)


# In[7]:


target


# In[8]:


m(input)


# In[ ]:





# In[9]:


output = loss(m(input), target)
print('BCELoss损失函数的计算结果为',output)


# In[10]:


output.backward()  #反向传播，计算当前梯度
print('BCELoss损失函数的计算结果为',output)


# In[11]:


m = nn.Sigmoid()
loss = nn.BCELoss()
input = torch.randn(3)
target = torch.empty(3).random_(2)
output = loss(m(input), target)
print('BCELoss损失函数的计算结果为',output)


# ## 2.5.2 交叉熵损失函数

# In[12]:


torch.nn.CrossEntropyLoss(weight=None, size_average=None, ignore_index=-100, reduce=None, reduction='mean')


# **功能**：计算交叉熵函数
# 
# **主要参数**：  
# 
# `weight`:每个类别的loss设置权值。
# 
# `size_average`:数据为bool，为True时，返回的loss为平均值；为False时，返回的各样本的loss之和。
# 
# `ignore_index`:忽略某个类的损失函数。
# 
# `reduce`:数据类型为bool，为True时，loss的返回是标量。
# 
# 计算公式如下：
# $
# \operatorname{loss}(x, \text { class })=-\log \left(\frac{\exp (x[\text { class }])}{\sum_{j} \exp (x[j])}\right)=-x[\text { class }]+\log \left(\sum_{j} \exp (x[j])\right)
# $
# 
# 

# In[13]:


loss = nn.CrossEntropyLoss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.empty(3, dtype=torch.long).random_(5)
output = loss(input, target)
output.backward()
print(output)


# ## 2.5.3 L1损失函数

# In[14]:


torch.nn.L1Loss(size_average=None, reduce=None, reduction='mean')


# 
# **功能：** 计算输出`y`和真实标签`target`之间的差值的绝对值。
# 
# 我们需要知道的是，`reduction`参数决定了计算模式。有三种计算模式可选：none：逐个元素计算。
# sum：所有元素求和，返回标量。
# mean：加权平均，返回标量。 
# 如果选择`none`，那么返回的结果是和输入元素相同尺寸的。默认计算方式是求平均。
# 
# **计算公式如下：**
# $
# L_{n} = |x_{n}-y_{n}|
# $
# 

# In[15]:


loss = nn.L1Loss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.randn(3, 5)
output = loss(input, target)
output.backward()

print('L1损失函数的计算结果为',output)


# In[ ]:





# ## 2.5.4 MSE损失函数

# In[16]:


torch.nn.MSELoss(size_average=None, reduce=None, reduction='mean')


# **功能：** 计算输出`y`和真实标签`target`之差的平方。
# 
# 和`L1Loss`一样，`MSELoss`损失函数中，`reduction`参数决定了计算模式。有三种计算模式可选：none：逐个元素计算。
# sum：所有元素求和，返回标量。默认计算方式是求平均。
# 
# **计算公式如下：**
# 
# $
# l_{n}=\left(x_{n}-y_{n}\right)^{2}
# $

# In[17]:


loss = nn.MSELoss()
input = torch.randn(3, 5, requires_grad=True)
target = torch.randn(3, 5)
output = loss(input, target)
output.backward()
print('MSE损失函数的计算结果为',output)


# 

# ## 2.5.5 余弦相似度
# ```python
# torch.nn.CosineEmbeddingLoss(margin=0.0, size_average=None, reduce=None, reduction='mean')
# ```
# **功能：** 对两个向量做余弦相似度
# 
# **主要参数:** 
# 
# 
# `reduction`：计算模式，可为 none/sum/mean。
# 
# 
# 
# `margin`：可取值[-1,1] ，推荐为[0,0.5] 。
# 
# 
# **计算公式：**
# 
# $
# \operatorname{loss}(x, y)=\left\{\begin{array}{ll}
# 1-\cos \left(x_{1}, x_{2}\right), & \text { if } y=1 \\
# \max \left\{0, \cos \left(x_{1}, x_{2}\right)-\text { margin }\right\}, & \text { if } y=-1
# \end{array}\right.
# $
# 其中,
# $
# \cos (\theta)=\frac{A \cdot B}{\|A\|\|B\|}=\frac{\sum_{i=1}^{n} A_{i} \times B_{i}}{\sqrt{\sum_{i=1}^{n}\left(A_{i}\right)^{2}} \times \sqrt{\sum_{i=1}^{n}\left(B_{i}\right)^{2}}}
# $
# 
# 
# 这个损失函数应该是最广为人知的。对于两个向量，做余弦相似度。将余弦相似度作为一个距离的计算方式，如果两个向量的距离近，则损失函数值小，反之亦然。
# 

# In[18]:


loss_f = nn.CosineEmbeddingLoss()
inputs_1 = torch.tensor([[0.3, 0.5, 0.7], [0.3, 0.5, 0.7]])
inputs_2 = torch.tensor([[0.1, 0.3, 0.5], [0.1, 0.3, 0.5]])
target = torch.tensor([1, -1], dtype=torch.float)
output = loss_f(inputs_1,inputs_2,target)

print('CosineEmbeddingLoss损失函数的计算结果为',output)


# ## 2.5.6 KL散度
# ```python
# torch.nn.KLDivLoss(size_average=None, reduce=None, reduction='mean', log_target=False)
# ```
# **功能：** 计算KL散度，也就是计算相对熵。用于连续分布的距离度量，并且对离散采用的连续输出空间分布进行回归通常很有用。
# 
# **主要参数:** 
# 
# `reduction`：计算模式，可为 `none`/`sum`/`mean`/`batchmean`。
# 
#     none：逐个元素计算。
#     
#     sum：所有元素求和，返回标量。
#     
#     mean：加权平均，返回标量。
#     
#     batchmean：batchsize 维度求平均值。
# 
# **计算公式：**
# 
# $
# \begin{aligned}
# D_{\mathrm{KL}}(P, Q)=\mathrm{E}_{X \sim P}\left[\log \frac{P(X)}{Q(X)}\right] &=\mathrm{E}_{X \sim P}[\log P(X)-\log Q(X)] \\
# &=\sum_{i=1}^{n} P\left(x_{i}\right)\left(\log P\left(x_{i}\right)-\log Q\left(x_{i}\right)\right)
# \end{aligned}
# $
# 

# In[19]:


inputs = torch.tensor([[0.5, 0.3, 0.2], [0.2, 0.3, 0.5]])
target = torch.tensor([[0.9, 0.05, 0.05], [0.1, 0.7, 0.2]], dtype=torch.float)
loss = nn.KLDivLoss()
output = loss(inputs,target)

print('KLDivLoss损失函数的计算结果为',output)


# ## 2.5.7 MarginRankingLoss

# ```python
# torch.nn.MarginRankingLoss(margin=0.0, size_average=None, reduce=None, reduction='mean')
# ```
# **功能：** 计算两个向量之间的相似度，用于排序任务。该方法用于计算两组数据之间的差异。
# 
# **主要参数:** 
# 
# `margin`：边界值，$x_{1}$ 与$x_{2}$ 之间的差异值。
# 
# `reduction`：计算模式，可为 none/sum/mean。
# 
# **计算公式：**
# 
# $
# \operatorname{loss}(x 1, x 2, y)=\max (0,-y *(x 1-x 2)+\operatorname{margin})
# $
# 
# 

# In[20]:


loss = nn.MarginRankingLoss()
input1 = torch.randn(3, requires_grad=True)
input2 = torch.randn(3, requires_grad=True)
target = torch.randn(3).sign()
output = loss(input1, input2, target)
output.backward()

print('MarginRankingLoss损失函数的计算结果为',output)

