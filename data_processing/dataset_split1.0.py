import pandas as pd
from sklearn.model_selection import train_test_split

# 读取CSV文件
file_dir = '../DataSet/combination/final/bing/12/'
data = pd.read_csv(file_dir + "bing.csv")

# 按label分组，对每个label单独划分训练集和测试集
train_data_list = []
test_data_list = []

for label, group in data.groupby('label'):
    train_group, test_group = train_test_split(group, test_size=0.2, random_state=42)
    train_data_list.append(train_group)
    test_data_list.append(test_group)

# 合并所有训练集和测试集
train_data = pd.concat(train_data_list)
test_data = pd.concat(test_data_list)

# 保存到新的CSV文件
train_data.to_csv(file_dir + 'baidu_train.csv', index=False)
test_data.to_csv(file_dir + 'baidu_test.csv', index=False)

print("训练集和测试集已成功保存到 train.csv 和 test.csv 文件中。")