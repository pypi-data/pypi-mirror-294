#!/usr/bin/env python
# coding: utf-8

# In[1]:


import  torch


# # conv2d接口

# ```
# torch.nn.Conv2d(
# 	in_channels, 
# 	out_channels, 
# 	kernel_size, 
# 	stride=1, 
# 	padding=0, 
# 	dilation=1, 
# 	groups=1, 
# 	bias=True, 
# 	padding_mode='zeros', 
# 	device=None, 
# 	dtype=None
# )
# ```

# In[ ]:





# ### 2. 参数解释
# 
# in_channels：输入的通道数，RGB 图像的输入通道数为 3
# 
# out_channels：输出的通道数
# 
# kernel_size：卷积核的大小，一般我们会使用 5x5、3x3 这种左右两个数相同的卷积核，因此这种情况只需要写 kernel_size = 5这样的就行了。如果左右两个数不同，比如3x5的卷积核，那么写作kernel_size = (3, 5)，注意需要写一个 tuple，而不能写一个 list。
# 
# stride = 1：卷积核在图像窗口上每次平移的间隔，即所谓的步长。
# 
# padding：指图像填充，后面的int型常数代表填充的多少（行数、列数），默认为0。需要注意的是这里的填充包括图像的上下左右，以padding=1为例，若原始图像大小为[32, 32]，那么padding后的图像大小就变成了[34, 34]
# 
# dilation：是否采用空洞卷积，默认为1（不采用）。从中文上来讲，这个参数的意义从卷积核上的一个参数到另一个参数需要走过的距离，那当然默认是1了，毕竟不可能两个不同的参数占同一个地方吧（为0）。更形象和直观的图示可以观察Github上的Dilated convolution animations，展示了dilation=2的情况。
# 
# groups：决定了是否采用分组卷积，groups参数可以参考groups参数详解
# 
# bias：即是否要添加偏置参数作为可学习参数的一个，默认为True。
# 
# padding_mode：即padding的模式，默认采用零填充。
# 

# ### 3. 尺寸关系
# 
# ![image.png](attachment:502c555b-9ed5-4bfb-b60c-48a65fa52f3f.png)
# 

# 参考：
# 
# - https://blog.csdn.net/AI_dataloads/article/details/133250229
# - https://blog.csdn.net/See_Star/article/details/127560160
# - 扩张卷积： https://blog.csdn.net/chaipp0607/article/details/99671483

# In[27]:


inputs = torch.randn((3, 5, 5))


# In[28]:


inputs.shape


# In[29]:


conv = torch.nn.Conv2d(
	in_channels = 3, 
	out_channels = 2, 
	kernel_size = (3,3), 
	stride=2, 
	padding=1, 
	dilation=1, 
	groups=1, 
	bias=True, 
	padding_mode='zeros', 
)


# In[30]:


o = conv(inputs)


# In[31]:


o.shape


# In[ ]:





# In[32]:


conv = torch.nn.Conv2d(
	in_channels = 3, 
	out_channels = 2, 
	kernel_size = (3,3), 
	stride=2, 
	padding=1, 
	dilation=2, 
	groups=1, 
	bias=True, 
	padding_mode='zeros', 
)


# In[33]:


o = conv(inputs)


# In[34]:


o.shape


# In[ ]:




