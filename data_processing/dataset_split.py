import pandas as pd
from sklearn.model_selection import train_test_split

# 读取CSV文件
file_dir = '../DataSet/io/Bing2020/'
data = pd.read_csv(file_dir + "bing.csv")

# 假设第一行是列名，第一列是label
# 如果第一行不是列名，可以使用以下代码添加列名
# data.columns = ['label', 'in_pkt', 'in_size', 'out_pkt', 'out_size']

# 划分训练集和测试集，比例为8:2
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# 保存到新的CSV文件
train_data.to_csv(file_dir + 'bing_train.csv', index=False)
test_data.to_csv(file_dir + 'bing_test.csv', index=False)

print("训练集和测试集已成功保存到 train.csv 和 test.csv 文件中。")