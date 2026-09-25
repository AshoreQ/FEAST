from tensorflow.python import keras

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef
import datetime
import os
import sys
from get_labels import get_labels,get_labels_2



DATA_FILE = "D:/Postgraduate/WebSCentinel/dataset/cnn/polling/eBay/"
RESULT_FILE = "D:/Postgraduate/WebSCentinel/result/polling/eBay/"
obj = "eBay"
# DATA_FILE = "../DataSet/chunk/data"
# RESULT_FILE = "../Result/chunk/"
FILE_NO_START = 1
FILE_NO_END = 1

IDX_MIN = 1
IDX_MAX = 10

# 如果没有这个文件，那么先创建一个文件
if not os.path.exists(RESULT_FILE):
    os.mkdir(RESULT_FILE)


acc_list = []
p_list = []
r_list = []
f1_list = []
mcc_list = []

for IDX in range(IDX_MIN, IDX_MAX + 1):
    train_data_file = DATA_FILE + obj + "_train.csv"
    test_data_file = DATA_FILE + obj + "_test.csv"
    # label_num = 100
    # label_num = IDX * 10

    train_data = pd.read_csv(train_data_file)
    test_data = pd.read_csv(test_data_file)
    # test_data['append'] = 0

    # 取数据集标签
    # keywords = get_labels(IDX)
    # keywords = get_labels_2(IDX)
    # train_data = train_data.loc[train_data['label'].isin(keywords)]
    # test_data = test_data.loc[test_data['label'].isin(keywords)]
    # 取数据集标签
    keywords = ['switch', 'laptop', 'airpods', 'headphones', 'earbuds', 'ipad', 'ssd', 'fitbit', 'game_of_thrones',
                  'fire_stick', 'toilet_paper', 'external_hard_drive', 'instant_pot', 'tablet', 'micro_sd_card', 'kindle',
                  'tv', 'air_fryer', 'bluetooth', 'roku']
    # keywords = ["youtube", "weather", "amazon", "facebook", "google", "wordle",
    #              "gmail", "walmart", "google_translate", "nfl"]
    # keywords = ['PlayStation_4', 'North_Korea', 'Samsung_Galaxy_4', 'Royal_Baby', 'Boston_Marathon', 'Harlem_Shake',
    #             'Cory_Monteith iPhone_5S', 'Paul_Walker', 'Nelson_Mandela']
    # keywords = ['Wordle', 'India_vs_England', 'Ukraine', 'Queen_Elizabeth', 'Ind_vs_SA', 'World_Cup', 'India_vs_West_Indies', 'iPhone14' 'Jeffrey_Dahmer', 'Indian_Premier_League']
    # train_data = train_data.loc[train_data['label'].isin(keywords)]
    # test_data = test_data.loc[test_data['label'].isin(keywords)]
    #
    # train_X = train_data.iloc[:, 1:].values
    # train_y = train_data.loc[:, "label"].values
    # test_X = test_data.iloc[:, 1:].values
    # test_y = test_data.loc[:, "label"].values
    #
    # # 标准化处理
    # scale = StandardScaler()
    # train_X = scale.fit_transform(train_X)
    # test_X = scale.fit_transform(test_X)
    #
    # train_X = train_X.reshape(train_X.shape[0], train_X.shape[1], 1)
    # test_X = test_X.reshape(test_X.shape[0], test_X.shape[1], 1)
    # categorical_train = pd.Categorical(train_y)
    # categorical_test = pd.Categorical(test_y)
    # train_y = categorical_train.codes
    # test_y = categorical_test.codes
        # print(train_X.shape[1])
    train_data = train_data.loc[train_data['label'].isin(keywords)]
    test_data = test_data.loc[test_data['label'].isin(keywords)]
    # 1. 先提取特征 X 和标签 y（确保这行没有被删除！）
    train_X = train_data.iloc[:, 1:].values
    train_y_raw = train_data.loc[:, "label"].values
    test_X = test_data.iloc[:, 1:].values
    test_y_raw = test_data.loc[:, "label"].values

    # 2. 标准化 X（注意：测试集要用训练集的 scaler）
    from sklearn.preprocessing import StandardScaler

    scale = StandardScaler()
    train_X = scale.fit_transform(train_X)
    test_X = scale.transform(test_X)  # 注意：这里是 transform，不是 fit_transform！


    # 3. 编码 y（使用 LabelEncoder 确保一致性）
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    train_y = le.fit_transform(train_y_raw)
    test_y = le.transform(test_y_raw)

    # 检查信息（调试用）
    # print(f"Label classes: {le.classes_}")
    # print(f"Number of classes: {len(le.classes_)}")
    # label_num = len(le.classes_)

    # 4. Reshape X 以适应 CNN
    label_num = len(le.classes_)
    train_X = train_X.reshape(train_X.shape[0], train_X.shape[1], 1)
    test_X = test_X.reshape(test_X.shape[0], test_X.shape[1], 1)

    # 5. 检查形状
    # print(f"train_X shape: {train_X.shape}, train_y shape: {train_y.shape}")
    # print(f"test_X shape: {test_X.shape}, test_y shape: {test_y.shape}")

    # 后面的 reshape 和模型构建代码保持不变...
    train_X = train_X.reshape(train_X.shape[0], train_X.shape[1], 1)
    test_X = test_X.reshape(test_X.shape[0], test_X.shape[1], 1)
    # test_X = test_X.reshape(train_X.shape[0], train_X.shape[1], 1)
    categorical_train = pd.Categorical(train_y)
    categorical_test = pd.Categorical(test_y)
    train_y = categorical_train.codes
    test_y = categorical_test.codes

    # clf_cnn = keras.models.Sequential([
    #     keras.layers.Conv1D(filters=64, kernel_size=7, activation='relu', padding='same', input_shape=(train_X.shape[1],1)),
    #     keras.layers.MaxPool1D(2),
    #     keras.layers.Conv1D(filters=128, kernel_size=3, activation='relu', padding='same'),
    #     keras.layers.Conv1D(filters=128, kernel_size=3, activation='relu', padding='same'),
    #     keras.layers.MaxPool1D(2),
    #     keras.layers.Conv1D(filters=256, kernel_size=3, activation='relu', padding='same'),
    #     keras.layers.Conv1D(filters=256, kernel_size=3, activation='relu', padding='same'),
    #     keras.layers.MaxPool1D(2),
    #     keras.layers.Flatten(),
    #     keras.layers.Dense(128, activation='relu'),
    #     keras.layers.Dropout(0.5),
    #     keras.layers.Dense(64, activation='relu'),
    #     keras.layers.Dropout(0.5),
    #     keras.layers.Dense(label_num, activation='softmax')
    # ])

    if test_X.shape[1] < train_X.shape[1]:
        test_X = np.pad(test_X, ((0, 0), (0, train_X.shape[1] - test_X.shape[1]), (0, 0)), mode='constant')
    elif test_X.shape[1] > train_X.shape[1]:
        test_X = test_X[:, :train_X.shape[1], :]

    clf_lstm = keras.models.Sequential([
        keras.layers.LSTMV1(units=128, return_sequences=True, input_shape=(train_X.shape[1], 1)),
        keras.layers.LSTMV1(units=128, return_sequences=False),
        # keras.layers.Dropout(0.5),
        keras.layers.Dense(label_num, activation='softmax')
    ])


    checkpoint_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    # clf_lstm.summary()
    clf_lstm.compile(optimizer='nadam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    clf_lstm.fit(train_X, train_y, epochs=200, validation_data=(test_X, test_y),verbose=0,callbacks=[checkpoint_cb])

    # acc = clf_lstm.evaluate(test_X, test_y)
    y_pre = clf_lstm.predict(test_X)
    y_pre = np.argmax(y_pre, axis=1)

    acc_list.append(accuracy_score(test_y, y_pre))
    p_list.append(precision_score(test_y, y_pre, average='weighted'))
    r_list.append(recall_score(test_y, y_pre, average="weighted"))
    f1_list.append(f1_score(test_y, y_pre, average="weighted"))
    mcc_list.append(matthews_corrcoef(test_y, y_pre))
    print(acc_list, p_list, r_list, f1_list, mcc_list)

row1 = {
    'acc': np.mean(acc_list),
    'p': np.mean(p_list),
    'r': np.mean(r_list),
    'f1': np.mean(f1_list),
    'mc': np.mean(mcc_list),
}

row_df = pd.DataFrame(row1, index=[0])
row_df.to_csv(RESULT_FILE + obj + "_lstm_mean.csv", index=False)

row2 = {
    'acc': np.std(acc_list),
    'p': np.std(p_list),
    'r': np.std(r_list),
    'f1': np.std(f1_list),
    'mc': np.std(mcc_list),
}

row_df = pd.DataFrame(row2, index=[0])
row_df.to_csv(RESULT_FILE + obj + "_lstm_std.csv", index=False)