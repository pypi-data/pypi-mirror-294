#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import torch
import jieba
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from torch.optim import Adam, lr_scheduler
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import precision_recall_fscore_support,accuracy_score
from sklearn import metrics
import json
import pandas as pd
import time
from datetime import timedelta


# In[2]:


MAX_LEN =  100
TRAIN_BATCH_SIZE = 64
VAL_BATCH_SIZE = 256
VOCAB_SIZE = len(json.load(open('./data/word2id.json', 'r', encoding='utf-8')))
learning_rate = 1e-4
NUM_EPOCH = 10

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# # 数据处理

# In[3]:


import json
import jieba
from torch.utils.data import Dataset

class SentimentDataset(Dataset):
    def __init__(self, data_path: str, data_type: str, max_token_len: int = 512):
        """
        初始化情感分析数据集类。
        参数:
            data_path (str): 数据文件路径。
            data_type (str): 数据类型，用于区分训练、验证或测试数据。
            max_token_len (int): 句子的最大词元长度，默认为512。
        """
        self.max_token_len = max_token_len
        # 加载数据文件
        self.data = json.load(open(data_path))
        # 加载词到ID的映射
        self.word2id = json.load(open('./data/word2id.json', 'r', encoding='utf-8'))
        # 定义标签到ID的映射
        self.label2id = {'angry': 0, 'neutral': 1, 'happy': 2, 'sad': 3, 'surprise': 4, 'fear': 5}

    def transform(self, sentence):
        """
        将句子转换为词ID列表。
        参数:
            sentence (str): 待转换的句子。
        返回:
            List[int]: 词ID组成的列表。
        """
        sent_ids = []
        # 使用jieba进行分词
        sentence = jieba.lcut(sentence)
        # 将每个词转换为对应的ID
        for word in sentence:
            if word not in self.word2id:
                sent_ids.append(1)  # 使用1作为未知词的ID
            else:
                sent_ids.append(self.word2id[word])
        return sent_ids
    
    def __getitem__(self, index: int):
        """
        根据索引获取数据项。
        参数:
            index (int): 数据索引。
        返回:
            Tuple[List[int], int]: 包含词ID列表和标签ID的元组。
        """
        line = self.data[index]
        content = line['content']
        label = line['label']

        sentence_id = self.transform(content)
        label_id = self.label2id[label]
    
        return sentence_id, label_id

    def __len__(self):
        """
        获取数据集的大小。
        返回:
            int: 数据集中的样本数量。
        """
        return len(self.data)


# In[4]:


# 为训练和评估创建SentimentDataset实例
train_dataset = SentimentDataset("./data/usual_train.txt", 'train', max_token_len=MAX_LEN)
eval_dataset = SentimentDataset("./data/usual_eval_labeled.txt", 'eval', max_token_len=MAX_LEN)


# In[5]:


# 打印一条数据
for td  in train_dataset:
    print(td)
    break


# In[6]:


import torch
from torch.nn.utils.rnn import pad_sequence

def collate_fn(batch):
    """
    自定义批处理函数，用于将数据批次组合成一个批次的Tensor，适用于DataLoader。
    参数:
        batch (list): 由多个数据样本组成的列表，每个样本包含句子ID和标签ID。
    
    返回:
        Tuple[Tensor, Tensor]: 第一个Tensor是填充后的句子ID，第二个Tensor是标签ID。
    """
    # 从batch中提取句子ID，并将其转换为长整型张量
    sentence_ids = [torch.LongTensor(sentence_id) for sentence_id, label_id in batch]
    # 从batch中提取标签ID，并将每个标签ID封装在Tensor中
    label_ids = [torch.LongTensor([label_id]) for sentence_id, label_id in batch]
    
    # 使用pad_sequence将不同长度的句子ID填充至相同长度，padding_value=0表示用0填充
    sentence_ids = pad_sequence(sentence_ids, batch_first=True, padding_value=0)
    # 将标签ID的列表转换成一个Tensor
    label_ids = torch.cat(label_ids)
    
    return sentence_ids, label_ids


# In[7]:


train_dataloader = DataLoader(train_dataset, batch_size=TRAIN_BATCH_SIZE, shuffle=True, num_workers=0, collate_fn = collate_fn)
eval_dataloader = DataLoader(eval_dataset, batch_size=VAL_BATCH_SIZE, shuffle=False, num_workers=0, collate_fn = collate_fn)


# In[8]:


# 打印一个batch数据
for td in train_dataloader:
    print(td)
    break


# # 模型构建

# In[9]:


class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=300, hidden_dim=128, n_layers=2, bidirectional=False, dropout=0.1, pad_idx=None, num_labels=6):
        """
        LSTM 模型，支持全局最大池化。
        参数:
            vocab_size (int): 词汇表大小。
            embedding_dim (int): 嵌入层的维度，默认为300。
            hidden_dim (int): LSTM单元的隐藏层维度，默认为128。
            n_layers (int): LSTM堆叠的层数，默认为2。
            bidirectional (bool): 是否为双向LSTM，默认为False。
            dropout (float): 在LSTM层之后应用的dropout比例，默认为0.1。
            pad_idx (int): 嵌入层中用于填充的索引，默认为None。
            num_labels (int): 输出类别的数量，默认为6。
        """
        super().__init__()

        # 嵌入层
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_idx)

        # LSTM层
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers=n_layers,
            bidirectional=bidirectional,
            dropout=dropout if n_layers > 1 else 0,  # 当层数大于1时启用dropout
            batch_first=True
        )

        # Dropout层，用于防止过拟合
        self.dropout = nn.Dropout(dropout)

        # 根据LSTM的方向性确定全连接层输入的大小
        num_direction = 2 if bidirectional else 1  # 双向则乘以2
        self.fc = nn.Linear(hidden_dim * num_direction, num_labels)  # 全连接层

    def forward(self, text):
        """
        模型的前向传播定义。
        参数:
            text (torch.Tensor): 输入文本的张量表示，大小为 [batch_size, sentence_length]
        返回:
            loggits (torch.Tensor): 模型的输出 logits
        """
        # 将文本输入嵌入层
        embedded = self.embedding(text)  # [batch_size, sentence_length] -> [batch_size, sentence_length, embedding_dim]

        # 将嵌入的输出送入LSTM层
        hidden_output, (h_n, c_n) = self.lstm(embedded)

        # 应用全局最大池化
        pooled_output, _ = torch.max(hidden_output, dim=1)  # 在时间维度上应用最大池化

        # 通过全连接层得到最终的logits
        logits = self.fc(pooled_output)
        
        return logits


# In[10]:


model = LSTMModel(
    vocab_size= VOCAB_SIZE,
    embedding_dim = 300, 
    hidden_dim = 128,
    n_layers = 1,
    bidirectional=True,
    dropout = 0.1,
    pad_idx = 0,
    num_labels = 6)


# In[11]:


model = model.to(device)


# # 模型训练

# 

# In[12]:


# 优化器设置为Adam，学习率为learning_rate
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# 损失函数设置为交叉熵损失，用于多分类任务
criterion = nn.CrossEntropyLoss()

# 选择运行设备，优先使用GPU，如果不可用则使用CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 初始化最优验证集损失为正无穷大
val_best_loss = float('inf')

# 初始化TensorBoard日志记录器，保存日志到指定目录
writer = SummaryWriter(log_dir='./lstm_v2/')

# 训练的总轮次
NUM_EPOCH = 20

# 开始训练与评估循环
for epoch in range(NUM_EPOCH):
    # 设置模型为训练模式
    model.train()
    
    # 初始化训练总损失和步数
    train_total_loss = 0.
    nb_train_steps = 0
    
    # 存储训练过程中预测的标签和真实标签
    train_labels_list, train_preds_list = [], []
    
    # 遍历一个epoch的数据
    for sentence_ids, label_ids in train_dataloader:
        nb_train_steps += 1
        
        # 将数据加载到设备上（GPU或CPU）
        sentence_ids, label_ids = sentence_ids.to(device), label_ids.to(device)
        
        # 模型前向传播，得到输出
        outputs = model(sentence_ids)
        
        # 计算损失
        train_loss = criterion(outputs, label_ids)
        train_total_loss += train_loss.item()
        
        # 清空优化器中的梯度
        optimizer.zero_grad()
        
        # 反向传播计算梯度
        train_loss.backward()
        
        # 优化器更新模型参数
        optimizer.step()
        
        # 获取模型预测的类别并存储
        train_preds_list.extend(torch.max(outputs.data, 1)[1].cpu().tolist())
        train_labels_list.extend(label_ids.data.cpu().tolist())

    # 计算训练集上的准确率
    train_acc = accuracy_score(train_labels_list, train_preds_list)
    
    # 计算平均训练损失
    train_loss = train_total_loss / nb_train_steps
    print(f'epoch:{epoch}, train_loss:{train_loss}, train_acc:{train_acc}')

    # 设置模型为评估模式
    model.eval()
    
    # 初始化验证集数据
    labels_list, preds_list = [], []
    nb_eval_steps = 0
    eval_total_loss = 0.
    
    # 在评估时不计算梯度以节省内存和计算
    with torch.no_grad():
        for sentence_ids, label_ids in eval_dataloader:
            # 将验证集数据加载到设备上
            sentence_ids, label_ids = sentence_ids.to(device), label_ids.to(device)
            
            # 模型前向传播，得到输出
            outputs = model(sentence_ids)
            
            # 计算验证集损失
            eval_loss = criterion(outputs, label_ids)
            eval_total_loss += eval_loss.item()
            
            # 获取模型预测的类别并存储
            preds_list.extend(torch.max(outputs.data, 1)[1].cpu().tolist())
            labels_list.extend(label_ids.data.cpu().tolist())

            nb_eval_steps += 1

    # 计算验证集上的准确率
    val_acc = accuracy_score(labels_list, preds_list)
    
    # 计算验证集上的宏平均精度、召回率和F1得分
    val_mp, val_mr, val_mf, _ = precision_recall_fscore_support(
        y_true=labels_list, y_pred=preds_list, average='macro')

    # 计算平均验证损失
    val_loss = eval_total_loss / nb_eval_steps

    # 如果当前验证损失优于之前的最佳损失，则保存模型
    if val_loss < val_best_loss:
        val_best_loss = val_loss
        torch.save(model.state_dict(), "./cache/TextRNN_model.bin")

    # 使用TensorBoard记录损失、准确率和其他指标
    writer.add_scalar("loss/train", train_loss, epoch)
    writer.add_scalar("loss/val", val_loss, epoch)
    writer.add_scalar("acc/train", train_acc, epoch)
    writer.add_scalar("acc/val", val_acc, epoch)
    writer.add_scalar("mp/val", val_mp, epoch)
    writer.add_scalar("mr/val", val_mr, epoch)
    writer.add_scalar("mf/val", val_mf, epoch)

    # 打印当前epoch的评估结果
    print(f'epoch:{epoch}, val_loss:{val_loss} val_acc: {val_acc}, val_mp:{val_mp}, val_mr:{val_mr}, val_mf:{val_mf}')


# In[ ]:





# # 模型预测

# In[13]:


test_dataset = SentimentDataset("./data/usual_test_labeled.txt", 'test',  max_token_len= MAX_LEN)
test_dataloader = DataLoader(test_dataset, batch_size=VAL_BATCH_SIZE, shuffle=False, num_workers=0, collate_fn = collate_fn)


# In[14]:


# 加载训练好的模型参数
model.load_state_dict(torch.load("./cache/TextRNN_model.bin"))

# 设置模型为评估模式，禁用dropout等操作
model.eval()

# 初始化测试集总损失
test_total_loss = 0.
# 初始化用于存储真实标签和预测标签的列表
labels_list, preds_list = [], []

# 遍历测试数据集
for sentence_ids, label in test_dataloader:
    # 将输入的句子ID和标签加载到指定设备（GPU或CPU）上
    sentence_ids = sentence_ids.to(device)
    label = label.to(device)

    # 模型前向传播，计算输出
    outputs = model(sentence_ids)

    # 计算损失
    test_loss = criterion(outputs, label)
    test_total_loss += test_loss.item()  # 累计测试集的总损失

    # 获取预测的类别并存储到preds_list中
    preds_list.extend(torch.max(outputs.data, 1)[1].cpu().tolist())
    # 存储真实的标签到labels_list中
    labels_list.extend(label.data.cpu().tolist())

# 计算测试集上的准确率
test_acc = metrics.accuracy_score(labels_list, preds_list)

# 生成测试集的分类报告，包括精确率、召回率和F1分数
test_report = metrics.classification_report(labels_list, preds_list, digits=6)

# 生成测试集的混淆矩阵
test_confusion = metrics.confusion_matrix(labels_list, preds_list)

# 打印测试集的损失和准确率
msg = 'Test Loss: {0:>5.2f},  Test Acc: {1:>6.2%}'
print(msg.format(test_total_loss / len(test_dataloader), test_acc))  # 修正：显示平均损失而不是最后一个批次的损失

# 打印精确率、召回率和F1分数
print("Precision, Recall and F1-Score...")
print(test_report)

# 打印混淆矩阵
print("Confusion Matrix...")
print(test_confusion)


# In[ ]:




