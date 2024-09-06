{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "研究目的：\n",
    "\n",
    "1 了解客户流失的大体状况   \n",
    "2 探究是什么原因造成了用户流失。如：流失的客户有哪些共同点；使用哪些服务的用户流失较为严重"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "_cell_guid": "79c7e3d0-c299-4dcb-8224-4455121ee9b0",
    "_uuid": "d629ff2d2480ee46fbb7e2d37f6b5fab8052498a"
   },
   "source": [
    "**背景说明：**\n",
    "\n",
    "客户流失是电信行业最大的问题之一。客户流失率通常作为公司的一个关键业务指标，因为留住一个现有客户的成本远远低于获得一个新客户的成本。所以对于公司来说，恢复的长期客户比新招募的客户更有价值。电信客户流失预测有助于公司发现潜在的流失客户，并及时采取相应措施，对其进行赢回。此处的‘流失’主要针对自愿流失客户，即自主停止服务或切换到其他公司。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "数据说明：\n",
    "\n",
    "这个数据集包含电信客户的多种信息，以及他们是否在上个月流失了。数据中，每一行代表一个客户，每一列为该客户的不同属性。这些属性主要包括客户订购的服务、帐户信息和个人信息。我们将使用Python和Seaborn库结合特征工程、逻辑回归、随机森林来进行数据分析。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 模型构建、预测，并输出决策树图形"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "from scipy import stats\n",
    "import matplotlib.pyplot as plt\n",
    "plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'\n",
    "plt.rcParams['axes.unicode_minus'] = False\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\")\n",
    "%matplotlib inline\n",
    "rc = {'font.sans-serif': 'SimHei',\n",
    "      'axes.unicode_minus': False}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>SeniorCitizen</th>\n",
       "      <th>Partner</th>\n",
       "      <th>Dependents</th>\n",
       "      <th>OnlineSecurity</th>\n",
       "      <th>TechSupport</th>\n",
       "      <th>PaperlessBilling</th>\n",
       "      <th>MonthlyCharges</th>\n",
       "      <th>TotalCharges</th>\n",
       "      <th>Churn</th>\n",
       "      <th>InternetService_DSL</th>\n",
       "      <th>InternetService_Fiber optic</th>\n",
       "      <th>InternetService_No</th>\n",
       "      <th>Contract_Month-to-month</th>\n",
       "      <th>Contract_One year</th>\n",
       "      <th>Contract_Two year</th>\n",
       "      <th>PaymentMethod_Bank transfer (automatic)</th>\n",
       "      <th>PaymentMethod_Credit card (automatic)</th>\n",
       "      <th>PaymentMethod_Electronic check</th>\n",
       "      <th>tenure_label</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>29.85</td>\n",
       "      <td>29.85</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>56.95</td>\n",
       "      <td>1889.50</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>53.85</td>\n",
       "      <td>108.15</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>42.30</td>\n",
       "      <td>1840.75</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>4</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>70.70</td>\n",
       "      <td>151.65</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   SeniorCitizen  Partner  Dependents  OnlineSecurity  TechSupport  \\\n",
       "0              0        1           0               0            0   \n",
       "1              0        0           0               1            0   \n",
       "2              0        0           0               1            0   \n",
       "3              0        0           0               1            1   \n",
       "4              0        0           0               0            0   \n",
       "\n",
       "   PaperlessBilling  MonthlyCharges  TotalCharges  Churn  InternetService_DSL  \\\n",
       "0                 1           29.85         29.85      0                    1   \n",
       "1                 0           56.95       1889.50      0                    1   \n",
       "2                 1           53.85        108.15      1                    1   \n",
       "3                 0           42.30       1840.75      0                    1   \n",
       "4                 1           70.70        151.65      1                    0   \n",
       "\n",
       "   InternetService_Fiber optic  InternetService_No  Contract_Month-to-month  \\\n",
       "0                            0                   0                        1   \n",
       "1                            0                   0                        0   \n",
       "2                            0                   0                        1   \n",
       "3                            0                   0                        0   \n",
       "4                            1                   0                        1   \n",
       "\n",
       "   Contract_One year  Contract_Two year  \\\n",
       "0                  0                  0   \n",
       "1                  1                  0   \n",
       "2                  0                  0   \n",
       "3                  1                  0   \n",
       "4                  0                  0   \n",
       "\n",
       "   PaymentMethod_Bank transfer (automatic)  \\\n",
       "0                                        0   \n",
       "1                                        0   \n",
       "2                                        0   \n",
       "3                                        1   \n",
       "4                                        0   \n",
       "\n",
       "   PaymentMethod_Credit card (automatic)  PaymentMethod_Electronic check  \\\n",
       "0                                      0                               1   \n",
       "1                                      0                               0   \n",
       "2                                      0                               0   \n",
       "3                                      0                               0   \n",
       "4                                      0                               1   \n",
       "\n",
       "   tenure_label  \n",
       "0             1  \n",
       "1             3  \n",
       "2             1  \n",
       "3             4  \n",
       "4             1  "
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "churn1 = pd.read_csv('./data.csv')\n",
    "churn1.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.tree import DecisionTreeClassifier\n",
    "#网格搜索\n",
    "from sklearn.model_selection import GridSearchCV\n",
    "#交叉验证\n",
    "from sklearn.model_selection import StratifiedKFold"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(array([0.73421497, 0.73421497, 0.73421497, 0.73421497, 0.73421497,\n",
       "        0.73421497, 0.73421497, 0.73421497, 0.73421497, 0.762087  ,\n",
       "        0.762087  , 0.762087  , 0.762087  , 0.762087  , 0.762087  ,\n",
       "        0.762087  , 0.762087  , 0.762087  , 0.78611915, 0.78611915,\n",
       "        0.78611915, 0.78611915, 0.78611915, 0.78611915, 0.78611915,\n",
       "        0.78611915, 0.78611915, 0.78640304, 0.78640304, 0.78640304,\n",
       "        0.78640304, 0.78640304, 0.78640304, 0.78640304, 0.78640304,\n",
       "        0.78640304, 0.78825367, 0.78825367, 0.78825367, 0.78825367,\n",
       "        0.78825367, 0.78825367, 0.78853816, 0.78853816, 0.78853816,\n",
       "        0.79024493, 0.79024493, 0.79038718, 0.79109862, 0.79109862,\n",
       "        0.79109862, 0.79166761, 0.79166761, 0.79166761, 0.78910695,\n",
       "        0.78882246, 0.7892492 , 0.79024493, 0.78981859, 0.79024433,\n",
       "        0.79067188, 0.79067188, 0.79067188, 0.78014617, 0.78000453,\n",
       "        0.78014637, 0.7811421 , 0.78227948, 0.78028963, 0.78071677,\n",
       "        0.78185395, 0.78156965, 0.77332051, 0.77232538, 0.77232457,\n",
       "        0.77403195, 0.77332112, 0.77303601, 0.77289599, 0.77360682,\n",
       "        0.77403357, 0.73421497, 0.73421497, 0.73421497, 0.73421497,\n",
       "        0.73421497, 0.73421497, 0.73421497, 0.73421497, 0.73421497,\n",
       "        0.762087  , 0.762087  , 0.762087  , 0.762087  , 0.762087  ,\n",
       "        0.762087  , 0.762087  , 0.762087  , 0.762087  , 0.78654589,\n",
       "        0.78654589, 0.78654589, 0.78654589, 0.78654589, 0.78654589,\n",
       "        0.78654589, 0.78654589, 0.78654589, 0.78739776, 0.78739776,\n",
       "        0.78739776, 0.78739776, 0.78739776, 0.78739776, 0.78739776,\n",
       "        0.78739776, 0.78739776, 0.78938963, 0.78938963, 0.78938963,\n",
       "        0.78938963, 0.78938963, 0.78938963, 0.78924718, 0.78924718,\n",
       "        0.78924718, 0.7916668 , 0.79152455, 0.7919513 , 0.79237844,\n",
       "        0.79180945, 0.79237844, 0.79323132, 0.79308928, 0.79308928,\n",
       "        0.78540993, 0.78597912, 0.78555238, 0.78654832, 0.78668975,\n",
       "        0.78697486, 0.78782794, 0.78811263, 0.78768569, 0.77460195,\n",
       "        0.77517114, 0.77630872, 0.77701996, 0.7774467 , 0.77673586,\n",
       "        0.77815834, 0.77787405, 0.77801629, 0.76777932, 0.76877465,\n",
       "        0.76905915, 0.77204513, 0.77076591, 0.77176064, 0.77218778,\n",
       "        0.77190288, 0.77161879]),\n",
       " {'criterion': 'gini',\n",
       "  'max_depth': 6,\n",
       "  'min_samples_leaf': 4,\n",
       "  'min_samples_split': 2},\n",
       " 0.7932313219319798)"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "col = list(churn1.columns)\n",
    "col.remove('Churn')\n",
    "x = churn1[col]\n",
    "y = churn1['Churn']\n",
    "tree_param_grid = { 'max_depth':range(1,10)\n",
    "                   ,'criterion':np.array(['entropy','gini'])\n",
    "                   ,'min_samples_split': list((2,4,6))\n",
    "                   ,'min_samples_leaf':list((1,2,4))}\n",
    "cross_validation = StratifiedKFold(n_splits=10).split(x,y)\n",
    "grid = GridSearchCV(DecisionTreeClassifier(),param_grid=tree_param_grid, cv=cross_validation)\n",
    "grid.fit(x, y)\n",
    "grid.cv_results_['mean_test_score'], grid.best_params_, grid.best_score_"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.model_selection import train_test_split\n",
    "X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DecisionTreeClassifier(max_depth=6, min_samples_leaf=4)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "clf = DecisionTreeClassifier(max_depth = ,criterion='gini'\n",
    "                            , min_samples_leaf =4\n",
    "                            , min_samples_split =2)\n",
    "clf.fit(X_train, y_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 模型评估"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(array([0.        , 0.08275862, 1.        ]),\n",
       " array([0.        , 0.46578366, 1.        ]),\n",
       " array([2, 1, 0], dtype=int64))"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#AUC曲线\n",
    "# 计算各阈值下假阳性率、真阳性率和AUC\n",
    "from sklearn.metrics import roc_curve, auc\n",
    "from sklearn.metrics import mean_absolute_error, accuracy_score, roc_curve, plot_confusion_matrix\n",
    "fpr,tpr,threshold = roc_curve(y_test,clf.predict(X_test))\n",
    "fpr,tpr,threshold "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.691512521884753"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "roc_auc = auc(fpr,tpr)\n",
    "roc_auc"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.19"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": false,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contents",
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": true,
   "toc_window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
