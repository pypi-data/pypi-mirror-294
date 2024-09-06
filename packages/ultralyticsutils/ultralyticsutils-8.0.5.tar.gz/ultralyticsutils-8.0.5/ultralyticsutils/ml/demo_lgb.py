import pandas as pd

from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score  # 0.24.2

train = pd.read_csv('data/Credit-Intelligence-Assessment/train_dataset.csv')
test = pd.read_csv('data/Credit-Intelligence-Assessment/test_dataset.csv')
# %%
# print(train.info())
# print(train.head())
test['信用分'] = -1
data_all_sample = pd.concat([train, test]).reset_index(drop=True)
print(data_all_sample.shape)
# %%
features = [i for i in train.columns if i not in ['用户编码', '信用分']]
feats = features
# %%
data_all_sample['缴费方式'] = 0
data_all_sample.loc[(data_all_sample['缴费用户最近一次缴费金额（元）'] != 0) & (
        data_all_sample['缴费用户最近一次缴费金额（元）'] % 10 == 0), '缴费方式'] = 1
data_all_sample.loc[(data_all_sample['缴费用户最近一次缴费金额（元）'] != 0) & (
        data_all_sample['缴费用户最近一次缴费金额（元）'] % 10 > 0), '缴费方式'] = 2
print(data_all_sample['缴费方式'].describe())
print(data_all_sample['缴费方式'].value_counts())
# %% label encoder
cat_col1 = [i for i in data_all_sample.select_dtypes[object].columns if i not in ['用户编码', '信用分']]
lbl = LabelEncoder()
for i in tqdm(cat_col1):
    data_all_sample[i] = lbl.fit_transform(data_all_sample[i].astype(str))
print(data_all_sample.head())
# %%
X = data_all_sample[data_all_sample['信用分'] != -1][feats]
Y = data_all_sample[data_all_sample['信用分'] != -1]['信用分']
train_x, val_x, train_y, vali_y = train_test_split(X.values, Y, test_size=0.3, random_state=2024)
print(train_x.shape, val_x.shape)

# %%
# data_all_sample.corr().


train1 = train[(train['用户当月账户余额（元）'] < 5000) & (train['当月金融理财类应用使用总次数'] < 40000)]


# %%
def fun1(x, c=1):
    return x + 1


fun2 = lambda x: x + 1

print(fun1(1))
print(fun2(1))

a = list(range(5))  # [0, 1, 2, 3, 4]
b = list(map(lambda x: x + 1, a))  # [1, 2, 3, 4, 5]
print(a)
print(b)

#%%
from torch.utils.data import Dataset,DataLoader


#%% 画图 3种图


