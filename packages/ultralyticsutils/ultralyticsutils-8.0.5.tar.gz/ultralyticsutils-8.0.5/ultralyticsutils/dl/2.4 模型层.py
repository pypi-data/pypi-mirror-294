#!/usr/bin/env python
# coding: utf-8

# # 2.2 模型层layers
# 
# 深度学习模型一般由各种模型层组合而成。
# 
# torch.nn中内置了非常丰富的各种模型层。它们都属于nn.Module的子类，具备参数管理功能。
# 
# 例如：
# 
# * nn.Linear, nn.Flatten, nn.Dropout, nn.BatchNorm2d, nn.Embedding
# 
# * nn.Conv2d,nn.AvgPool2d,nn.Conv1d,nn.ConvTranspose2d
# 
# * nn.GRU,nn.LSTM
# 
# * nn.Transformer
# 
# 如果这些内置模型层不能够满足需求，我们也可以通过继承nn.Module基类构建自定义的模型层。
# 
# 实际上，pytorch不区分模型和模型层，都是通过继承nn.Module进行构建。
# 
# 因此，我们只要继承nn.Module基类并实现forward方法即可自定义模型层。
# 
# 
# https://pytorch.org/docs/stable/nn.html

# In[ ]:





# ## 一，基础层

# 一些基础的内置模型层简单介绍如下。
# 
# * nn.Linear：全连接层。参数个数 = 输入层特征数× 输出层特征数(weight)＋ 输出层特征数(bias)
# 
# * nn.Embedding：嵌入层。一种比Onehot更加有效的对离散特征进行编码的方法。一般用于将输入中的单词映射为稠密向量。嵌入层的参数需要学习。
# 
# * nn.Flatten：压平层，用于将多维张量样本压成一维张量样本。
# 
# * nn.BatchNorm1d：一维批标准化层。通过线性变换将输入批次缩放平移到稳定的均值和标准差。可以增强模型对输入不同分布的适应性，加快模型训练速度，有轻微正则化效果。一般在激活函数之前使用。可以用afine参数设置该层是否含有可以训练的参数。
# 
# * nn.BatchNorm2d：二维批标准化层。 常用于CV领域。
# 
# * nn.BatchNorm3d：三维批标准化层。
# 
# * nn.Dropout：一维随机丢弃层。一种正则化手段。
# 
# * nn.Dropout2d：二维随机丢弃层。
# 
# * nn.Dropout3d：三维随机丢弃层。
# 
# * nn.Threshold：限幅层。当输入大于或小于阈值范围时，截断之。
# 
# * nn.ConstantPad2d： 二维常数填充层。对二维张量样本填充常数扩展长度。
# 
# * nn.ReplicationPad1d： 一维复制填充层。对一维张量样本通过复制边缘值填充扩展长度。
# 
# * nn.ZeroPad2d：二维零值填充层。对二维张量样本在边缘填充0值.
# 
# * nn.GroupNorm：组归一化。一种替代批归一化的方法，将通道分成若干组进行归一。不受batch大小限制。
# 
# * nn.LayerNorm：层归一化。常用于NLP领域，不受序列长度不一致影响。
# 
# * nn.InstanceNorm2d: 样本归一化。一般在图像风格迁移任务中效果较好。
# 
# 
# * nn.ReLU  ReLU激活函数
# 
# * nn.Sigmoid  Sigmoid激活函数
# 
# * nn.Tanh   Tanh激活函数
# 
# * nn.Softmax  Softmax激活函数
# 
# 
# 
# 
# 

# In[ ]:





# 重点说说各种归一化层：
# 
# $$y = \frac{x - \mathrm{E}[x]}{ \sqrt{\mathrm{Var}[x] + \epsilon}} * \gamma + \beta$$
# 
# 
# 
# * 结构化数据的BatchNorm1D归一化 【结构化数据的主要区分度来自每个样本特征在全体样本中的排序，将全部样本的某个特征都进行相同的放大缩小平移操作，样本间的区分度基本保持不变，所以结构化数据可以做BatchNorm，但LayerNorm会打乱全体样本根据某个特征的排序关系，引起区分度下降】
# 
# 
# * 图片数据的各种归一化(一般常用BatchNorm2D)【图片数据的主要区分度来自图片中的纹理结构，所以图片数据的归一化一定要在图片的宽高方向上操作以保持纹理结构，此外在Batch维度上操作还能够引入少许的正则化，对提升精度有进一步的帮助。】
# 
# 
# 
# 
# 
# * 文本数据的LayerNorm归一化 【文本数据的主要区分度来自于词向量(Embedding向量)的方向，所以文本数据的归一化一定要在 特征(通道)维度上操作 以保持 词向量方向不变。此外文本数据还有一个重要的特点是不同样本的序列长度往往不一样，所以不可以在Sequence和Batch维度上做归一化，否则将不可避免地让padding位置对应的向量变成非零向量】
# 
# 
# 
# 对BatchNorm需要注意的几点：
# 
# (1)BatchNorm在训练过程和推理过程的逻辑是否一样？
# 
# 不一样！训练过程BatchNorm的均值和方差和根据mini-batch中的数据估计的，而推理过程中BatchNorm的均值和方差是用的训练过程中的全体样本估计的。因此预测过程是稳定的，相同的样本不会因为所在批次的差异得到不同的结果，但训练过程中则会受到批次中其他样本的影响所以有正则化效果。
# 
# (2)BatchNorm的精度效果与batch_size大小有何关系? 
# 
# 如果受到GPU内存限制，不得不使用很小的batch_size，训练阶段时使用的mini-batch上的均值和方差的估计和预测阶段时使用的全体样本上的均值和方差的估计差异可能会较大，效果会变差。这时候，可以尝试LayerNorm或者GroupNorm等归一化方法。
# 

# In[ ]:





# In[ ]:





# In[8]:


import torch 
from torch import nn 

batch_size, channel, height, width = 32, 16, 128, 128

tensor = torch.arange(0,32*16*128*128).view(32,16,128,128).float() 

# BatchNorm2d 会计算该批次数据中每个通道的均值和方差。对每个通道的特征图进行归一化处理，使得输出的每个通道的特征图的均值为 0，方差为 1。
bn = nn.BatchNorm2d(num_features=channel,affine=False)

# 1.num_features：一般输入参数为batch_size*num_features*height*width，即为其中特征的数量
# 2.affine：当设为true时，会给定可以学习的系数矩阵gamma和beta

bn_out = bn(tensor)


channel_mean = torch.mean(bn_out[:,0,:,:]) 
channel_std = torch.std(bn_out[:,0,:,:])
print("channel mean:",channel_mean.item())
print("channel std:",channel_std.item())



# In[9]:


channel_mean = torch.mean(bn_out[:,1,:,:]) 
channel_std = torch.std(bn_out[:,1,:,:])
print("channel mean:",channel_mean.item())
print("channel std:",channel_std.item())


# In[ ]:





# In[10]:


import torch 
from torch import nn 

batch_size, sequence, features = 32, 100, 2048
tensor = torch.arange(0,32*100*2048).view(32,100,2048).float() 

# 对于每个样本中的每个时间步，层归一化会在所有特征 上独立计算均值和方差。
ln = nn.LayerNorm(normalized_shape=[features],
                  elementwise_affine = False)

ln_out = ln(tensor)

token_mean = torch.mean(ln_out[0,0,:]) 
token_std = torch.std(ln_out[0,0,:])
print("token_mean:",token_mean.item())
print("token_std:",token_std.item())



# ## 二，卷积网络相关层
# 

# 一些与卷积相关的内置层介绍如下
# 
# * nn.Conv1d：普通一维卷积，常用于文本。参数个数 = 输入通道数×卷积核尺寸(如3)×卷积核个数 + 卷积核尺寸(如3）
#   
# * nn.Conv2d：普通二维卷积，常用于图像。参数个数 = 输入通道数×卷积核尺寸(如3乘3)×卷积核个数 + 卷积核尺寸(如3乘3)。) 通过调整dilation参数大于1，可以变成空洞卷积，增加感受野。 通过调整groups参数不为1，可以变成分组卷积。分组卷积中每个卷积核仅对其对应的一个分组进行操作。 当groups参数数量等于输入通道数时，相当于tensorflow中的二维深度卷积层tf.keras.layers.DepthwiseConv2D。 利用分组卷积和1乘1卷积的组合操作，可以构造相当于Keras中的二维深度可分离卷积层tf.keras.layers.SeparableConv2D。
# 
# * nn.Conv3d：普通三维卷积，常用于视频。参数个数 = 输入通道数×卷积核尺寸(如3乘3乘3)×卷积核个数 + 卷积核尺寸(如3乘3乘3) 。
# 
# * nn.MaxPool1d: 一维最大池化。
# 
# * nn.MaxPool2d：二维最大池化。一种下采样方式。没有需要训练的参数。
# 
# * nn.MaxPool3d：三维最大池化。
# 
# * nn.AdaptiveMaxPool2d：二维自适应最大池化。无论输入图像的尺寸如何变化，输出的图像尺寸是固定的。
#   该函数的实现原理，大概是通过输入图像的尺寸和要得到的输出图像的尺寸来反向推算池化算子的padding,stride等参数。
#   
# * nn.FractionalMaxPool2d：二维分数最大池化。普通最大池化通常输入尺寸是输出的整数倍。而分数最大池化则可以不必是整数。分数最大池化使用了一些随机采样策略，有一定的正则效果，可以用它来代替普通最大池化和Dropout层。
# 
# * nn.AvgPool2d：二维平均池化。
# 
# * nn.AdaptiveAvgPool2d：二维自适应平均池化。无论输入的维度如何变化，输出的维度是固定的。
# 
# * nn.ConvTranspose2d：二维卷积转置层，俗称反卷积层。并非卷积的逆操作，但在卷积核相同的情况下，当其输入尺寸是卷积操作输出尺寸的情况下，卷积转置的输出尺寸恰好是卷积操作的输入尺寸。在语义分割中可用于上采样。
# 
# * nn.Upsample：上采样层，操作效果和池化相反。可以通过mode参数控制上采样策略为"nearest"最邻近策略或"linear"线性插值策略。
# 
# * nn.Unfold：滑动窗口提取层。其参数和卷积操作nn.Conv2d相同。实际上，卷积操作可以等价于nn.Unfold和nn.Linear以及nn.Fold的一个组合。
#   其中nn.Unfold操作可以从输入中提取各个滑动窗口的数值矩阵，并将其压平成一维。利用nn.Linear将nn.Unfold的输出和卷积核做乘法后，再使用
#   nn.Fold操作将结果转换成输出图片形状。
# 
# * nn.Fold：逆滑动窗口提取层。
# 

# In[ ]:





# In[3]:


import torch 
from torch import nn 
import torch.nn.functional as F 

# 卷积输出尺寸计算公式 o = (i + 2*p -k')//s  + 1 
# 对空洞卷积 k' = d(k-1) + 1
# o是输出尺寸，i 是输入尺寸，p是 padding大小， k 是卷积核尺寸， s是stride步长, d是dilation空洞参数

inputs = torch.arange(0,25).view(1,1,5,5).float() # i= 5
filters = torch.tensor([[[[1.0,1],[1,1]]]]) # k = 2

outputs = F.conv2d(inputs, filters) # o = (5+2*0-2)//1+1 = 4
outputs_s2 = F.conv2d(inputs, filters, stride=2)  #o = (5+2*0-2)//2+1 = 2
outputs_p1 = F.conv2d(inputs, filters, padding=1) #o = (5+2*1-2)//1+1 = 6
outputs_d2 = F.conv2d(inputs,filters, dilation=2) #o = (5+2*0-(2(2-1)+1))//1+1 = 3

print("--inputs--")
print(inputs)
print("--filters--")
print(filters)

print("--outputs--")
print(outputs,"\n")

print("--outputs(stride=2)--")
print(outputs_s2,"\n")

print("--outputs(padding=1)--")
print(outputs_p1,"\n")

print("--outputs(dilation=2)--")
print(outputs_d2,"\n")



# In[ ]:





# ## 三，循环网络相关层

