#!/usr/bin/env python
# coding: utf-8

# # 2.7 PyTorch优化器
# 
# 深度学习的目标是通过不断改变网络参数，使得参数能够对输入做各种非线性变换拟合输出，本质上就是一个函数去寻找最优解，只不过这个最优解是一个矩阵，而如何快速求得这个最优解是深度学习研究的一个重点，以经典的resnet-50为例，它大约有2000万个系数需要进行计算，那么我们如何计算出这么多系数，有以下两种方法：
# 
# 1. 第一种是直接暴力穷举一遍参数，这种方法从理论上行得通，但是实施上可能性基本为0，因为参数量过于庞大。
# 2. 为了使求解参数过程更快，人们提出了第二种办法，即BP+优化器逼近求解。
# 
# 因此，优化器是根据网络反向传播的梯度信息来更新网络的参数，以起到降低loss函数计算值，使得模型输出更加接近真实标签。
# 
# 

# 
# 
# 
# ## 2.7.1 PyTorch提供的优化器
# 
# PyTorch很人性化的给我们提供了一个优化器的库`torch.optim`，在这里面提供了多种优化器。
# 
# + torch.optim.SGD 
# + torch.optim.ASGD
# + torch.optim.Adadelta
# + torch.optim.Adagrad
# + torch.optim.Adam
# + torch.optim.AdamW
# + torch.optim.Adamax
# + torch.optim.RAdam
# + torch.optim.NAdam
# + torch.optim.SparseAdam
# + torch.optim.LBFGS
# + torch.optim.RMSprop
# + torch.optim.Rprop
# 

# 1. 每个优化器都是一个类，我们一定要进行实例化才能使用，比如下方实现：
# 
#     ```python
#     class Net(nn.Moddule):
#         ···
#     net = Net()
#     optim = torch.optim.SGD(net.parameters(),lr=lr)
#     optim.step()
#     ```
# 
# 2. optimizer在一个神经网络的epoch中需要实现下面两个步骤：
#    1. 梯度置零
#    2. 梯度更新
# 
#     ```python
#     optimizer = torch.optim.SGD(net.parameters(), lr=1e-5)
#     for epoch in range(EPOCH):
#         ...
#         optimizer.zero_grad()  #梯度置零
#         loss = ...             #计算loss
#         loss.backward()        #BP反向传播
#         optimizer.step()       #梯度更新
#     ```
# 3. 给网络不同的层赋予不同的优化器参数。
# 
#     ```python
#     from torch import optim
#     from torchvision.models import resnet18
# 
#     net = resnet18()
# 
#     optimizer = optim.SGD([
#         {'params':net.fc.parameters()},#fc的lr使用默认的1e-5
#         {'params':net.layer4[0].conv1.parameters(),'lr':1e-2}],lr=1e-5)
# 
#     # 可以使用param_groups查看属性
#     ```

# In[2]:


from torch import optim
from torchvision.models import resnet18

net = resnet18()


# In[3]:


for ind,i in net.state_dict().items():
    print (ind,i.shape)


# In[5]:


optimizer = optim.SGD([
    {'params':net.fc.parameters()},#fc的lr使用默认的1e-5
    {'params':net.layer4[0].conv1.parameters(),'lr':1e-2}],lr=1e-5)


# In[ ]:





# 
