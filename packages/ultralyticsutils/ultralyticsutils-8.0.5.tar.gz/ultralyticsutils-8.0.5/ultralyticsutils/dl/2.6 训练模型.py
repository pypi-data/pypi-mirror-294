#!/usr/bin/env python
# coding: utf-8

# # 6-2 训练模型
# 
# 

# In[ ]:





# In[1]:


import torch 
print("torch.__version__ = ", torch.__version__)


# In[ ]:





# ### 一、准备数据

# In[2]:


import torch 
from torch import nn 

import torchvision 
from torchvision import transforms


# In[3]:


# 定义数据转换操作：将图像转换为张量
transform = transforms.Compose([transforms.ToTensor()])

# 加载MNIST训练数据集，自动下载并应用上述定义的转换
ds_train = torchvision.datasets.MNIST(root="./data/mnist/", train=True, download=True, transform=transform)
# 加载MNIST验证数据集，自动下载并应用上述定义的转换
ds_val = torchvision.datasets.MNIST(root="./data/mnist/", train=False, download=True, transform=transform)

# 创建训练数据的DataLoader，设置批大小为128，打乱顺序，并设置4个工作进程
train_dataloader = torch.utils.data.DataLoader(ds_train, batch_size=128, shuffle=True, num_workers=4)
# 创建验证数据的DataLoader，设置批大小为128，不打乱顺序，并设置4个工作进程
val_dataloader = torch.utils.data.DataLoader(ds_val, batch_size=128, shuffle=False, num_workers=4)

# 打印训练集和验证集的样本数
print(len(ds_train))
print(len(ds_val))


# In[4]:


ds_train[0][0].shape


# ### 二, 模型定义

# 脚本风格的训练循环非常常见。

# In[6]:


model = nn.Sequential()
model.add_module("conv1",nn.Conv2d(in_channels=1,out_channels=32,kernel_size = 3))
model.add_module("pool1",nn.MaxPool2d(kernel_size = 2,stride = 2))
model.add_module("conv2",nn.Conv2d(in_channels=32,out_channels=64,kernel_size = 5))
model.add_module("pool2",nn.MaxPool2d(kernel_size = 2,stride = 2))
model.add_module("dropout",nn.Dropout2d(p = 0.1))
model.add_module("adaptive_pool",nn.AdaptiveMaxPool2d((1,1)))
model.add_module("flatten",nn.Flatten())
model.add_module("linear1",nn.Linear(64,32))
model.add_module("relu",nn.ReLU())
model.add_module("linear2",nn.Linear(32,10))

print(model)


# ### 三, 训练模型

# 完成了上述设定后就可以加载数据开始训练模型了。首先应该设置模型的状态：如果是训练状态，那么模型的参数应该支持反向传播的修改；如果是验证/测试状态，则不应该修改模型参数。在PyTorch中，模型的状态设置非常简便，如下的两个操作二选一即可：
# 
# ```python
# model.train()   # 训练状态
# model.eval()   # 验证/测试状态
# ```
# 
# 我们前面在DataLoader构建完成后介绍了如何从中读取数据，在训练过程中使用类似的操作即可，区别在于此时要用for循环读取DataLoader中的全部数据。
# 
# ```python
# for data, label in train_dataloader:
# ```
# 
# 之后将数据放到GPU上用于后续计算，此处以.cuda()为例
# 
# ```python
# data, label = data.cuda(), label.cuda()
# ```
# 
# 开始用当前批次数据做训练时，应当先将优化器的梯度置零：
# 
# ```python
# optimizer.zero_grad()
# ```
# 
# 之后将data送入模型中训练：
# 
# ```python
# output = model(data)
# ```
# 
# 根据预先定义的criterion计算损失函数：
# 
# ```python
# loss = criterion(output, label)
# ```
# 
# 将loss反向传播回网络：
# 
# ```python
# loss.backward()
# ```
# 
# 使用优化器更新模型参数：
# 
# ```python
# optimizer.step()
# ```

# In[ ]:





# 

# 
# 验证/测试的流程基本与训练过程一致，不同点在于：
# 
# - 需要预先设置torch.no_grad，以及将model调至eval模式
# - 不需要将优化器的梯度置零
# - 不需要将loss反向回传到网络
# - 不需要更新optimizer
# 
# 一个完整的图像分类的训练过程如下所示：
# 
# ```python
# def train(epoch):
#     model.train()
#     train_loss = 0
#     for data, label in train_dataloader:
#         data, label = data.cuda(), label.cuda()
#         optimizer.zero_grad()
#         output = model(data)
#         loss = criterion(output, label)
#         loss.backward()
#         optimizer.step()
#         train_loss += loss.item()*data.size(0)
#     train_loss = train_loss/len(train_dataloader.dataset)
# 	print('Epoch: {} \tTraining Loss: {:.6f}'.format(epoch, train_loss))
# 
# ```
# 
# 对应的，一个完整图像分类的验证过程如下所示：
# 
# ```python
# def val(epoch):       
#     model.eval()
#     val_loss = 0
#     with torch.no_grad():
#         for data, label in val_dataloader:
#             data, label = data.cuda(), label.cuda()
#             output = model(data)
#             preds = torch.argmax(output, 1)
#             loss = criterion(output, label)
#             val_loss += loss.item()*data.size(0)
#             running_accu += torch.sum(preds == label.data)
#     val_loss = val_loss/len(val_dataloader.dataset)
#     print('Epoch: {} \tVal Loss: {:.6f}'.format(epoch, val_loss))
# ```

# In[ ]:





# In[ ]:





# In[7]:


model = model.to('cuda')


# In[8]:


criterion = nn.CrossEntropyLoss()
optimizer= torch.optim.Adam(model.parameters(),lr = 0.01)   

epochs = 20 
ckpt_path='checkpoint.pt'


for epoch in range(1, epochs+1):
    print("Epoch {0} / {1}".format(epoch, epochs))

    # 1，train -------------------------------------------------  
    
    model.train()
    train_loss = 0 #metrics
    for data, label in train_dataloader:
        data, label = data.to('cuda'), label.to('cuda')
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, label)
        loss.backward()
        optimizer.step()

        ####################
        train_loss += loss.item()*data.size(0)
    train_loss = train_loss/len(train_dataloader.dataset)
    #acc
    #pre
    #
    print('Epoch: {} \t Training Loss: {:.6f}'.format(epoch, train_loss))
    
    model.eval()
    val_loss = 0
    running_accu  = 0
    with torch.no_grad():
        for data, label in val_dataloader:
            data, label = data.cuda(), label.cuda()
            output = model(data)

            loss = criterion(output, label)

            
            preds = torch.argmax(output, 1)
            
            val_loss += loss.item()*data.size(0)
            running_accu += torch.sum(preds == label.data)
    val_loss = val_loss/len(val_dataloader.dataset)
    print('Epoch: {} \t Val Loss: {:.6f}'.format(epoch, val_loss))


# In[ ]:




