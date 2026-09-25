import os
from get_ip import getIp
from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap
import pandas
import csv
import pandas as pd
import datetime


def get_features(DATA_FILE, n):
    data = []
    # 得到这个文件夹里的所有文件名
    for pcap_file in os.listdir(DATA_FILE):
        in_size = 0
        out_size = 0
        in_packet = 0
        out_packet = 0
        x = 0  # 数据包个数
        y = 0  # 数据包大小的累积
        graph = []  # 根据每个(x,y)点绘图
        features = []
        print("处理：", pcap_file)
        # 获取数据包的源目的ip
        pcap_file = DATA_FILE + "/" + pcap_file
        ips = getIp(pcap_file)
        remote_ip = ips[0]  # 搜索引擎的ip，就是数据包的源ip
        local_ip = ips[1]  # 本机的ip，就是数据包的目的ip
        if ips[1] == 0:
            continue
        packet_list = rdpcap(pcap_file)
        for pkt in packet_list:
            # 只要ip数据包
            if not pkt.haslayer(IP):
                continue
            ip_pkt = pkt.getlayer(IP)
            x += 1
            if not ip_pkt.haslayer(TCP):
                continue
            if ip_pkt.src in remote_ip:
                in_packet += 1
                in_size += len(ip_pkt.payload)
                y += len(ip_pkt.payload)
            if ip_pkt.src in local_ip:
                out_packet += 1
                out_size += len(ip_pkt.payload)
                y -= len(ip_pkt.payload)
            graph.append([x, y])
        if graph == []:
            continue
        features.append(in_packet)
        features.append(in_size)
        features.append(out_packet)
        features.append(out_size)

        # 绘图 CUMUL 曲线
        max_x = graph[-1][0]  # 最大的x
        gap = float(max_x) / (n + 1)  # 取值间隔
        graph_ptr = 0  # x点的指针
        for i in range(0, n):
            sample_x = gap * (i + 1)
            while(graph[graph_ptr][0] < sample_x):
                graph_ptr += 1
                # 最后超出范围的判断
                if(graph_ptr >= len(graph) - 1):
                    break
            next_x = graph[graph_ptr][0]
            next_y = graph[graph_ptr][1]
            last_x = graph[graph_ptr - 1][0]
            last_y = graph[graph_ptr - 1][1]

            # 计算y点
            slope = (next_y - last_y) / float(next_x - last_x)
            sample_y = slope * (sample_x - last_x) + last_y
            features.append(sample_y)
        features.insert(0, pcap_file[pcap_file.index('_') + 1:pcap_file.index('_trial')])
        data.append(features)

    return data

# 不手工分测试集合训练集
# DATA_FILE = "../Pcap/data2"
# CSV_FILE = "../DataSet/cumul60/dataset2.csv"
DATA_FILE = "../Pcap_processed/Bing/2020"
CSV_FILE = "../DataSet/cumul/Bing2020/bing.csv"
file_csv = open(CSV_FILE, 'w', newline='', encoding='utf-8')
n = 60

df = pandas.DataFrame()

# train_data = getData(TRAIN_DATA_FILE)
# test_data = getData(TEST_DATA_FILE)

start = datetime.datetime.now()
data = get_features(DATA_FILE, n)
end = datetime.datetime.now()
print("CUMUL所用时间", (end - start).seconds)

csv_write = csv.writer(file_csv, dialect='excel')
for line in data:
    csv_write.writerow(line)
file_csv.close()

# 定义列名


df = pd.read_csv(CSV_FILE, header=None)
col_name = df.columns.tolist()
col_name[1] = "in_pkt"
col_name[2] = "in_size"
col_name[3] = "out_pkt"
col_name[4] = "out_size"
for i in range(5, len(col_name) - 1):
    col_name[i] = "cumul_" + str(i)
col_name[0] = "label"
df.columns = col_name
df.to_csv(CSV_FILE, mode="w", index=None)
