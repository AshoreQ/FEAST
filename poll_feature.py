import os
import csv
import numpy as np
import pandas as pd
import datetime

from src.get_ip import getIp
from temporal_feature import get_temporal_feature   # 复用现有
from polling import extract_from_temporal           # 直接调用你写的函数

# ============= 可调超参 =============
T              = 0.1            # polling 周期（Bing=0.1 s）
byte_per_char  = 1              # 字母=1，空格=3 可改
k              = 90             # 输出序列固定长度
# =====================================

def get_polling_data(DATA_FILE):
    """
    不再 detect_model，**全部当 polling 处理**
    """
    data = []
    for pcap_file in os.listdir(DATA_FILE):
        print("polling处理：", pcap_file)

        label = pcap_file[pcap_file.index('_') + 1:pcap_file.index('_trial')]

        pcap_path = os.path.join(DATA_FILE, pcap_file)
        ips = getIp(pcap_path)
        remote_ip = ips[0]
        # 1. 解析成 DataFrame
        website, _, df = get_temporal_feature(pcap_path)

        # 2. 直接当 polling 提取 42 维
        F_poll = extract_from_temporal(df, remote_ip, T=T,
                                       byte_per_char=byte_per_char, k=k)
        row = [label] + F_poll.tolist()
        data.append(row)

    return data


def write_csv(data, csv_path):
    """
    补零对齐 → 写 CSV → 加列名
    """
    if not data:
        print("未找到任何样本！")
        return
    max_len = max(len(r) for r in data)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        for row in data:
            writer.writerow(row + [0] * (max_len - len(row)))

    # 加列头
    df = pd.read_csv(csv_path, header=None)
    cols = ['label'] + [f'poll_{i}' for i in range(1, max_len)]
    df.columns = cols
    df.to_csv(csv_path, index=None)
    print(f"保存完成：{csv_path}, 形状：{df.shape}")


# =================== 主入口 ===================
if __name__ == '__main__':
    # 1. 数据目录（可改成任意站点）
    DATA_FILE = "../data/fit/Taobao"          # 你的 polling 数据
    CSV_FILE  = "../dataset/polling/Taobao/polling.csv"

    # 2. 对应搜索引擎 IP（Bing 为例）
    # remote_ip = ['202.89.233.101', '13.107.21.200',
    #              '202.89.233.100', '106.117.216.33']
    # 3. 运行
    start = datetime.datetime.now()
    data = get_polling_data(DATA_FILE)
    write_csv(data, CSV_FILE)
    end = datetime.datetime.now()
    print("polling comb 耗时：", (end - start).seconds, "s")