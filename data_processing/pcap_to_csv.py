from pcap_miner import getData
import pandas
import csv
import pandas as pd
import datetime


# TRAIN_DATA_FILE = "../Data/Data60/TrainData1"
# TEST_DATA_FILE = "../Data/Data60/TestData1"
# TRAIN_CSV_FILE = "../DataSet/Data60/TrainData1.csv"
# TEST_CSV_FILE = "../DataSet/Data60/TestData1.csv"
# train_csv = open(TRAIN_CSV_FILE, 'w', newline='')
# test_csv = open(TEST_CSV_FILE, 'w', newline='')

# 不手工分测试集合训练集
DATA_FILE = "../Pcap/data3"
CSV_FILE = "../DataSet/chunk/data3_3.csv"
file_csv = open(CSV_FILE, 'w', newline='')

df = pandas.DataFrame()
max_len = 0

# train_data = getData(TRAIN_DATA_FILE)
# test_data = getData(TEST_DATA_FILE)

start = datetime.datetime.now()
data = getData(DATA_FILE)
end = datetime.datetime.now()
print("2011所用时间", (end - start).seconds)

# 找出最长的行
# for line in train_data:
#     if len(line) > max_len:
#         max_len = len(line)
# for line in test_data:
#     if len(line) > max_len:
#         max_len = len(line)

for line in data:
    if len(line) > max_len:
        max_len = len(line)

# 把每一条数据都变成一样长，写入csv文件
# csv_write = csv.writer(train_csv, dialect='excel')
# for line in train_data:
#     line_max = [0] * max_len
#     for i in range(len(line)):
#         line_max[i] = line[i]
#     # 把数据写入csv文件
#     csv_write.writerow(line_max)
# train_csv.close()
#
# csv_write = csv.writer(test_csv, dialect='excel')
# for line in test_data:
#     line_max = [0] * max_len
#     for i in range(len(line)):
#         line_max[i] = line[i]
#     # 把数据写入csv文件
#     csv_write.writerow(line_max)
# test_csv.close()

csv_write = csv.writer(file_csv, dialect='excel')
for line in data:
    line_max = [0] * max_len
    for i in range(len(line)):
        line_max[i] = line[i]
    # 把数据写入csv文件
    csv_write.writerow(line_max)
file_csv.close()

# 定义列名

# df = pd.read_csv(TRAIN_CSV_FILE, header=None)
# col_name = df.columns.tolist()
# col_name[0] = "label"
# col_name[1] = "pkg_count"
# col_name[2] = "chunk_count"
# col_name[3] = "total_size"
# for i in range(4, len(col_name)):
#     col_name[i] = "chunk_" + str(i)
# df.columns = col_name
# df.to_csv(TRAIN_CSV_FILE, mode="w", index=None)
#
# df = pd.read_csv(TEST_CSV_FILE, header=None)
# col_name = df.columns.tolist()
# col_name[0] = "label"
# col_name[1] = "pkg_count"
# col_name[2] = "chunk_count"
# col_name[3] = "total_size"
# for i in range(4, len(col_name)):
#     col_name[i] = "chunk_" + str(i)
# df.columns = col_name
# df.to_csv(TEST_CSV_FILE, mode="w", index=None)

df = pd.read_csv(CSV_FILE, header=None)
col_name = df.columns.tolist()
col_name[0] = "label"
col_name[1] = "pkg_count"
col_name[2] = "chunk_count"
col_name[3] = "total_size"
for i in range(4, len(col_name)):
    col_name[i] = "chunk_" + str(i)
df.columns = col_name
df.to_csv(CSV_FILE, mode="w", index=None)