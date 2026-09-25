import os


from get_ip import getIp
from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap
import pandas as pd
import numpy as np
import datetime
import csv

from temporal_feature import get_temporal_feature
from util import load_pcap
from detection import detect_website_keystrokes, detect_keystrokes

def extract_keystroke_features(pcap_file):
    website, _, keystrokes = get_temporal_feature(pcap_file)
    if keystrokes.empty:
        return [0] * 3  # 返回空特征

    times = keystrokes['frame_time'].values
    lengths = keystrokes['frame_length'].values

    intervals = np.diff(times)
    return [
        np.mean(intervals) if len(intervals) > 0 else 0,
        np.std(intervals) if len(intervals) > 0 else 0,
        np.mean(lengths),
        np.std(lengths),
        len(keystrokes),
        times[-1] - times[0] if len(times) > 1 else 0,
        # sum(1 for i in intervals if i < 200) if len(intervals) > 0 else 0
    ]

MIN_GAP_TIME = 0.5
# bing
# MIN_GAP_TIME = 0.7
# MIN_GAP_TIME = 0.25

data = []
def getData(DATA_FILE):
    # 得到这个文件夹里的所有文件名
    for pcap_file in os.listdir(DATA_FILE):
        print("处理：", pcap_file)
        # 文件名格式 search_aaron_hernandez_trial_3.pcap 得到第一个“_”和"_trial"之间的 其实就是搜索词，就是标签名
        label = pcap_file[pcap_file.index('_') + 1:pcap_file.index('_trial')]
        # 获取数据包的源目的ip
        pcap_file = DATA_FILE + "/" + pcap_file
        ips = getIp(pcap_file)
        remote_ip = ips[0]  # 搜索引擎的ip，就是数据包的源ip
        # local_ip = ips[1]
        # Baid ip 特殊处理
        # remote_ip = ['110.242.69.21', '110.242.70.57', '220.181.111.1', '39.156.70.239', '39.156.70.46', '106.117.216.33',
        #               '220.181.111.232', "39.156.66.18", "39.156.66.14","110.242.68.4","110.242.68.3","111.63.60.33","220.181.38.149","220.181.38.150"]
        # ips = getIp(pcap_file)
        # remote_ip = ips[0]
        # Google: remote_ip = ["172.217.2.163"]
        # Bing ip 特殊处理
        remote_ip = ['202.89.233.101', '13.107.21.200', '202.89.233.100', '106.117.216.33']
        local_ip = ['192.168.247.139', '192.168.125.100', '192.168.25.129', '192.168.88.128',
                    '192.168.139.131', '192.168.101.129', '172.20.0.2', '192.168.238.129',
                    '192.168.248.129', '192.168.200.138', '192.168.125.100', '192.168.195.128',
                    "172.21.0.2", "172.19.0.2", "172.18.0.2", "172.20.0.2", "172.22.0.2",
                    "172.23.0.2", "172.25.0.2", "172.27.0.2", "172.30.0.2", "172.26.0.2",
                    "192.168.0.2", "192.168.112.2", "192.168.96.2", "192.168.32.2",
                    "192.168.139.129", "192.168.0.105", "192.168.0.101", "192.168.0.102",
                    "192.168.0.108", "192.168.0.104"]  # 本机的ip，就是数据包的目的ip
        # 存储根据ip地址和数据包大小过滤之后的tcp包序列
        pkg_list = []
        # 标识是否无第一块，bing的第一块需要特殊处理
        is_first_pkt = True
        # 处理pcap文件，
        packet_list = rdpcap(pcap_file)
        for pkt in packet_list:
            # 只要ip数据包
            if not pkt.haslayer(IP):
                continue
            ip_pkt = pkt.getlayer(IP)
            # 只要tcp数据包
            if ip_pkt.haslayer(TCP):
                tcp_pkt = ip_pkt.getlayer(TCP)
                # pkg_list.append(pkt)
                # 噪音过滤策略过滤
                # 不是bing

                if '202.89.233.101' not in remote_ip or '202.89.233.100' not in remote_ip or '13.107.21.200' not in remote_ip\
                        or '106.117.216.33' not in remote_ip:
                    if (ip_pkt.src in remote_ip or remote_ip is None) and ip_pkt.dst in local_ip and len(
                            tcp_pkt.payload) != 0 and len(tcp_pkt.payload) <= 1024:
                        pkg_list.append(pkt)
                # 是bing的话单独处理
                else:
                    if is_first_pkt:  # 第一块无关的包统一加进去
                        if (ip_pkt.src in remote_ip or remote_ip is None) and ip_pkt.dst in local_ip and len(
                                tcp_pkt.payload) != 0:
                            is_first_pkt = False
                            pkg_list.append(pkt)
                    else:
                        if (ip_pkt.src in remote_ip or remote_ip is None) and ip_pkt.dst in local_ip and len(
                                tcp_pkt.payload) != 0 and len(tcp_pkt.payload) <= 1024:
                            pkg_list.append(pkt)
        if not pkg_list:
            print(pcap_file, ':isEmpty or ip not update')
            continue
        else:
            pkg_list = [pkg_list[0]] + pkg_list  # 这一步操作是为了分块的时候不用特别判断第一块



        #################################
        in_size = 0
        out_size = 1
        in_packet = 0
        out_packet = 0
        x = 0  # 数据包个数
        y = 0  # 数据包大小的累积
        graph = []  # 根据每个(x,y)点绘图
        features = []
        # print("处理：", pcap_file)
        # # 获取数据包的源目的ip
        # pcap_file = DATA_FILE + "/" + pcap_file
        # ips = getIp(pcap_file)
        # remote_ip = ips[0]  # 搜索引擎的ip，就是数据包的源ip
        # local_ip = ips[1]  # 本机的ip，就是数据包的目的ip

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
        gap = float(max_x) / (30 + 1)  # 取值间隔
        graph_ptr = 0  # x点的指针
        for i in range(0, 30):
            sample_x = gap * (i + 1)
            while (graph[graph_ptr][0] < sample_x):
                graph_ptr += 1
                # 最后超出范围的判断
                if (graph_ptr >= len(graph) - 1):
                    break
            next_x = graph[graph_ptr][0]
            next_y = graph[graph_ptr][1]
            last_x = graph[graph_ptr - 1][0]
            last_y = graph[graph_ptr - 1][1]

            # 计算y点
            slope = (next_y - last_y) / float(next_x - last_x)
            sample_y = slope * (sample_x - last_x) + last_y
            features.append(sample_y)
        features.insert(0, label)
        # ks_features = extract_keystroke_features(pcap_file)
        # features += ks_features

        #################################

        # 分块，根据时间间隔和数据包大小
        line = [0, 0, 0]  # 第一个位置是所有有效数据包的总数量，第二个位置是分块总数量，第三个位置是所有有效数据包的有效载荷总大小
        chunk_size = 0  # 块大小
        if '202.89.233.101' not in remote_ip or '202.89.233.100' not in remote_ip:
            for pkt_index in range(1, len(pkg_list)):
                cur = pkg_list[pkt_index]
                pre = pkg_list[pkt_index - 1]
                cur_ip_pkt = cur.getlayer(IP)
                cur_tcp_pkt = cur_ip_pkt.getlayer(TCP)
                line[0] += 1
                line[2] += len(cur_tcp_pkt.payload)
                # 根据时间间隔分块
                if abs(cur.time - pre.time) <= MIN_GAP_TIME:
                    chunk_size = chunk_size + len(cur_tcp_pkt.payload)
                else:
                    # 根据数据包大小分块
                    if chunk_size > 50:
                        line.append(chunk_size)
                        # print(chunk_size)
                        line[1] += 1
                        chunk_size = len(cur_tcp_pkt.payload)
                # 只剩最后一个包了，特殊处理
                if pkt_index == len(pkg_list) - 1:
                    if chunk_size > 50:
                        line.append(chunk_size)
                        # print(chunk_size)
                        line[1] += 1
            # 按行存入dataframe
            # line.append(label)
            # print(line)
            data.append(features + line)
            # df.loc[len(df.index)] = line
        # bing 特殊处理
        else:
            for pkt_index in range(1, len(pkg_list)):
                cur = pkg_list[pkt_index]
                pre = pkg_list[pkt_index - 1]
                cur_ip_pkt = cur.getlayer(IP)
                cur_tcp_pkt = cur_ip_pkt.getlayer(TCP)
                line[0] += 1
                line[2] += len(cur_tcp_pkt)
                # 根据时间间隔分块
                if abs(cur.time - pre.time) <= MIN_GAP_TIME:
                    chunk_size = chunk_size + len(cur_tcp_pkt.payload)
                else:
                    line.append(chunk_size)
                    # print(chunk_size)
                    line[1] += 1
                    chunk_size = len(cur_tcp_pkt.payload)
                if pkt_index == len(pkg_list) - 1:
                    line.append((chunk_size))
                    # print(chunk_size)
                    line[1] += 1
            l = pcap_file.index('_trial') - pcap_file.index('search_') - 7
            if len(line) - 3 > l:
                del line[3]  # 删除掉无关的第一块
            # 按行存入dataframe
            # line.append(label)
            # print(line)
            data.append(features + line)
            # print(features + line)
            # df.loc[len(df.index)] = line


DATA_FILE = r"D:\Postgraduate\WebSCentinel\data\fit\bing\2022"
CSV_FILE = "../dataset/combinations/bing/size_fit.csv"
file_csv = open(CSV_FILE, 'w', newline='', encoding='utf-8')

df = pd.DataFrame()
max_len = 0

# train_data = getData(TRAIN_DATA_FILE)
# test_data = getData(TEST_DATA_FILE)

start = datetime.datetime.now()
getData(DATA_FILE)
print(data)
end = datetime.datetime.now()
print("所用时间", (end - start).seconds)

# 找出最长的行

for line in data:
    if len(line) > max_len:
        max_len = len(line)

# 把每一条数据都变成一样长，写入csv文件

csv_write = csv.writer(file_csv, dialect='excel')
for line in data:
    line_max = [0] * max_len
    for i in range(len(line)):
        line_max[i] = line[i]
    # 把数据写入csv文件
    csv_write.writerow(line_max)
file_csv.close()

# 定义列名

df = pd.read_csv(CSV_FILE, header=None)
col_name = df.columns.tolist()
col_name[0] = "label"
col_name[1] = "in_pkt"
col_name[2] = "in_size"
col_name[3] = "out_pkt"
col_name[4] = "out_size"

for i in range(5, 35):
    col_name[i] = "cumul_" + str(i - 4)
# col_name[35] = "pkg_count"
# col_name[36] = "chunk_count"
# col_name[37] = "total_size"

# col_name[35] = "ks_interval_mean"
# col_name[36] = "ks_interval_std"
# col_name[35] = "ks_length_mean"
# col_name[36] = "ks_length_std"
# col_name[37] = "ks_count"
# col_name[40] = "ks_duration"
# col_name[38] = "ks_burst_count"

for i in range(35, len(col_name)):
    col_name[i] = "chunk_" + str(i - 35)



df.columns = col_name
df.to_csv(CSV_FILE, mode="w", index=None)

print(df.shape[0])
print(df.shape[1])

