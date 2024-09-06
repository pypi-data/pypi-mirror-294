#!/usr/bin/env python
# coding: utf-8

# # 2.1 Dataset和DataLoader
# 
# Pytorch通常使用Dataset和DataLoader这两个工具类来构建数据管道。
# 
# - Dataset定义了数据集的内容，它相当于一个类似列表的数据结构，具有确定的长度，能够用索引获取数据集中的元素。
# 
# - DataLoader定义了按batch加载数据集的方法，它是一个实现了`__iter__`方法的可迭代对象，每次迭代输出一个batch的数据。
# 
# 

# In[1]:


import torch 
import torchvision

print("torch.__version__="+torch.__version__) 
print("torchvision.__version__="+torchvision.__version__) 


# 

# ### 一，Dataset构建数据集
# 
# Dataset创建数据集常用的方法有：
# 
# * 使用 torch.utils.data.TensorDataset 根据Tensor创建数据集(numpy的array，Pandas的DataFrame需要先转换成Tensor)。
# 
# * 使用 torchvision.datasets.ImageFolder 根据图片目录创建图片数据集。
# 
# * 继承 torch.utils.data.Dataset 创建自定义数据集。
# 
# 
# 此外，还可以通过
# 
# * torch.utils.data.random_split 将一个数据集分割成多份，常用于分割训练集，验证集和测试集。
# 
# * 调用Dataset的加法运算符(`+`)将多个数据集合并成一个数据集。
# 

# #### 1.继承 torch.utils.data.Dataset 创建自定义数据集

# In[2]:


from torch.utils.data import Dataset,DataLoader


# In[3]:


class ToyDataset(Dataset):
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y 
        
    def __len__(self):
        return len(self.X)
        
    def __getitem__(self,index):
        return self.X[index],self.Y[index]
    


# In[4]:


X = torch.randn(1000,3)

Y = torch.randint(low=0,high=2,size=(1000,)).float()

ds = ToyDataset(X,Y)

dl = DataLoader(ds,batch_size=4,drop_last = False)

for  d in dl:
    features,labels = d

    break
# features,labels = next(iter(dl))
print("features = ",features )
print("labels = ",labels )  


# In[ ]:





# In[ ]:





# #### 2.使用 torch.utils.data.TensorDataset 根据Tensor创建数据集

# In[5]:


X = torch.randn(1000,3)

Y = torch.randint(low=0,high=2,size=(1000,)).float()


ds = torch.utils.data.TensorDataset(X,Y)


# In[6]:


dl = DataLoader(ds,batch_size=4,drop_last = False)

for  d in dl:
    features,labels = d

    break
# features,labels = next(iter(dl))
print("features = ",features )
print("labels = ",labels )  


# 

# ### 三，使用DataLoader加载数据集

# DataLoader能够控制batch的大小，batch中元素的采样方法，以及将batch结果整理成模型所需输入形式的方法，并且能够使用多进程读取数据。
# 
# DataLoader的函数签名如下。

# ```python
# DataLoader(
#     dataset, #
#     batch_size=1, #
#     shuffle=False,#
#     sampler=None,
#     batch_sampler=None,
#     num_workers=0, #
#     collate_fn=None,  #
#     pin_memory=False,
#     drop_last=False,
#     timeout=0,
#     worker_init_fn=None,
#     multiprocessing_context=None,
# )
# ```
# 

# 一般情况下，我们仅仅会配置 dataset, batch_size, shuffle, num_workers,pin_memory, drop_last这六个参数，
# 
# 有时候对于一些复杂结构的数据集，还需要自定义collate_fn函数，其他参数一般使用默认值即可。
# 
# DataLoader除了可以加载我们前面讲的 torch.utils.data.Dataset 外，还能够加载另外一种数据集 torch.utils.data.IterableDataset。
# 
# 和Dataset数据集相当于一种列表结构不同，IterableDataset相当于一种迭代器结构。 它更加复杂，一般较少使用。
# 
# - dataset : 数据集
# - batch_size: 批次大小
# - shuffle: 是否乱序
# - sampler: 样本采样函数，一般无需设置。
# - batch_sampler: 批次采样函数，一般无需设置。
# - num_workers: 使用多进程读取数据，设置的进程数。
# - collate_fn: 整理一个批次数据的函数。
# - pin_memory: 是否设置为锁业内存。默认为False，锁业内存不会使用虚拟内存(硬盘)，从锁业内存拷贝到GPU上速度会更快。
# - drop_last: 是否丢弃最后一个样本数量不足batch_size批次数据。
# - timeout: 加载一个数据批次的最长等待时间，一般无需设置。
# - worker_init_fn: 每个worker中dataset的初始化函数，常用于 IterableDataset。一般不使用。
# 
# 

# In[ ]:





# In[7]:


#构建输入数据管道
ds = torch.utils.data.TensorDataset(torch.arange(1,50))
dl = DataLoader(ds,
                batch_size = 10,
                shuffle= True,
                num_workers=2,
                drop_last = True)
#迭代数据
for batch, in dl:
    print(batch)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### 四，深入理解Dataset和DataLoader原理

# 
# **1，获取一个batch数据的步骤**
# 
# 让我们考虑一下从一个数据集中获取一个batch的数据需要哪些步骤。
# 
# (假定数据集的特征和标签分别表示为张量`X`和`Y`，数据集可以表示为`(X,Y)`, 假定batch大小为`m`)
# 
# (1) 首先我们要确定数据集的长度`n`。
# 
# 结果类似：`n = 1000`。
# 
# (2) 然后我们从`0`到`n-1`的范围中抽样出`m`个数(batch大小)。
# 
# 假定`m=4`, 拿到的结果是一个列表，类似：`indices = [1,4,8,9]`
# 
# (3) 接着我们从数据集中去取这`m`个数对应下标的元素。
# 
# 拿到的结果是一个元组列表，类似：`samples = [(X[1],Y[1]),(X[4],Y[4]),(X[8],Y[8]),(X[9],Y[9])]`
# 
# (4) 最后我们将结果整理成两个张量作为输出。
# 
# 拿到的结果是两个张量，类似`batch = (features,labels) `， 
# 
# 其中 `features = torch.stack([X[1],X[4],X[8],X[9]])`
# 
# `labels = torch.stack([Y[1],Y[4],Y[8],Y[9]])`
# 
# 
# 

# **2，Dataset和DataLoader的功能分工**
# 
# 以下是 Dataset和 DataLoader的核心源码，省略了为了提升性能而引入的诸如多进程读取数据相关的代码。
# 

# In[8]:


import torch 
class Dataset(object):
    def __init__(self):
        pass
    
    def __len__(self):
        raise NotImplementedError
        
    def __getitem__(self,index):
        raise NotImplementedError
        

class DataLoader(object):
    def __init__(self,dataset,batch_size,collate_fn = None,shuffle = True,drop_last = False):
        self.dataset = dataset
        self.collate_fn = collate_fn
        self.sampler =torch.utils.data.RandomSampler if shuffle else \
           torch.utils.data.SequentialSampler
        self.batch_sampler = torch.utils.data.BatchSampler
        self.sample_iter = self.batch_sampler(
            self.sampler(self.dataset),
            batch_size = batch_size,drop_last = drop_last)
        self.collate_fn = collate_fn if collate_fn is not None else \
            torch.utils.data._utils.collate.default_collate
        
    def __next__(self):
        indices = next(iter(self.sample_iter))
        batch = self.collate_fn([self.dataset[i] for i in indices])
        return batch
    
    def __iter__(self):
        return self
    


# In[1]:


import pandas as pd 


# In[3]:


df = pd.DataFrame()
df 


# - 上述第1个步骤确定数据集的长度是由 Dataset的`__len__` 方法实现的。
# 
# - 第2个步骤从`0`到`n-1`的范围中抽样出`m`个数的方法是由 DataLoader的 `sampler`和 `batch_sampler`参数指定的。
# 
# `sampler`参数指定单个元素抽样方法，一般无需用户设置，程序默认在DataLoader的参数`shuffle=True`时采用随机抽样，`shuffle=False`时采用顺序抽样。
# 
# `batch_sampler`参数将多个抽样的元素整理成一个列表，一般无需用户设置，默认方法在DataLoader的参数`drop_last=True`时会丢弃数据集最后一个长度不能被batch大小整除的批次，在`drop_last=False`时保留最后一个批次。
# 
# - 第3个步骤的核心逻辑根据下标取数据集中的元素 是由 Dataset的 `__getitem__`方法实现的。
# 
# - 第4个步骤的逻辑由DataLoader的参数`collate_fn`指定。一般情况下也无需用户设置。
# 

# In[ ]:




