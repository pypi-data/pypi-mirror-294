#!/usr/bin/env python
# coding: utf-8

# In[17]:


# 标准库导入
import os
import shutil
import time
import random
# 第三方库导入
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models
from sklearn.metrics import accuracy_score
from torch.utils.tensorboard import SummaryWriter
import torchvision.transforms as transforms 
from PIL import Image, ImageFile

# 配置，确保即使图片文件损坏也能加载图片
ImageFile.LOAD_TRUNCATED_IMAGES = True

# 设置使用的 CUDA 设备
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 进一步的初始化设置或模块级别的配置可以在这里进行
# 例如，设置随机种子以保证结果可复现
torch.manual_seed(42)
random.seed(42)


# In[18]:


class Garbage_Loader(Dataset):
    def __init__(self, txt_path, train_flag=True):
        """
        初始化数据加载器
        :param txt_path: 图片信息的文本文件路径
        :param train_flag: 指示是否为训练数据
        """
        # 从指定的文本文件中读取图像信息
        self.imgs_info = self.get_images(txt_path)
        self.train_flag = train_flag

        # 训练时使用的图像变换策略，包括调整大小、随机水平和垂直翻转以及转换为张量格式
        self.train_tf = transforms.Compose([
            transforms.Resize(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.ToTensor(),
        ])
        
        # 验证时使用的图像变换策略，只包括调整大小和转换为张量格式
        self.val_tf = transforms.Compose([
            transforms.Resize(224),
            transforms.ToTensor(),
        ])

    def get_images(self, txt_path):
        """
        从文本文件读取图片路径和标签
        :param txt_path: 文本文件路径
        :return: 图片信息列表，每项为[图片路径, 标签]
        """
        with open(txt_path, 'r', encoding='utf-8') as f:
            imgs_info = [line.strip().split('\t') for line in f.readlines()]
        return imgs_info

    def padding_black(self, img):
        """
        将图片填充为正方形，背景为黑色
        :param img: PIL图像对象
        :return: 填充后的图像
        """
        w, h = img.size
        scale = 224. / max(w, h)  # 计算缩放比例以确保图片填充后边长为224
        img_fg = img.resize([int(w * scale), int(h * scale)])  # 缩放图片

        size_bg = 224
        img_bg = Image.new("RGB", (size_bg, size_bg))  # 创建一个新的黑色背景图像
        img_bg.paste(img_fg, ((size_bg - img_fg.width) // 2,  # 将缩放后的图片居中粘贴到背景图像上
                              (size_bg - img_fg.height) // 2))
        return img_bg

    def __getitem__(self, index):
        """
        获取单个数据项
        :param index: 数据索引
        :return: 处理后的图像和标签
        """
        img_path, label = self.imgs_info[index]  # 获取图像路径和标签
        img = Image.open('/root/autodl-tmp/' + img_path).convert('RGB')  # 打开图像并转换为RGB
        img = self.padding_black(img)  # 将图像填充为正方形
        if self.train_flag:
            img = self.train_tf(img)  # 应用训练时的图像变换
        else:
            img = self.val_tf(img)  # 应用验证时的图像变换
        label = int(label)  # 将标签转换为整数
        return img, label

    def __len__(self):
        """
        数据集长度
        :return: 数据集中的数据项数
        """
        return len(self.imgs_info)


# ### 测试dataset和dataloader构造是否正确

# In[19]:


# 创建训练数据集的实例
train_dataset = Garbage_Loader("/root/autodl-tmp/dataset/train.txt", True)
# 打印训练数据集中的数据项总数
print("数据个数：", len(train_dataset))

# 使用DataLoader来批量加载数据，设定批量大小为1，并启用数据打乱
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                            batch_size=1, 
                                            shuffle=True)

# 从数据加载器中迭代获取数据，这里仅迭代一次以打印第一个批次的图像和标签
for image, label in train_loader:
    # 打印当前批次图像的维度
    print(image.shape)
    # 打印当前批次的标签
    print(label)
    # 终止循环，确保只打印第一批次的信息
    break


# In[ ]:





# In[20]:


# ------------------------------ step 1/4 : 加载数据 ---------------------------
# 定义训练和验证数据文件的路径
train_dir_list = '/root/autodl-tmp/dataset/train.txt'
valid_dir_list = '/root/autodl-tmp/dataset/val.txt'

# 设置批处理大小
batch_size = 64

# 创建数据加载器实例
train_data = Garbage_Loader(train_dir_list, train_flag=True)
valid_data = Garbage_Loader(valid_dir_list, train_flag=False)

# 配置 DataLoader
train_loader = DataLoader(dataset=train_data, num_workers=8, pin_memory=True, batch_size=batch_size, shuffle=True)
valid_loader = DataLoader(dataset=valid_data, num_workers=8, pin_memory=True, batch_size=batch_size)

# 获取并打印数据集大小
train_data_size = len(train_data)
print('训练集数量：%d' % train_data_size)
valid_data_size = len(valid_data)
print('验证集数量：%d' % valid_data_size)


# In[ ]:





# In[ ]:





# 

# ### 模型构建

# In[21]:


# https://pytorch.org/vision/stable/models.html#classification

class GarbageResNet50(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        """
        GarbageResNet50 类：为垃圾分类定制的 ResNet-50 模型，支持加载预训练权重并替换全连接层以适应新的类别数。
        
        参数:
            num_classes (int): 目标类别的数量。
            pretrained (bool): 是否使用预训练的模型作为初始化。
        """
        super(GarbageResNet50, self).__init__()  # 调用父类的初始化方法
        self.model = models.resnet50(pretrained=pretrained)  # 加载预训练的 ResNet-50 模型

        # 替换全连接层以匹配目标类别数
        fc_inputs = self.model.fc.in_features
        self.model.fc = nn.Linear(fc_inputs, num_classes)

    def forward(self, x):
        """
        定义模型的前向传播。
        
        参数:
            x (torch.Tensor): 输入的图像张量。
            
        返回:
            torch.Tensor: 模型输出的张量。
        """
        return self.model(x)



# In[5]:


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar'):
    """
        根据 is_best 存模型，一般保存 valid acc 最好的模型
    """
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best_' + filename)


# In[ ]:





# In[ ]:





# In[22]:


def train(train_loader, model, criterion, optimizer, epoch, writer):
    """
    训练神经网络模型。
    参数:
        train_loader - DataLoader，提供训练数据。
        model - 待训练的模型。
        criterion - 用于计算损失的损失函数。
        optimizer - 用于优化模型参数的优化器。
        epoch - 当前的训练周期编号。
        writer - 用于写入TensorBoard的记录器。
    """
    # 切换模型到训练模式
    model.train()

    # 初始化变量
    end = time.time()
    train_preds_list = []
    train_labels_list = []
    train_total_loss = 0.0
    nb_train_steps = 0

    # 遍历数据加载器中的每一个批次
    for i, (input, label) in enumerate(train_loader):
        nb_train_steps += 1
        # 将输入和标签转移到CUDA设备上
        input = input.to("cuda")
        label = label.to("cuda")

        # 计算模型输出和损失
        output = model(input)
        loss = criterion(output, label)

        # 清除旧的梯度，执行反向传播，进行一步参数优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 累计损失和预测结果
        train_total_loss += loss.item()
        train_preds_list.extend(torch.max(output, 1)[1].cpu().tolist())
        train_labels_list.extend(label.cpu().tolist())

    # 计算平均损失和准确率
    train_acc = accuracy_score(train_labels_list, train_preds_list)
    train_loss = train_total_loss / nb_train_steps
    print(f'epoch: {epoch}, train_loss: {train_loss}, train_acc: {train_acc}')

    # 将损失写入TensorBoard
    writer.add_scalar('loss/train_loss', train_loss, global_step=epoch)


# In[23]:


def validate(val_loader, model, criterion, epoch, writer, phase="VAL"):
    """
    在给定的验证集上评估模型的性能。
    参数：
        val_loader - DataLoader，提供验证数据。
        model - 待评估的模型。
        criterion - 用于计算损失的损失函数。
        epoch - 当前的验证周期编号。
        writer - 用于写入TensorBoard的记录器。
        phase - 表示当前是验证阶段还是其他自定义阶段，默认为"VAL"。
    """
    # 切换模型到评估模式
    model.eval()

    # 初始化变量
    val_labels_list, val_preds_list = [], []
    val_total_loss = 0.0
    nb_eval_steps = 0 

    # 禁用梯度计算，以提高计算效率并减少内存消耗
    with torch.no_grad():
        end = time.time()
        for i, (input, label) in enumerate(val_loader):
            nb_eval_steps += 1
            # 将输入和标签转移到CUDA设备上
            input = input.to("cuda")
            label = label.to("cuda")
            
            # 计算模型输出和损失
            output = model(input)
            val_loss = criterion(output, label)

            # 累计损失和预测结果
            val_total_loss += val_loss.item()
            val_preds_list.extend(torch.max(output, 1)[1].cpu().tolist())
            val_labels_list.extend(label.data.cpu().tolist())

    # 计算平均损失和准确率
    val_acc = accuracy_score(val_labels_list, val_preds_list)
    val_loss = val_total_loss / nb_eval_steps
    
    # 打印并记录结果
    print(f'epoch:{epoch}, val_loss:{val_loss} val_acc: {val_acc}')
    writer.add_scalar('loss/valid_loss', val_loss, global_step=epoch)
    
    return val_acc


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 
# 
# 优化器配置：
# 
# 使用Adam优化器，这是一种常用的梯度下降优化算法，适用于大多数深度学习任务。
# model.parameters()：这个函数调用返回了模型的所有可训练参数。
# lr=lr_init：这里将初始学习率设置为lr_init。
# weight_decay=weight_decay：权重衰减通常用于正则化，有助于防止模型过拟合。
# 学习率调度器：
# 
# 使用torch.optim.lr_scheduler.StepLR调度器，它会在每过step_size个epoch后将学习率乘以gamma（在这里是0.1）。这意味着学习率将按指数级衰减，有助于模型在训练后期细化学习并收敛到更好的性能。
# 
# 

# In[ ]:


# ------------------------------ step 2/4 : 定义网络 ---------------------------
# 将模型迁移到 GPU
# 使用类创建模型
num_classes = 214
model = GarbageResNet50(num_classes, pretrained=True)
model = model.cuda()
# ------------------------------ step 3/4 : 定义损失函数和优化器等 -------------
# 设置学习率和其他超参数
lr_init = 0.0001
lr_stepsize = 20
weight_decay = 0.001

# 初始化损失函数和优化器
criterion = nn.CrossEntropyLoss()


optimizer = optim.Adam(model.parameters(), lr=lr_init, weight_decay=weight_decay)

# 配置学习率调度器
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=lr_stepsize, gamma=0.1)

# 创建 TensorBoard 日志写入器
writer = SummaryWriter('runs/resnet50')

# ------------------------------ step 4/4 : 训练 -------------------------------
best_acc = 0
epochs = 80

# 进行多个训练周期
for epoch in range(epochs):
    # 更新学习率
    scheduler.step()

    # 在训练集上训练模型
    train(train_loader, model, criterion, optimizer, epoch, writer)

    # 在验证集上评估模型
    val_acc = validate(valid_loader, model, criterion, epoch, writer, phase="VAL")
    is_best = val_acc > best_acc
    best_acc = max(val_acc, best_acc)

    # 保存模型状态
    save_checkpoint({
        'epoch': epoch + 1,
        'arch': 'resnet50',
        'state_dict': model.state_dict(),
        'best_acc': best_acc,
        'optimizer': optimizer.state_dict(),
    }, is_best, filename='checkpoint_resnet50.pth.tar')

# 关闭 TensorBoard 日志写入器
writer.close()


# 

# In[ ]:





# In[ ]:


import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms 
from torchvision import models
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置使用的GPU设备
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 定义softmax函数，用于计算预测结果的概率分布
def softmax(x):
    """对输入的x执行softmax计算，返回概率分布。"""
    exp_x = np.exp(x)
    softmax_x = exp_x / np.sum(exp_x, 0)
    return softmax_x

# 从文件加载标签
with open('/root/autodl-tmp/dataset/dir_label.txt', 'r', encoding='utf-8') as f:
    labels = [line.strip().split('\t') for line in f.readlines()]

# 设置测试数据集和数据加载器
test_list = '/root/autodl-tmp/dataset/test.txt'
test_data = Garbage_Loader(test_list, train_flag=False)
test_loader = DataLoader(dataset=test_data, num_workers=1, pin_memory=True, batch_size=1)

# 初始化自定义模型，假设GarbageResNet50类已在其他地方定义
num_classes = 214
model = GarbageResNet50(num_classes, pretrained=False).cuda()

# 加载训练好的模型权重
checkpoint = torch.load('model_best_checkpoint_resnet50.pth.tar')
model.load_state_dict(checkpoint['state_dict'])
model.eval()

# 遍历测试数据
for i, (image, label) in enumerate(test_loader):
    # 将图像数据转换为NumPy数组，用于显示
    src = image.squeeze().numpy().transpose((1, 2, 0))  # 调整为适合matplotlib显示的格式

    # 将图像数据发送到GPU
    image = image.cuda()

    # 计算预测结果
    pred = model(image)
    score = softmax(pred.detach().cpu().numpy()[0])
    pred_id = np.argmax(score)

    # 显示图像和预测结果
    plt.imshow(src)
    print('预测结果：', labels[pred_id][0])
    plt.show()
    break  # 只处理第一张图像，去掉这一行可处理整个数据集


# In[ ]:





# In[ ]:




