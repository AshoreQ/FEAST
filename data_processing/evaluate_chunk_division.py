import pandas as pd


DATA_FILE = "../DataSet/chunk/data"
RESULT_FILE = "../Result/chunk/"
FILE_NO_START = 3
FILE_NO_END = 3
N = 3

for i in range(FILE_NO_START, FILE_NO_END + 1):
    # data_file = DATA_FILE + str(i) + ".csv"
    data_file = "../DataSet/chunk/data3_3.csv"
    data = pd.read_csv(data_file)
    for j in range(0, N):
        count = 0
        for index, row in data.iterrows():
            l = len(row['label'])
            cor_list = []
            for c in range(0, j + 1):
                cor_list.append(l + c)
                cor_list.append(l - c)
            if row['chunk_count'] in cor_list:
                count += 1
        print("正确长度偏差：",j)
        print(count / data.shape[0])

'''
100 baidu
正确长度偏差： 0
0.9337071900660925
正确长度偏差： 1
0.9968956539154816
正确长度偏差： 2
0.9977969156819547

100 bing
正确长度偏差： 0
0.3655761024182077
正确长度偏差： 1
0.7822597033123349
正确长度偏差： 2
0.8811217232269863
'''


