import datetime
import time
import os
import sys

import torch
from keras.src.trainers.data_adapters.data_adapter_utils import class_weight_to_sample_weights
from sklearn import ensemble, neighbors, svm, tree, linear_model, naive_bayes
from sklearn.impute import SimpleImputer
from sympy import false
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import StackingClassifier
from pytorch_tabnet.tab_model import TabNetClassifier
from lightgbm import LGBMClassifier
import pandas as pd
import numpy as np
from get_labels import get_labels_2, get_labels

DATA_FILE = "../../dataset/combinations/Bing/"
RESULT_FILE = "../../result/Bing/"
obj = "bing"
is_ks = False


IDX_MIN = 1
IDX_MAX = 1

# 如果没有这个文件，那么先创建一个文件
if not os.path.exists(RESULT_FILE):
    os.mkdir(RESULT_FILE)

for model_select in ["rf", "xgb", "knn", "dt", "svm", "lr", "nb", "lgb"]:
    for IDX in range(IDX_MIN, IDX_MAX + 1):
        if is_ks:
            data_file = DATA_FILE + obj + "_ks_length.csv"
        else:
            data_file = DATA_FILE + "size_fit.csv"
            # data_file = r"D:\Postgraduate\WebSCentinel\dataset\polling\eBay\polling.csv"
            #data_file = DATA_FILE + "taobao.csv"
        # di = RESULT_FILE + str(IDX + 2022)
        postfix = "size"
        di = RESULT_FILE + postfix
        if not os.path.exists(di):
            os.mkdir(di)
        if is_ks:
            result_file = (RESULT_FILE + str(IDX + 2022) + "/" + obj + "_" + model_select + "_ks_length" + ".txt")
        else:
            # result_file = RESULT_FILE + str(IDX + 2022) + "/" + "size/" + obj + "_" + model_select +"_polling.txt"
            result_file = RESULT_FILE + postfix + "/" + obj + "_" + model_select + "_size" + ".txt"
            # result_file = "D:/Postgraduate/WebSCentinel/result/polling/eBay/" + "polling_" + model_select + ".txt"
        # 输出重定向
        sys.stdout = open(result_file, mode="w", encoding="utf-8")

        data = pd.read_csv(data_file)

        # 取数据集标签
        # keywords = get_labels_2(IDX)
        # keywords = ['switch', 'laptop', 'airpods', 'headphones', 'earbuds', 'ipad', 'ssd', 'fitbit', 'game_of_thrones',
        #         'fire_stick', 'toilet_paper', 'external_hard_drive', 'instant_pot', 'tablet', 'micro_sd_card', 'kindle', 'tv',
        #         'air_fryer', 'bluetooth', 'roku']
        # # 2023:
        # keywords = ["youtube", "weather", "amazon", "facebook", "google", "wordle",
        #                "gmail", "walmart", "google_translate", "nfl"]
        keywords = ['Wordle', 'India_vs_England', 'Ukraine', 'Queen_Elizabeth', 'Ind_vs_SA', 'World_Cup',
                    'India_vs_West_Indies', 'iPhone14' 'Jeffrey_Dahmer', 'Indian_Premier_League']
        data = data.loc[data['label'].isin(keywords)]

        X = data.iloc[:, 1:].values
        y = data.loc[:, "label"].values

        # 标签编码
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        # 动态调整 n_splits
        unique_classes, class_counts = np.unique(y_encoded, return_counts=True)
        min_class_count = min(class_counts)
        if min_class_count < 2:
            print(f"[警告] 类别 {label_encoder.inverse_transform([unique_classes[np.argmin(class_counts)]])[0]} 只有 {min_class_count} 个样本，无法做交叉验证。")
            print("跳过当前实验。")
            continue
        n_splits = min(5, min_class_count)  # 确保 n_splits 不大于最小类别样本数量
        print(f"动态调整后的 n_splits: {n_splits}")

        folds = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

        if model_select == 'rf':
            model = ensemble.RandomForestClassifier(random_state=42, max_features=100)
        elif model_select == 'xgb':
            model = XGBClassifier(verbosity=0)
        elif model_select == 'knn':
            model = neighbors.KNeighborsClassifier(n_neighbors=1)
        elif model_select == 'svm':
            model = svm.SVC(kernel="rbf", C=5000)
        elif model_select == 'dt':
            model = tree.DecisionTreeClassifier(random_state=42)
        elif model_select == 'lr':
            model = linear_model.LogisticRegression(max_iter=3000, C=200)
        elif model_select == 'nb':
            model = naive_bayes.GaussianNB()
        elif model_select == 'stacking':
            estimators = [
                ('knn', neighbors.KNeighborsClassifier(n_neighbors=1)),
                ('dt', tree.DecisionTreeClassifier(random_state=42)),
                ('svr', make_pipeline(StandardScaler(), svm.SVC(kernel="rbf", random_state=42, gamma=0.1, C=5000)))
            ]
            model = StackingClassifier(
                estimators=estimators,
                final_estimator=make_pipeline(StandardScaler(), linear_model.LogisticRegression(max_iter=3000, C=500, random_state=42))
            )
        elif model_select == 'et':
            model = ensemble.ExtraTreesClassifier(random_state=42, max_features=100)
        elif model_select == 'tabnet':
            model = TabNetClassifier(
                n_d=32,  # 决策步长维度
                n_a=32,  # 注意力维度
                n_steps=3,  # 决策步数（通常 3~5）
                gamma=1.3,  # 特征重用惩罚
                optimizer_params=dict(lr=2e-2),
                scheduler_params={"step_size": 10, "gamma": 0.9},
                scheduler_fn=torch.optim.lr_scheduler.StepLR,
                verbose=1,
                seed=42            )
        elif model_select == 'lgb':
            model = LGBMClassifier(
                n_estimators=100,
                learning_rate=0.05,
                max_depth=6,
                random_state=42,
                verbose=-1  # 静默训练日志（避免污染 stdout）
            )

        # 保存测试结果
        acc_list = []
        p_list = []
        r_list = []
        f1_list = []
        mcc_list = []

        # start = datetime.datetime.now()
        start = time.perf_counter_ns()

        for train_index, test_index in folds.split(X, y_encoded):
            train_X, test_X = X[train_index], X[test_index]
            train_y, test_y = y_encoded[train_index], y_encoded[test_index]
            model.fit(train_X, train_y)
            y_pre = model.predict(test_X)

            acc_list.append(accuracy_score(test_y, y_pre))
            p_list.append(precision_score(test_y, y_pre, average='weighted', zero_division=1))
            r_list.append(recall_score(test_y, y_pre, average='weighted', zero_division=1))
            f1_list.append(f1_score(test_y, y_pre, average='weighted', zero_division=1))
            mcc_list.append(matthews_corrcoef(test_y, y_pre))

        # end = datetime.datetime.now()
        end = time.perf_counter_ns()
        elapsed_ms = (end - start) / 1_000_000  # 纳秒转毫秒
        print("Acc:", acc_list)
        print("P:", p_list)
        print("R:", r_list)
        print("F1", f1_list)
        print("MCC", mcc_list)
        print(f"Acc:{np.mean(acc_list)},P:{np.mean(p_list)},R:{np.mean(r_list)},F1:{np.mean(f1_list)},MCC:{np.mean(mcc_list)}")
        print(f"{model_select} 模型所用时间: {elapsed_ms:.2f} ms")