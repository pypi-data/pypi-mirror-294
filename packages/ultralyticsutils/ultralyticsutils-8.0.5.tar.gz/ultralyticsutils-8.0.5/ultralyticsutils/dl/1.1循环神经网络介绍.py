#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import torch.nn as nn


# # RNN介绍

# In[ ]:





# 循环神经网络（Recurrent Neural Network，RNN）是一种用于处理序列数据的神经网络。相比一般的神经网络来说，他能够处理序列变化的数据。比如某个单词的意思会因为上文提到的内容不同而有不同的含义，RNN就能够很好地解决这类问题。

# ![image.png](attachment:image.png)

# - **隐藏状态更新方程**:
#   $$ h_t = \tanh(x_t W_{ih}^T + b_{ih} + h_{t-1} W_{hh}^T + b_{hh}) $$
# 
# 其中：
# - $ h_t $ 是时间步 $t$ 的隐藏状态。
# - $x_t$ 是时间步 $t$ 的输入。
# - $W_{ih}$ 是输入到隐藏层的权重矩阵。
# - $b_{ih}$ 是输入到隐藏层的偏置。
# - $W_{hh}$ 是隐藏层到隐藏层的权重矩阵。
# - $b_{hh}$ 是隐藏层到隐藏层的偏置。
# 

# torch.nn.RNN(
#   input_size, 
#   hidden_size, 
#   num_layers=1, 
#   nonlinearity='tanh', 
#   bias=True, 
#   batch_first=False, 
#   dropout=0.0, 
#   bidirectional=False, 
#   device=None, 
#   dtype=None
# )
# 
# - **input_size**: 输入x的维度
# - **hidden_size**: 隐藏状态h的维度
# - **num_layers**: 递归层的数量。例如，设置num_layers=2意味着堆叠两个RNN，形成一个堆叠的RNN，其中第二个RNN接收第一个RNN的输出并计算最终结果。
# - **nonlinearity**: 使用的非线性函数。可以是'tanh'或'relu'。
# - **bias**: 如果为False，则该层不使用偏置权重b_ih和b_hh。
# - **batch_first**: 如果为True，则输入和输出张量的格式为(batch, seq, feature)，而不是(seq, batch, feature)。
# - **dropout**: 如果非零，除最后一层外，在每个RNN层的输出上引入一个Dropout层，Dropout概率等于dropout。
# - **bidirectional**: 如果为True，则成为一个双向RNN。
# 

# 
# - **输入 (input)**: `input`, `h_0`
# 
#   - **输入 (input)**: 张量形状如下：
#     - 当未分批处理时：`(L, H_in)`，其中 `L` 是序列长度，`H_in` 是输入维度。
#     - 当 `batch_first=False` 时：`(L, N, H_in)`，其中 `N` 是批次大小。
#     - 当 `batch_first=True` 时：`(N, L, H_in)`。
#     这个输入包含输入序列的特征。输入也可以是一个打包的可变长度序列。详情请参见 `torch.nn.utils.rnn.pack_padded_sequence()` 或 `torch.nn.utils.rnn.pack_sequence()`。
# 
#   - **初始隐藏状态 (h_0)**: 张量形状如下：
#     - 当未分批处理时：`(D * num_layers, H_out)`，其中 `D` 是方向数（双向为2，单向为1），`num_layers` 是层数，`H_out` 是输出维度。
#     - 当输入是批次时：`(D * num_layers, N, H_out)`。
#     如果未提供，默认为零。
# 
# 其中：
# - `N` = 批次大小
# - `L` = 序列长度
# - `D` = 如果 `bidirectional=True` 则为2，否则为1
# - `H_in` = 输入大小
# - `H_out` = 隐藏状态的维度
# 

# - **输出 (Outputs)**: `output`, `h_n`
#   - **output**: 张量形状如下：
#     - 当未分批处理时：`(L, D*H_out)`，其中 `L` 是序列长度，`D` 是方向数（双向为2，单向为1），`H_out` 是输出维度。
#     - 当 `batch_first=False` 时：`(L, N, D*H_out)`，其中 `N` 是批次大小。
#     - 当 `batch_first=True` 时：`(N, L, D*H_out)`。
#     这个输出包含了RNN最后一层的输出特征 (h_t) 对每个t。如果输入是一个 `torch.nn.utils.rnn.PackedSequence`，输出也将是一个打包序列。
# 
#   - **h_n**: 张量形状如下：
#     - 当未分批处理时：`(D*num_layers, H_out)`，其中 `D` 是方向数（双向为2，单向为1），`num_layers` 是层数，`H_out` 是输出维度。
#     - 当输入是批次时：`(D*num_layers, N, H_out)`。
#     这个张量包含批次中每个元素的最终隐藏状态。
# 

# In[2]:


rnn = nn.RNN(input_size = 10, hidden_size = 20, num_layers = 1,bidirectional=False, batch_first=True)

#输入的batch:2   序列长度：5. 输入维度：10
input = torch.randn(2, 5, 10)

output, hn = rnn(input)


# In[3]:


output.shape


# In[4]:


hn.shape


# In[5]:


rnn = nn.RNN(input_size = 10, hidden_size = 20, num_layers = 1, batch_first=True)

#输入的batch:3   序列长度：5. 输入维度：10
input = torch.randn(3, 5, 10)

output, hn = rnn(input)


# In[6]:


output.shape


# In[7]:


hn.shape


# 

# # LSTM 介绍

# 

# ![image.png](attachment:image.png)
# 
# 
# ![image.png](attachment:b8e7ddbf-d1ed-4e58-bf38-5609b180e986.png)
# 
# https://colah.github.io/posts/2015-08-Understanding-LSTMs/

# - **门控和状态更新公式**:
#   - **输入门 (i_t)**:
#     $$ i_t = \sigma(W_{ii} x_t + b_{ii} + W_{hi} h_{t-1} + b_{hi}) $$
#   - **遗忘门 (f_t)**:
#     $$ f_t = \sigma(W_{if} x_t + b_{if} + W_{hf} h_{t-1} + b_{hf}) $$
#   - **单元更新 (g_t)**:
#     $$ g_t = \tanh(W_{ig} x_t + b_{ig} + W_{hg} h_{t-1} + b_{hg}) $$
#   - **输出门 (o_t)**:
#     $$ o_t = \sigma(W_{io} x_t + b_{io} + W_{ho} h_{t-1} + b_{ho}) $$
#   - **单元状态更新 (c_t)**:
#     $$ c_t = f_t \odot c_{t-1} + i_t \odot g_t $$
#   - **隐藏状态更新 (h_t)**:
#     $$ h_t = o_t \odot \tanh(c_t) $$
# 
# 其中：
# - $ h_t $ 是时间步 $ t $ 的隐藏状态。
# - $ c_t $ 是时间步 $ t $ 的单元状态。
# - $ x_t $ 是时间步 $ t $ 的输入。
# - $ h_{t-1} $ 是时间步 $ t-1 $ 的隐藏状态或时间为0时的初始隐藏状态。
# - $i_t$, $f_t$, $g_t$, $o_t$ 分别是输入门、遗忘门、单元更新和输出门。
# - $ \sigma $ 是sigmoid函数。
# - $ \odot $ 是哈达玛积（元素间乘积）。
# 

# torch.nn.LSTM(input_size, 
#               hidden_size, 
#               num_layers=1, 
#               bias=True, 
#               batch_first=False, 
#               dropout=0.0, 
#               bidirectional=False, 
#               proj_size=0, 
#               device=None, 
#               dtype=None)
# 
# 
# ### 参数 (Parameters)
# 
# - **input_size** - 输入x中预期的特征数量。
# - **hidden_size** - 隐藏状态h中的特征数量。
# - **num_layers** - 递归层的数量。例如，设置 `num_layers=2` 表示将两个LSTMs堆叠在一起形成一个堆叠的LSTM，其中第二个LSTM接收第一个LSTM的输出并计算最终结果。默认值：1。
# - **bias** - 如果为False，则该层不使用偏置权重 `b_ih` 和 `b_hh`。默认值：True。
# - **batch_first** - 如果为True，则输入和输出张量的提供方式为 `(batch, seq, feature)` 而不是 `(seq, batch, feature)`。注意，这不适用于隐藏状态或单元状态。有关详细信息，请参见下面的输入/输出部分。默认值：False。
# - **dropout** - 如果非零，除了最后一层外，在每个LSTM层的输出上引入一个Dropout层，Dropout概率等于dropout。默认值：0。
# - **bidirectional** - 如果为True，则成为一个双向LSTM。默认值：False。
# - **proj_size** - 如果大于0，则使用具有相应大小投影的LSTM。默认值：0。
# 

# ### 输入 (Inputs): `input`, `(h_0, c_0)`
# 
# - **input**: 张量的形状为：
#   - 未分批输入时：`(L, H_in)`，其中 `L` 是序列长度，`H_in` 是输入尺寸。
#   - 当 `batch_first=False` 时：`(L, N, H_in)`，其中 `N` 是批量大小。
#   - 当 `batch_first=True` 时：`(N, L, H_in)`。
#   此输入包含输入序列的特征。输入也可以是打包的变长序列。详情请参见 `torch.nn.utils.rnn.pack_padded_sequence()` 或 `torch.nn.utils.rnn.pack_sequence()`。
# 
# - **h_0**: 张量的形状为：
#   - 未分批输入时：`(D*num_layers, H_out)`，其中 `D` 是方向数（如果双向则为2，否则为1），`num_layers` 是层的数量，`H_out` 是输出尺寸。
#   - 输入是批量时：`(D*num_layers, N, H_out)`。
#   这个张量包含输入序列中每个元素的初始隐藏状态。如果没有提供 `(h_0, c_0)`，默认为零。
# 
# - **c_0**: 张量的形状为：
#   - 未分批输入时：`(D*num_layers, H_cell)`，其中 `H_cell` 是单元状态尺寸。
#   - 输入是批量时：`(D*num_layers, N, H_cell)`。
#   这个张量包含输入序列中每个元素的初始单元状态。如果没有提供 `(h_0, c_0)`，默认为零。
# 
# 其中：
# - `N` = 批量大小
# - `L` = 序列长度
# - `D` = 如果 `bidirectional=True` 则为2，否则为1
# - `H_in` = 输入尺寸
# - `H_out` = 输出尺寸
# - `H_cell` = 单元状态尺寸，如果 `proj_size > 0` 则使用投影尺寸，否则使用隐藏尺寸
# 

# ### 输出 (Outputs): `output`, `(h_n, c_n)`
# 
# - **output**: 张量的形状为：
#   - 未分批输入时：`(L, D*H_out)`，其中 `L` 是序列长度，`D` 是方向数（如果双向则为2，否则为1），`H_out` 是输出尺寸。
#   - 当 `batch_first=False` 时：`(L, N, D*H_out)`，其中 `N` 是批量大小。
#   - 当 `batch_first=True` 时：`(N, L, D*H_out)`。
#   此输出包含LSTM最后一层的输出特征 (h_t) 对每个t。如果输入是 `torch.nn.utils.rnn.PackedSequence`，输出也将是一个打包序列。当 `bidirectional=True` 时，输出将包含序列中每个时间步的正向和反向隐藏状态的拼接。
# 
# - **h_n**: 张量的形状为：
#   - 未分批输入时：`(D*num_layers, H_out)`，其中 `D` 是方向数（如果双向则为2，否则为1），`num_layers` 是层数，`H_out` 是输出尺寸。
#   - 输入是批量时：`(D*num_layers, N, H_out)`。
#   这个张量包含序列中每个元素的最终隐藏状态。当 `bidirectional=True` 时，`h_n` 将包含最终正向和反向隐藏状态的拼接。
# 
# - **c_n**: 张量的形状为：
#   - 未分批输入时：`(D*num_layers, H_cell)`，其中 `H_cell` 是单元状态尺寸。
#   - 输入是批量时：`(D*num_layers, N, H_cell)`。
#   这个张量包含序列中每个元素的最终单元状态。当 `bidirectional=True` 时，`c_n` 将包含最终正向和反向单元状态的拼接。
# 
# 

# In[8]:


lstm = nn.LSTM(input_size = 10, hidden_size = 20, num_layers = 1,bidirectional=False, batch_first=True)
input = torch.randn(2, 5, 10)

output, (hn, cn) = lstm(input)


# In[9]:


output.shape


# In[10]:


hn.shape


# In[11]:


cn.shape


# In[12]:


lstm = nn.LSTM(input_size = 10, hidden_size = 3, num_layers = 1, batch_first=True)
input = torch.randn(3, 5, 10)
output, (hn, cn) = lstm(input)


# In[13]:


output.shape


# In[14]:


hn.shape


# In[15]:


cn.shape


# In[16]:


output


# In[17]:


pooled_ouput, _ = torch.max(output, dim=1)  


# In[18]:


pooled_ouput


# In[ ]:





# In[ ]:





# In[ ]:





# # GRU介绍

# 

# ![image.png](attachment:image.png)
# 
# https://zh.d2l.ai/chapter_recurrent-modern/gru.html

# 
# 
# ### GRU 更新公式
# 
# - **重置门 (r_t)**:
#   $$ r_t = \sigma(W_{ir} x_t + b_{ir} + W_{hr} h_{t-1} + b_{hr}) $$
# - **更新门 (z_t)**:
#   $$ z_t = \sigma(W_{iz} x_t + b_{iz} + W_{hz} h_{t-1} + b_{hz}) $$
# - **新状态 (n_t)**:
#   $$ n_t = \tanh(W_{in} x_t + b_{in} + r_t \odot (W_{hn} h_{t-1} + b_{hn})) $$
# - **隐藏状态 (h_t)**:
#   $$ h_t = (1 - z_t) \odot n_t + z_t \odot h_{t-1} $$
# 
# 其中：
# - $ h_t $ 是时间步 $ t $ 的隐藏状态。
# - $ x_t $ 是时间步 $ t $ 的输入。
# - $ h_{t-1} $ 是时间步 $ t-1 $ 的隐藏状态或时间为0时的初始隐藏状态。
# - $r_t$, $z_t$, $n_t$ 分别是重置门、更新门和新状态门。
# - $ \sigma $ 是sigmoid函数。
# - $ \odot $ 是哈达玛积（元素间乘积）。
# 

# torch.nn.GRU(input_size, 
#              hidden_size, 
#              num_layers=1, 
#              bias=True, 
#              batch_first=False, 
#              dropout=0.0, 
#              bidirectional=False, 
#              device=None, 
#              dtype=None)
# 
# ### 参数 (Parameters)
# 
# - **input_size** - 输入x中预期的特征数量。
# - **hidden_size** - 隐藏状态h中的特征数量。
# - **num_layers** - 递归层的数量。例如，设置 `num_layers=2` 表示将两个GRU堆叠在一起形成一个堆叠的GRU，其中第二个GRU接收第一个GRU的输出并计算最终结果。默认值：1。
# - **bias** - 如果为False，则该层不使用偏置权重 `b_ih` 和 `b_hh`。默认值：True。
# - **batch_first** - 如果为True，则输入和输出张量的提供方式为 `(batch, seq, feature)` 而不是 `(seq, batch, feature)`。注意，这不适用于隐藏状态或单元状态。有关详细信息，请参见下面的输入/输出部分。默认值：False。
# - **dropout** - 如果非零，除了最后一层外，在每个GRU层的输出上引入一个Dropout层，Dropout概率等于dropout。默认值：0。
# - **bidirectional** - 如果为True，则成为一个双向GRU。默认值：False。
# 

# ### 输入 (Inputs): `input`, `h_0`
# 
# - **input**: 张量的形状为：
#   - 未分批输入时：`(L, H_in)`，其中 `L` 是序列长度，`H_in` 是输入尺寸。
#   - 当 `batch_first=False` 时：`(L, N, H_in)`，其中 `N` 是批量大小。
#   - 当 `batch_first=True` 时：`(N, L, H_in)`。
#   此输入包含输入序列的特征。输入也可以是打包的变长序列。详情请参见 `torch.nn.utils.rnn.pack_padded_sequence()` 或 `torch.nn.utils.rnn.pack_sequence()`。
# 
# - **h_0**: 张量的形状为：
#   - 未分批输入时：`(D*num_layers, H_out)`，其中 `D` 是方向数（如果双向则为2，否则为1），`num_layers` 是层数，`H_out` 是输出尺寸。
#   - 输入是批量时：`(D*num_layers, N, H_out)`。
#   这个张量包含输入序列中每个元素的初始隐藏状态。如果未提供，其默认值为零。
# 
# 其中：
# - `N` = 批量大小
# - `L` = 序列长度
# - `D` = 如果 `bidirectional=True` 则为2，否则为1
# - `H_in` = 输入尺寸
# - `H_out` = 输出尺寸
# 

# ### 输出 (Outputs): `output`, `h_n`
# 
# - **output**: 张量的形状为：
#   - 未分批输入时：`(L, D*H_out)`，其中 `L` 是序列长度，`D` 是方向数（如果双向则为2，否则为1），`H_out` 是输出尺寸。
#   - 当 `batch_first=False` 时：`(L, N, D*H_out)`，其中 `N` 是批量大小。
#   - 当 `batch_first=True` 时：`(N, L, D*H_out)`。
#   此输出包含GRU最后一层的输出特征 (h_t) 对每个t。如果输入是 `torch.nn.utils.rnn.PackedSequence`，输出也将是一个打包序列。
# 
# - **h_n**: 张量的形状为：
#   - 未分批输入时：`(D*num_layers, H_out)`，其中 `D` 是方向数（如果双向则为2，否则为1），`num_layers` 是层数，`H_out` 是输出尺寸。
#   - 输入是批量时：`(D*num_layers, N, H_out)`。
#   这个张量包含输入序列中每个元素的最终隐藏状态。
# 
# 

# In[19]:


gru = nn.GRU(input_size = 10, hidden_size = 20, num_layers = 1, batch_first=True, dropout=0.0, bidirectional=False)
input = torch.randn(2, 5, 10)
output, hn = gru(input)


# In[20]:


output.shape


# In[21]:


hn.shape


# In[22]:


gru = nn.GRU(input_size = 10, hidden_size = 20, num_layers = 1, batch_first=True)

input = torch.randn(3, 5, 10)

output, hn = gru(input)


# In[23]:


output.shape


# In[24]:


hn.shape


# In[ ]:





# # 深度循环神经网络

# ![image.png](attachment:image.png)

# In[25]:


gru = nn.GRU(input_size = 10, hidden_size = 20, num_layers = 5, batch_first=True)

input = torch.randn(2, 5, 10)

output, hn = gru(input)


# In[26]:


output.shape


# In[27]:


hn.shape


# In[ ]:





# In[ ]:





# # 双向循环神经网络

# ![image.png](attachment:image.png)

# 

# In[28]:


gru = nn.GRU(input_size = 10, hidden_size = 20, num_layers = 1, batch_first=True,bidirectional=True)

input = torch.randn(2, 5, 10)

output, hn = gru(input)


# In[29]:


output.shape


# In[30]:


hn.shape


# In[ ]:





# In[ ]:





# In[31]:


output_sum = (output[:, :, :20] + output[:, :, 20:])


# In[32]:


output_sum.shape


# In[ ]:





# # pack_padded_sequence函数

# 在处理变长序列文本时，单个batch中的样本长度可能不一致。在使用RNN模型时，我们需要将这些样本填充至统一长度，尽管被填充的位置没有实际意义。通常，我们取最后一个有效时刻的输出作为最终输出，但填充后的最后时刻并非原样本的真实最后时刻。为解决这一问题，我们使用 `pack_padded_sequence` 和 `pad_packed_sequence` 两个函数。
# 
# ![image.png](attachment:4513c272-e8f7-49d7-8d95-017b3cc8c7c3.png)
# 
# 
# `pack_padded_sequence`
# 该函数将一个batch中的不同长度样本压缩成一个连续序列。考虑以下一个batch的样本：
# ```
# [[1, 2, 3, 4],
#  [2, 3, 5, 0],
#  [6, 7, 0, 0],
#  [8, 0, 0, 0]]
# ```
# 
# 压缩之后，我们将序列转换成一个列表，即：
# ```
# [1, 2, 6, 8, 2, 3, 7, 3, 5, 4]
# ```
# 并记录原来每个列表的长度，如：
# ```
# size = [4, 3, 2, 1]
# ```
# 因此，经过 `pack_padded_sequence` 处理后，我们得到两个列表：`data=[1, 2, 6, 8, 2, 3, 7, 3, 5, 4]` 和 `size=[4, 3, 2, 1]`。在输入RNN时，按照 `size` 列表的顺序输入数据。
# 
# 完整示例图如下：
# ![image.png](attachment:7859ffab-a90d-4f68-91d6-0890a74a50b7.png)
# 
# 
# `pad_packed_sequence`
# 该函数的作用与 `pack_padded_sequence` 相反，它将压缩的序列重新展开，通常填充值设为0。例如：
# ```
# [[1, 2, 3, 4],
#  [2, 3, 5, 0],
#  [6, 7, 0, 0],
#  [8, 0, 0, 0]]
# ```
# 这里的填充仅为了方便理解，并不代表RNN处理后的实际输出，因为RNN的输出尺寸和维度可能与原始输入不同。

# #### 例子

# In[33]:


embedding_size = 8 # 嵌入向量大小8
hidden_size = 16   # 隐藏向量大小16
vocab_size = 10    # 词汇表大小10


# embedding
embedding = torch.nn.Embedding(vocab_size, embedding_size, padding_idx=0)
# GRU的RNN循环神经网络
gru = torch.nn.GRU(embedding_size, hidden_size)


# In[34]:


from torch.nn.utils.rnn  import pad_sequence


# In[35]:


input_seq = [ torch.tensor([2, 3, 5]), torch.tensor([6, 7]), torch.tensor([8]),torch.tensor([1, 2, 3, 4 ])]

pad_seqs = pad_sequence(input_seq, batch_first=True, padding_value=0)


# In[36]:


pad_seqs


# In[37]:


lengths = (pad_seqs != 0).sum(dim=1)
lengths


# In[ ]:





# In[ ]:





# In[38]:


embeded = embedding(pad_seqs)



# 压缩，设置batch_first为true
pack = torch.nn.utils.rnn.pack_padded_sequence(embeded, lengths, batch_first=True, enforce_sorted=False)                                                   
#packsequencce 数据格式


#　利用gru循环神经网络测试结果
pade_outputs, _ = gru(pack)

print(pade_outputs)

# 设置batch_first为true;你可以不设置为true,为false时候只影响结构不影响结果
pade_outputs, input_sizes = torch.nn.utils.rnn.pad_packed_sequence(pade_outputs, batch_first=True)

# 查看输出的元祖
print(pade_outputs.shape) 
print(input_sizes)


# In[39]:


pade_outputs


# In[40]:


embeded = embedding(torch.tensor(pad_seqs))



#　利用gru循环神经网络测试结果
pade_outputs, _ = gru(embeded)


# 查看输出的元祖
print(pade_outputs) 
print(input_sizes)


# In[ ]:





# In[41]:


last_seq = [pade_outputs[e, i-1, :].unsqueeze(0) for e, i in enumerate(input_sizes)]
# Merge them together
last_seq = torch.cat(last_seq, dim=0) 


# In[42]:


last_seq.shape


# In[43]:


a_list  = []
for e, i in enumerate(input_sizes):
    print(e,i)
    a = pade_outputs[e, i-1, :]   # hidden_size

    print(a)
    a = a.unsqueeze(0)  #1 * hidden_size

    print(a)
    a_list.append(a)
last_seq = torch.cat(a_list, dim=0)   #4 * hidden size


# In[44]:


last_seq.shape


# In[45]:


a_list  = []
for e, i in enumerate(input_sizes):
    print(e,i)
    a = pade_outputs[e, i-1, :]   # hidden_size


 
    a_list.append(a)
last_seq = torch.stack(a_list, dim=0)   #4 * hidden size


# In[46]:


last_seq.shape


# In[ ]:




