#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import torch
from torch.utils.data import DataLoader,Dataset,random_split
import torch.optim as optim
from torchvision import transforms
import gzip
import os
import torchvision
import matplotlib.pyplot as plt
import torch.nn as nn


# # 读取数据
# 
# datasets.MNIST是Pytorch的内置函数torchvision.datasets.MNIST，通过这个可以导入数据集。
# 
# train=True 代表我们读入的数据作为训练集（如果为true则从training.pt创建数据集，否则从test.pt创建数据集）
# 
# transform则是读入我们自己定义的数据预处理操作
# 
# download=True则是当我们的根目录（root）下没有数据集时，便自动下载。
# 
# 

# In[5]:


# 定义数据预处理转换：转换为张量并进行标准化
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])  # 使用0.5的均值和标准差进行归一化
])

# 加载MNIST训练数据集
trainsets = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)

# 将训练数据集分割为训练集和验证集
traindataset, valdataset = random_split(trainsets, [50000, 10000])  # 50000用于训练，10000用于验证

# 创建训练数据加载器
train_loader = torch.utils.data.DataLoader(traindataset, batch_size=100, shuffle=True)

# 创建验证数据加载器
val_loader = torch.utils.data.DataLoader(valdataset, batch_size=100, shuffle=True)

# 加载MNIST测试数据集
testsets = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# 创建测试数据加载器
test_loader = torch.utils.data.DataLoader(testsets, batch_size=100, shuffle=False)


# In[6]:


trainsets[0][0].shape


# In[4]:


for img,label in train_loader:
    img = img.view(img.size(0),-1)

    break


# In[5]:


img.shape


# # 简单的三层全连接神经网络
# 其中，需要传递的参数为：输入的维度（in_dim），第一层网络的神经元个数（n_hidden_1），第二层网络神经元的个数（n_hidden_2），第三层网络（输出层）神经元个数。
# 
# 

# In[6]:


class simpleNet(nn.Module):
    def __init__(self,in_dim,n_hidden_1,n_hidden_2,out_dim):
        super(simpleNet,self).__init__()
        self.layer1 = nn.Linear(in_dim,n_hidden_1)
        self.layer2 = nn.Linear(n_hidden_1,n_hidden_2)
        self.layer3 = nn.Linear(n_hidden_2,out_dim)
    
    def forward(self,x):  #batch, in_dim
        x = self.layer1(x)  # batch n_hidden_1
        x = self.layer2(x)  #bat  ch  n_hidden_2
        x = self.layer3(x)  # batch  out_dim
        return x


# # 模型训练
# 
# 1）关于模型的输入参数
# 
# 因为图片的大小为28*28，所以输入的维度是 28 *28，然后300和100分别是隐藏层的维度（这边可以自行测试修改），最后输出层的维度为10，因为这是个训练识别数字的分类问题（0~9一共十个数字）。
# 
# 2）img.view(img.size(0),-1)的作用
# 
# 首先，view()函数是用来改变tensor的形状的，例如将2行3列的tensor变成1行6列，其中-1表示会自适应的调整剩余的维度
# 

# In[ ]:





# In[2]:


#定义学习率，训练次数，损失函数，优化器
device = 'cuda' if torch.cuda.is_available() else 'cpu'

learning_rate = 1e-2
epoches = 20

criterion = nn.CrossEntropyLoss()

model = simpleNet(28*28,300,100,10)

optimizer = optim.SGD(model.parameters(),lr=learning_rate)



model.to(device)

# 模型训练过程
for epoch in range(epoches):
    train_loss = 0
    train_acc = 0

    for img, label in train_loader:
        img = img.view(img.size(0), -1).to(device)  # 调整图片形状并移至设备
        label = label.to(device)  # 标签移至设备
        output = model(img)  # 前向传播
        loss = criterion(output, label)  # 计算损失
        optimizer.zero_grad()  # 梯度清零
        loss.backward()  # 反向传播
        optimizer.step()  # 优化器更新参数

        train_loss += loss.item()
        pred = torch.argmax(output, 1)  # 预测
        num_correct = (pred == label).sum().item()  # 正确预测数量
        train_acc += num_correct

    train_loss /= len(train_loader.dataset)
    train_acc /= len(train_loader.dataset)
    print(f'Epoch: {epoch+1}, Train Loss: {train_loss:.6f}, Train Acc: {train_acc:.6f}')

    # 验证集评估
    model.eval()  # 切换为评估模式
    eval_loss = 0
    eval_acc = 0
    with torch.no_grad():  # 不计算梯度
        for img, label in val_loader:
            img = img.view(img.size(0), -1).to(device)
            label = label.to(device)
            output = model(img)
            loss = criterion(output, label)
            eval_loss += loss.item() * img.size(0)
            pred = torch.argmax(output, 1)
            num_correct = (pred == label).sum().item()
            eval_acc += num_correct

        eval_loss /= len(val_loader.dataset)
        eval_acc /= len(val_loader.dataset)
        print(f'Eval Loss: {eval_loss:.6f}, Acc: {eval_acc:.6f}')
    

#batch  loss / batch num


# sample loss /  sample num 


# # 模型测试

# In[8]:


#测试网络模型
model.eval()
eval_loss = 0
eval_acc = 0
for img,label in test_loader:
    img = img.view(img.size(0),-1).to(device)
    label = label.to(device)
    output = model(img)

    
    loss = criterion(output,label)
    eval_loss += loss.item()*img.size(0)
    _ , pred = torch.max(output,1)
    num_correct = (pred==label).sum().item()
    eval_acc += num_correct 
print("Test Loss:{:.6f},Acc:{:.6f}".format(eval_loss/len(testsets),eval_acc/len(testsets)))


# # 模型层添加激活函数

# In[9]:


'''
最后一层输出层不能添加激活函数，因为输出的结果表示实际的得分
'''
class Activation_Net(nn.Module):
    def __init__(self,in_dim,n_hidden_1,n_hidden_2,out_dim):
        super(Activation_Net,self).__init__()
        self.layer1 = nn.Sequential(nn.Linear(in_dim,n_hidden_1),nn.ReLU(True))
        self.layer2 = nn.Sequential(nn.Linear(n_hidden_1,n_hidden_2),nn.ReLU(True))
        self.layer3 = nn.Sequential(nn.Linear(n_hidden_2,out_dim)) #线性类别输出

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x


# # 模型训练

# In[10]:


#定义学习率，训练次数，损失函数，优化器
device = 'cuda' if torch.cuda.is_available() else 'cpu'
learning_rate = 1e-2
epoches = 20
criterion = nn.CrossEntropyLoss()
model = Activation_Net(28*28,300,100,10)
optimizer = optim.SGD(model.parameters(),lr=learning_rate)
model.to(device)

#模型进行训练
for epoch in range(epoches):
    train_loss = 0
    train_acc = 0
    for img,label in train_loader:
        img = img.view(img.size(0),-1).to(device)
        label = label.to(device)
        output = model(img)
        loss = criterion(output,label)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _,pred = output.max(1)
        num_correct = (pred==label).sum().item()
        train_acc += num_correct
  

    print('epoch: {}, Train Loss: {:.6f}, Train Acc: {:.6f}'.format(epoch+1, train_loss/len(train_loader), train_acc/len(train_loader)))




# # 模型测试

# In[11]:


model.eval()
eval_loss = 0
eval_acc = 0

for img,label in test_loader:
    img = img.view(img.size(0),-1).to(device)
    label = label.to(device)
    output = model(img)
    loss = criterion(output,label)
    eval_loss += loss.item()
    _ , pred = torch.max(output,1)
    num_correct = (pred==label).sum().item()
    eval_acc += num_correct 
print("Test Loss:{:.6f},Acc:{:.6f}".format(eval_loss/len(testsets),eval_acc/len(testsets)))


# In[ ]:





# In[ ]:




