import os
import csv
import numpy as np
import pandas as pd
import datetime

from src.get_ip import getIp
from temporal_feature import get_temporal_feature   # 复用现有
from debounce import extract_from_temporal           # 直接调用你写的函数

# ============= 可调超参 =============
T              = 0.1
byte_per_char  = 1              # 字母=1，空格=3 可改
k              = 20             # 输出序列固定长度
# =====================================

def get_debounce_data(DATA_FILE):
    """
    不再 detect_model，**全部当 polling 处理**
    """
    data = []
    # Bing ip 特殊处理
    # remote_ip = ['202.89.233.101', '13.107.21.200', '202.89.233.100', '106.117.216.33']
    local_ip = ['192.168.247.139', '192.168.125.100', '192.168.25.129', '192.168.88.128', '192.168.139.131',
                '192.168.101.129'
        , '172.20.0.2', '192.168.238.129', '192.168.248.129', '192.168.200.138', '192.168.125.100', '192.168.195.128'
        , "172.21.0.2", "172.19.0.2", "172.18.0.2", "172.20.0.2", "172.22.0.2", "172.23.0.2", "172.25.0.2", "172.27.0.2"
        , "172.30.0.2", "172.26.0.2", "192.168.0.2", "192.168.112.2", "192.168.96.2", "192.168.32.2",
                "192.168.139.129"]  # 本机的ip，就是数据包的目的ip
    for pcap_file in os.listdir(DATA_FILE):
        print("polling 处理：", pcap_file)
        label = pcap_file[pcap_file.index('_') + 1:pcap_file.index('_trial')]
        pcap_path = os.path.join(DATA_FILE, pcap_file)
        ips = getIp(pcap_path)
        remote_ip = ips[0]

        # 1. 解析成 DataFrame
        website, df, df_all = get_temporal_feature(pcap_path)

        # 2. 直接当 polling 提取 48 维
        F_debounce = extract_from_temporal(df_all, remote_ip, T=T,
                                       byte_per_char=byte_per_char, k=k)
        row = [label] + F_debounce.tolist()
        data.append(row)

    return data


def write_csv(data, csv_path):
    """
    补零对齐 → 写 CSV → 加列名
    """
    file_csv = open(csv_path, 'w', newline='', encoding='utf-8')
    # 把每一条数据都变成一样长，写入csv文件
    max_len = 0
    for line in data:
        if len(line) > max_len:
            max_len = len(line)
    csv_write = csv.writer(file_csv, dialect='excel')
    for line in data:
        line_max = [0] * max_len
        for i in range(len(line)):
            line_max[i] = line[i]
        # 把数据写入csv文件
        csv_write.writerow(line_max)
    file_csv.close()

    # 加列头
    df = pd.read_csv(csv_path, header=None)
    cols = ['label'] + [f'debounce_{i}' for i in range(1, max_len)]
    df.columns = cols
    df.to_csv(csv_path, index=None)
    print(f"保存完成：{csv_path}, 形状：{df.shape}")


# =================== 主入口 ===================
if __name__ == '__main__':
    # 1. 数据目录（可改成任意站点）
    DATA_FILE = "../data/JD/"
    CSV_FILE  = "../dataset/combinations/taobao_debounce.csv"

    # 2. 运行
    start = datetime.datetime.now()
    data = get_debounce_data(DATA_FILE)
    write_csv(data, CSV_FILE)
    end = datetime.datetime.now()
    print("polling 耗时：", (end - start).seconds, "s")