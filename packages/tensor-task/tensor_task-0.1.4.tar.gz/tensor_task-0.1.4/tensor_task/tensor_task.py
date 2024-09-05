def f1():
	s = '''
将文本数据读取为table数据

import os
os.chdir('/Users/zhangwentao/Desktop/work/工作/2024/燎原计划')
import pandas as pd

# 定义数据路径
data_dir = './data/点评语料'

# 创建空的 DataFrame
columns = ['review', 'label']
df = pd.DataFrame(columns=columns)

# 读取 pos 文件夹中的文件
pos_dir = os.path.join(data_dir, 'pos')
for filename in os.listdir(pos_dir):
    filepath = os.path.join(pos_dir, filename)
    with open(filepath, 'r', encoding='gbk', errors='ignore') as file:
            text = file.read()
            text = text.strip()
            text = text.replace('\n', '')
            text = text.replace(' ', '')
            df = df.append({'review': text, 'label': 1}, ignore_index=True)
        

# 读取 neg 文件夹中的文件
neg_dir = os.path.join(data_dir, 'neg')
for filename in os.listdir(neg_dir):
    filepath = os.path.join(neg_dir, filename)
    with open(filepath, 'r', encoding='gbk', errors='ignore') as file:
            text = file.read()
            text = text.strip()
            text = text.replace('\n', '')
            text = text.replace(' ', '')
            df = df.append({'review': text, 'label': 0}, ignore_index=True)

# 保存为 CSV 文件
output_path = './data/dp_comments2.csv'
df.to_csv(output_path, index=False)
	'''
	return s



def f2():
	s = '''
数据读取

file_path = './data/dp_comments2.csv'
import pandas as pd
df3 = pd.read_csv(file_path)

reviews = df3['review'].tolist()
labels = df3['label'].tolist()
df3.head(2)
	'''
	return s


def f3():
	s = '''
分词、停用词、小写化

# 处理文本
vocab = set()

import jieba
def tokenize(text):
    tokens = jieba.lcut(text.lower())
    return [token for token in tokens if token not in stopwords]

# 预处理
tokenized_reviews = [tokenize(review) for review in reviews]

# 查看最长句子的分词长度 作为后续max_len的参考 max_len不可大于此数值
max([len(review) for review in tokenized_reviews])
	'''
	return s


def f4():
	s = '''
生成词汇表、索引、转化分词结果

# 生成词汇表
for review_list in tokenized_reviews:
    for word in review_list:
        vocab.add(word)

len(vocab)

# 生成索引
word_to_idx = {word: i for i, word in enumerate(vocab)} 
idx_to_word = {i: word for i, word in enumerate(vocab)}  

len(word_to_idx)

# 按照索引，将评论转换为向量 不足的长度0填充
texts = []
max_len = 100

for review_list in tokenized_reviews:
    seq = [word_to_idx[word] if word in word_to_idx else 0 for word in review_list[:max_len]]  
    seq += [0] * (max_len - len(seq))  # padding 0
    texts.append(seq)

len(texts)

	'''
	return s


def f5():
	s = '''
数据集准备

# 生成数据集

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(torch.tensor(texts), torch.tensor(labels), test_size=0.25, random_state=42)


train_dataset = TensorDataset(X_train,y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

test_dataset = TensorDataset(X_test,y_test)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
	'''
	return s




def f6():
	s = '''
lstm 模型定义及实例化
# 模型修改 需要增加一层embedding
# 模型准备
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, input_size, hidden_size, output_size, num_layers, bidirectional, dropout=0):
        super().__init__()
        self.num_layers = num_layers
        self.embedding = nn.Embedding(vocab_size, input_size)  
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=bidirectional, dropout=dropout)
        self.fc = nn.Linear(hidden_size * 2 if bidirectional else hidden_size, output_size)
        #self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embedding(x)
        h_0 = torch.zeros(self.num_layers * 2 if bidirectional else self.num_layers, x.size(0), hidden_size).to(x.device)
        c_0 = torch.zeros(self.num_layers * 2 if bidirectional else self.num_layers, x.size(0), hidden_size).to(x.device)
        out, _ = self.lstm(x, (h_0, c_0))
        out = self.fc(out[:, -1, :])
        #out = self.sigmoid(out)
        return out


# 计算测试集的准确率 acc函数
def evaluate(model, dataloader):
    model.eval()  # Set the model to evaluation mode
    correct = 0
    total = 0
    with torch.no_grad():
        for X, y in dataloader:
            outputs = model(X)
            _, predicted = torch.max(outputs, 1)
            total += y.size(0)
            correct += (predicted == y).sum().item()

    return correct / total

# 实例化
# 创建model部分前移至这里，方便改参数
vocab_size = len(word_to_idx) + 1 # vocabulary_siza
input_size = max_len  # word2vec vector size 即 max_len
hidden_size = 64
output_size = 2  # binary classification
num_layers = 2
bidirectional = True
dropout = 0.4

model = LSTMClassifier(vocab_size, input_size, hidden_size, output_size, num_layers, bidirectional)
	'''
	return s


def f7():
	s = '''
训练代码

import torch.optim as optim

criterion = nn.CrossEntropyLoss() # 分类的损失函数 交叉墒
optimizer = optim.Adam(model.parameters(), lr=0.01)

num_epochs = 10  # Number of epochs

for epoch in range(num_epochs):
    # Training Phase
    model.train()  # Set the model to training mode
    running_loss = 0.0
    corrects_sum = 0

    for X, y in train_loader:
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        # 训练集准确率
        _, predicted = torch.max(outputs, 1)
        corrects_sum += torch.sum(predicted == y.data)

    # Calculate average training loss
    avg_train_loss = running_loss / len(train_loader)

    # 训练集准确率
    train_accuracy = corrects_sum / len(train_dataset)

    # Evaluation Phase
    test_accuracy = evaluate(model, test_loader)

    print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, Test Accuracy: {test_accuracy:.4f}')

	'''
	return s


#### cv

def f8():
	s = '''
读取数据、构建标签索引

import torch
from torch import nn
import numpy as np
# 数据打包
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

# 图像读取
from matplotlib import pyplot as plt
import cv2
from PIL import Image # 推荐

# 图像预处理
from torchvision.transforms import ToTensor
from torchvision.transforms import Normalize

# CPU GPU 检测
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
device
import os

os.chdir('/Users/zhangwentao/Desktop/work/工作/2024/燎原计划')
print(os.getcwd())

# 读取训练集
train_root = "./data/gestures/train/"
X_train = []
y_train = []
for label in os.listdir(train_root):
    label_root = os.path.join(train_root, label)
    for file in os.listdir(label_root):
        file_path = os.path.join(label_root, file)
        X_train.append(file_path)
        y_train.append(label)

# 读取测试集
test_root = "./data/gestures/test/"
X_test = []
y_test = []
for label in os.listdir(test_root):
    label_root = os.path.join(test_root, label)
    for file in os.listdir(label_root):
        file_path = os.path.join(label_root, file)
        X_test.append(file_path)
        y_test.append(label)

生成标签索引
label_list = list(set(y_train))
label_list.sort()

label2idx = {label: idx for idx, label in enumerate(label_list)}
idx2label = {idx: label for idx, label in enumerate(label_list)}

print(label2idx)
print(idx2label)
	'''
	return s

def f9():
	s = '''
图像数据集定义
# 继承 Dataset 自定义一个数据集，实现按数据的单样本索引
class MyDataset(Dataset):
    
    def __init__(self, X, y):
        self.X = X
        self.y = y
        
    def __getitem__(self, idx):
        """
            特征
            索引
        """
        
        img_file = self.X[idx] # 已经是矩阵
        img_label = self.y[idx] # 一元值
        
        # 特征
        img = Image.open(fp=img_file)
        img = img.resize((128, 128))
        # [C, H, W]
        # [0, 1]
        img = ToTensor()(img) # 默认处理成 [0, 1]范围内的值 建议转化为[-1, 1] 即 (value - 0.5) / 0.5
        img = Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])(img) # 用normalize实现
        
        
        # 索引 -- 一元值 long形式即可
        label = torch.tensor(data=label2idx.get(img_label), dtype=torch.long)
        
        return img, label

    def __len__(self):
        """
            样本个数
        """
        return len(self.X)


# 训练集打包
train_dataset = MyDataset(X=X_train, y=y_train)
train_dataloader = DataLoader(dataset=train_dataset, 
                              batch_size=8, 
                              shuffle=True,
                              drop_last=False)

# 测试集打包
test_dataset = MyDataset(X=X_test, y=y_test)
test_dataloader = DataLoader(dataset=test_dataset, 
                              batch_size=16, 
                              shuffle=False)
	'''
	return s


def f10():
	s = '''
模型定义、实例化
# 自定义
class MyModel(nn.Module): #nn.Module是父类，继承后可直接用nn.Module的方法
    
        自定义一个类
        '__init__' 中 实例化层 类 --> 对象
        'forward' 中 把对象当作函数使用，都是可callback的
        输入：图像
        输出：概率
    
    def __init__(self, img_size=128, num_classes=10):
        
            1、接收和处理超参数
            2、定义需要的层
        
        super().__init__() # 系统自动初始化父类 否则会报错 : cannot assign module before Module.__init__() call
        
        self.num_classes = num_classes
        
        # 卷积 抽取特征
        self.conv1 = nn.Conv2d(in_channels=3,
                               out_channels=8,
                               kernel_size=3, # 卷积核个数，基本固定
                               stride=1, # 每次卷积完毕后移动几个单元格
                               padding=1 # 原始像素外圈补1 防止像素损失
                              )
        # batch norml 批规范化
        self.bn1 = nn.BatchNorm2d(num_features=8)
        # relu
        self.relu1 = nn.ReLU()
        # 池化
        self.mp1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        
        
        # 卷积 抽取特征
        self.conv2 = nn.Conv2d(in_channels=8,
                               out_channels=16,
                               kernel_size=3, # 卷积核个数，基本固定
                               stride=1, # 每次卷积完毕后移动几个单元格
                               padding=1 # 原始像素外圈补1 防止像素损失
                              )
        # batch norml 批规范化
        self.bn2 = nn.BatchNorm2d(num_features=16)
        # relu
        self.relu2 = nn.ReLU()
        # 池化
        self.mp2 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        
        
        # 卷积 抽取特征
        self.conv3 = nn.Conv2d(in_channels=16,
                               out_channels=32,
                               kernel_size=3, # 卷积核个数，基本固定
                               stride=1, # 每次卷积完毕后移动几个单元格
                               padding=1 # 原始像素外圈补1 防止像素损失
                              )
        # batch norml 批规范化
        self.bn3 = nn.BatchNorm2d(num_features=32)
        # relu
        self.relu3 = nn.ReLU()
        # 池化
        self.mp3 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        
        # 为了矩阵计算 reshape [N, C, H, W] --> [N, num_features]
        self.flatten = nn.Flatten()
        
        
        
        
        # 全连接
        self.linear1 = nn.Linear(in_features=8192, out_features=512)
        self.relu4 = nn.ReLU()
        
        self.linear2 = nn.Linear(in_features=512, out_features=self.num_classes)
        
        
    
    def forward(self, x):
        
            调用在 '__init__' 定义的对象，来完成正向传播
            引入relu 让其变成非线形比较好
        
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.mp1(x)
        
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.mp2(x)
        
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.mp3(x)
        
        x = self.flatten(x)
        
        x = self.linear1(x)
        x = self.relu4(x)

        x = self.linear2(x)
        return x

# 实例化一个模型
model = MyModel(num_classes=10)
model.to(device=device)
# 训练轮次
epochs = 30
# 优化器
optimizer = torch.optim.SGD(params=model.parameters(), lr=1e-3)
# 误差度量方法 多分类 直接用交叉墒
loss_fn = nn.CrossEntropyLoss()

	'''
	return s




def f11():
	s = '''
训练

def get_acc(model, data_loader):
    """
        过程监控
            - 评估模型性能
    """
    accs = []
    model.eval() # 默认train模式，计算这一批数据的准确率 一般回归任务可用  eval模式计算截至目前的准确率 一般分类任务可用
    with torch.no_grad(): # 节省性能 不画DAG图
        for X, y in data_loader:
            X = X.to(device=device)
            y = y.to(device=device)
            y_pred = model(X)
            y_pred = y_pred.argmax(dim=1)
            acc = (y_pred == y).to(dtype=torch.float32).mean() # 这一批次的准确率
            accs.append(acc.item())
    return sum(accs) / len(accs) # 截至目前的准确率
train_accs = []
test_accs = []

def train():    
    # 读取之前的模型当作最优模型，有更好的模型则更新
    # 加载模型
    #best_model = MyModel(num_classes=10)
    #best_model.load_state_dict(state_dict=torch.load(f="./model/best_model.pt", weights_only=True))
    #best_acc = get_acc(best_model, data_loader=test_dataloader)
    
    # 开始之前，先计算损失有多少
    train_acc = get_acc(model, data_loader=train_dataloader)
    test_acc = get_acc(model, data_loader=test_dataloader)
    print(f"开始训练之前：train_acc: {train_acc}, test_acc: {test_acc}")
    train_accs.append(train_acc)
    test_accs.append(test_acc)
    for epoch in range(epochs):
        model.train()
        for X, y in train_dataloader:
            # 数据搬家
            X = X.to(device=device)
            y = y.to(device=device)
            # forward 方法，正向传播
            # 内部构建一个计算图 DAG
            y_pred = model(X)
            # 计算损失(loss是个单值函数)
            loss = loss_fn(y_pred, y)
            # 反向传播
            loss.backward()
            # 优化一步
            optimizer.step()
            # 清空梯度
            optimizer.zero_grad() 
        # 每一轮结束，计算损失当前有多少
        train_acc = get_acc(model, data_loader=train_dataloader)
        test_acc = get_acc(model, data_loader=test_dataloader)
        print(f"当前轮次：{epoch + 1}, train_acc: {train_acc}, test_acc: {test_acc}")
        train_accs.append(train_acc)
        test_accs.append(test_acc)
        # 保存当前模型为 last.pt
        #torch.save(obj=model.state_dict(), f="./model/last_model.pt")
        # 如果遇到了更好的模型，则更新/保存 best.pt
        #if test_acc > best_acc:
            #best_acc = test_acc
            #torch.save(obj=model.state_dict(), f="./model/best_model.pt")
	'''
	return s