# 
# 
# * nn.LSTM：长短记忆循环网络层【支持多层】。最普遍使用的循环网络层。具有携带轨道，遗忘门，更新门，输出门。可以较为有效地缓解梯度消失问题，从而能够适用长期依赖问题。设置bidirectional = True时可以得到双向LSTM。需要注意的时，默认的输入和输出形状是(seq,batch,feature), 如果需要将batch维度放在第0维，则要设置batch_first参数设置为True。
# 
# * nn.GRU：门控循环网络层【支持多层】。LSTM的低配版，不具有携带轨道，参数数量少于LSTM，训练速度更快。
# 
# * nn.RNN：简单循环网络层【支持多层】。容易存在梯度消失，不能够适用长期依赖问题。一般较少使用。
# 
# * nn.LSTMCell：长短记忆循环网络单元。和nn.LSTM在整个序列上迭代相比，它仅在序列上迭代一步。一般较少使用。
# 
# * nn.GRUCell：门控循环网络单元。和nn.GRU在整个序列上迭代相比，它仅在序列上迭代一步。一般较少使用。
# 
# * nn.RNNCell：简单循环网络单元。和nn.RNN在整个序列上迭代相比，它仅在序列上迭代一步。一般较少使用。
# 

# 
# 
# 一般地，各种RNN序列模型层(RNN,GRU,LSTM等)可以用函数表示如下:
# 
# $$h_t = f(h_{t-1},x_t)$$
# 
# 这个公式的含义是：t时刻循环神经网络的输出向量$h_t$由t-1时刻的输出向量$h_{t-1}$和t时刻的输入$i_t$变换而来。
# 
# 

# * LSTM 结构解析 
# 
# 参考文章：《人人都能看懂的LSTM》https://zhuanlan.zhihu.com/p/32085405
# 
# LSTM通过引入了三个门来控制信息的传递，分别是遗忘门，输入门 和输出门 。三个门的作用为：
# 
# （1）遗忘门: 遗忘门$f_t$控制上一时刻的内部状态  需要遗忘多少信息；
# 
# （2）输入门: 输入门$i_t$控制当前时刻的候选状态  有多少信息需要保存；
# 
# （3）输出门: 输出门$o_t$控制当前时刻的内部状态  有多少信息需要输出给外部状态  ；
# 
# 
# $$
# \begin{align}
# i_{t}=\sigma\left(W_{i} x_{t}+U_{i} h_{t-1}+b_{i}\right) \tag{1} \\
# f_{t}=\sigma\left(W_{f} x_{t}+U_{f} h_{t-1}+b_{f}\right) \tag{2} \\
# o_{t}=\sigma\left(W_{o} x_{t}+U_{o} h_{t-1}+b_{o}\right) \tag{3} \\
# \tilde{c}_{t}=\tanh \left(W_{c} x_{t}+U_{c} h_{t-1}+b_{c}\right) \tag{4} \\
# c_{t}=f_{t} \odot c_{t-1}+i_{t} \odot \tilde{c}_{t} \tag{5} \\
# h_{t}=o_{t} \odot \tanh \left(c_{t}\right) \tag{6}
# \end{align}
# $$
# 
# 
# 
# 

# * GRU 结构解析
# 
# 参考文章：《人人都能看懂的GRU》https://zhuanlan.zhihu.com/p/32481747
# 
# GRU的结构比LSTM更为简单一些，GRU只有两个门，更新门和重置门  。
# 
# （1）更新门：更新门用于控制每一步$h_t$被更新的比例，更新门越大，$h_t$更新幅度越大。
# 
# （2）重置门：重置门用于控制更新候选向量$\tilde{h}_{t}$中前一步的状态$h_{t-1}$被重新放入的比例，重置门越大，更新候选向量中$h_{t-1}$被重新放进来的比例越大。
# 
# 
# 
# 
# 公式中的小圈表示哈达玛积，也就是两个向量逐位相乘。
# 
# 其中(1)式和(2)式计算的是更新门$u_t$和重置门$r_t$，是两个长度和$h_t$相同的向量。
# 
# 
# 注意到(4)式 实际上和ResNet的残差结构是相似的，都是 f(x) = x + g(x) 的形式，可以有效地防止长序列学习反向传播过程中梯度消失问题。
# 
# 
# 
# $$
# \begin{align}
# z_{t}=\sigma\left(W_{z} x_{t}+U_{z} h_{t-1}+b_{z}\right)\tag{1} \\
# r_{t}=\sigma\left(W_{r} x_{t}+U_{r} h_{t-1}+b_{r}\right) \tag{2}\\
# \tilde{h}_{t}=\tanh \left(W_{h} x_{t}+U_{h}\left(r_{t} \odot h_{t-1}\right)+b_{h}\right) \tag{3}\\
# h_{t}= h_{t-1} - z_{t}\odot h_{t-1}  + z_{t} \odot  \tilde{h}_{t} \tag{4}
# \end{align}
# $$
# GRU的参数数量为LSTM的3/4.
# 
# 

# In[4]:


import torch 
from torch import nn 

inputs = torch.randn(8,200,64) #batch_size, seq_length, features

gru = nn.GRU(input_size=64,hidden_size=32,num_layers=1,batch_first=True)
gru_output,gru_hn = gru(inputs)
print("--GRU--")
print("gru_output.shape:",gru_output.shape)
print("gru_hn.shape:",gru_hn.shape)
print("\n")


print("--LSTM--")
lstm = nn.LSTM(input_size=64,hidden_size=32,num_layers=1,batch_first=True)
lstm_output,(lstm_hn,lstm_cn) = lstm(inputs)
print("lstm_output.shape:",lstm_output.shape)
print("lstm_hn.shape:",lstm_hn.shape)  #最后的隐藏层
print("lstm_cn.shape:",lstm_cn.shape)  #记忆单元





# In[5]:


9408/12544 


# In[ ]:





# ## 四，Transformer相关层

# * nn.Transformer：Transformer网络结构。Transformer网络结构是替代循环网络的一种结构，解决了循环网络难以并行，难以捕捉长期依赖的缺陷。它是目前NLP任务的主流模型的主要构成部分。
# 
# * nn.TransformerEncoder：Transformer编码器结构。由多个 nn.TransformerEncoderLayer编码器层组成。
# 
# * nn.TransformerDecoder：Transformer解码器结构。由多个 nn.TransformerDecoderLayer解码器层组成。
# 
# * nn.TransformerEncoderLayer：Transformer的编码器层。主要由Multi-Head self-Attention, Feed-Forward前馈网络, LayerNorm归一化层, 以及残差连接层组成。
# 
# * nn.TransformerDecoderLayer：Transformer的解码器层。主要由Masked Multi-Head self-Attention, Multi-Head cross-Attention, Feed-Forward前馈网络, LayerNorm归一化层, 以及残差连接层组成。
# 
# * nn.MultiheadAttention：多头注意力层。用于在序列方向上融合特征。使用的是Scaled Dot Production Attention，并引入了多个注意力头。
# 
# 
# $$\operatorname{Attention}(Q, K, V)=\operatorname{softmax}\left(\frac{Q K^{T}}{\sqrt{d_{k}}}\right) V$$ 
# 
# $$\begin{aligned}
# \operatorname{MultiHead}(Q, K, V) &=\operatorname{Concat}\left(\operatorname{head}_{1}, \ldots, \text { head }_{\mathrm{h}}\right) W^{O} \\
# \text { where }\, head_{i} &=\operatorname{Attention}\left(Q W_{i}^{Q}, K W_{i}^{K}, V W_{i}^{V}\right)
# \end{aligned}$$
# 
# 
# ![image.png](attachment:427a6dd9-8c2c-4c48-95b8-416822513356.png)

# 参考阅读材料： 
# 
# Transformer知乎原理讲解：https://zhuanlan.zhihu.com/p/48508221
# 
# Transformer哈佛博客代码讲解：http://nlp.seas.harvard.edu/annotated-transformer/ 
# 

# In[1]:


import torch 
from torch import nn 

#验证MultiheadAttention和head数量无关
inputs = torch.randn(8,200,64) #batch_size, seq_length, features

attention_h8 = nn.MultiheadAttention(
    embed_dim = 64,
    num_heads = 8,
    bias=True,
    batch_first=True
)

attention_h16 = nn.MultiheadAttention(
    embed_dim = 64,
    num_heads = 16,
    bias=True,
    batch_first=True
)


out_h8 = attention_h8(inputs,inputs,inputs)
out_h16 = attention_h16(inputs,inputs,inputs)



# In[2]:


out_h8[1].shape


# In[5]:


len(out_h8)


# In[7]:


out_h8[0].shape


# In[ ]:




