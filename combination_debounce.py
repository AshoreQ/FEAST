"""
合并版 combination.py
输出列：label | 4 维基础统计 | 30 维 cumul | 3 维 chunk 统计 | N 维 chunk_size | 48 维 polling
"""

import os
import csv
import datetime
import numpy as np
import pandas as pd
from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap

# --------------- 原有依赖 ---------------
from get_ip import getIp
from temporal_feature import get_temporal_feature
# --------------- 新增依赖（polling 特征） ---------------
from debounce import extract_from_temporal   # 同目录即可

# --------------- 超参（与 debounce_feature.py 保持一致） ---------------
T = 0.1
byte_per_char = 1
k = 20
MIN_GAP_TIME = 0.5          # 原 combination 里的分块阈值

# --------------- 本地 IP 列表（原脚本里那一大串） ---------------
LOCAL_IP = [
    '192.168.247.139', '192.168.125.100', '192.168.25.129', '192.168.88.128',
    '192.168.139.131', '192.168.101.129', '172.20.0.2', '192.168.238.129',
    '192.168.248.129', '192.168.200.138', '192.168.195.128',
    "172.21.0.2", "172.19.0.2", "172.18.0.2", "172.22.0.2", "172.23.0.2",
    "172.25.0.2", "172.27.0.2", "172.30.0.2", "172.26.0.2",
    "192.168.0.2", "192.168.112.2", "192.168.96.2", "192.168.32.2",
    "192.168.139.129"
]

# ===================================================================
# 以下函数基本沿用原 combination.py 逻辑，仅把「特征提取」部分拆成两步
# ===================================================================
def extract_comb_features(pcap_path, remote_ip):
    """
    返回 CUMUL+chunk 特征列表（长度不固定，后面会统一补零）
    """
    # 1. 读包并过滤
    pkts = rdpcap(pcap_path)
    pkg_list = []
    is_first = True
    for pkt in pkts:
        if not pkt.haslayer(IP):
            continue
        ip = pkt[IP]
        if not ip.haslayer(TCP):
            continue
        tcp = ip[TCP]
        # 方向判断
        if ip.src in remote_ip and ip.dst in LOCAL_IP and len(tcp.payload) > 0:
            # 非 bing 的额外长度过滤
            if '202.89.233.101' not in remote_ip and '202.89.233.100' not in remote_ip:
                if len(tcp.payload) > 1024:
                    continue
            # bing 的第一包不过滤长度
            if '202.89.233.101' in remote_ip or '202.89.233.100' in remote_ip:
                if is_first:
                    is_first = False
                else:
                    if len(tcp.payload) > 1024:
                        continue
            pkg_list.append(pkt)
    if not pkg_list:
        return []

    # 2. 基础 4 维 + 30 维 cumul
    in_pkt = in_size = out_pkt = out_size = 0
    graph = []          # [(x, y)]
    for pkt in pkts:
        if not pkt.haslayer(IP):
            continue
        ip = pkt[IP]
        x = len(graph) + 1
        if ip.src in remote_ip:
            in_pkt += 1
            in_size += len(ip.payload)
            y = (graph[-1][1] if graph else 0) + len(ip.payload)
        elif ip.src in LOCAL_IP:
            out_pkt += 1
            out_size += len(ip.payload)
            y = (graph[-1][1] if graph else 0) - len(ip.payload)
        else:
            continue
        graph.append([x, y])
    if not graph:
        return []
    base = [in_pkt, in_size, out_pkt, out_size]

    # 30 维 cumul
    max_x = graph[-1][0]
    gap = max_x / 31.0
    cumul = []
    ptr = 0
    for i in range(1, 31):
        sample_x = gap * i
        while ptr < len(graph) - 1 and graph[ptr][0] < sample_x:
            ptr += 1
        nx, ny = graph[ptr][0], graph[ptr][1]
        lx, ly = graph[ptr - 1][0], graph[ptr - 1][1]
        slope = (ny - ly) / float(nx - lx)
        sample_y = slope * (sample_x - lx) + ly
        cumul.append(sample_y)

    # 3. chunk 分块
    chunk_sizes = []
    chunk_count = 0
    cur_size = 0
    for i in range(1, len(pkg_list)):
        prev, curr = pkg_list[i - 1], pkg_list[i]
        cur_size += len(curr[TCP].payload)
        if abs(curr.time - prev.time) <= MIN_GAP_TIME:
            continue
        # 一次间隔结束
        if cur_size > 50:
            chunk_sizes.append(cur_size)
            chunk_count += 1
        cur_size = len(curr[TCP].payload)
    # 末尾包
    if cur_size > 50:
        chunk_sizes.append(cur_size)
        chunk_count += 1

    total_pkg = len(pkg_list) - 1
    total_size = sum(len(p[TCP].payload) for p in pkg_list[1:])
    comb_feat = base + cumul + [total_pkg, chunk_count, total_size] + chunk_sizes
    return comb_feat


def process_folder(DATA_DIR):
    rows = []
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith('.pcap'):
            continue
        print('[comb+polling] 处理：', fname)
        label = fname[fname.index('_') + 1:fname.index('_trial')]
        pcap_path = os.path.join(DATA_DIR, fname)
        remote_ip = getIp(pcap_path)[0]

        # 1. 组合特征
        comb = extract_comb_features(pcap_path, remote_ip)
        if not comb:
            continue

        # 2. polling 48 维
        website, df, df_all = get_temporal_feature(pcap_path)
        debounce = extract_from_temporal(df_all, remote_ip, T=T,
                                         byte_per_char=byte_per_char, k=k)
        debounce = debounce.tolist()

        # 3. 合并
        row = [label] + comb + debounce
        rows.append(row)
    return rows


# ===================================================================
# 主入口
# ===================================================================
# =============  只替换主程序最后一段即可  =============
if __name__ == '__main__':
    DATA_DIR = '../data/Amazon/'          # 改成自己的目录
    SAVE_CSV = '../dataset/combinations/Amazon/Amazon_debounce.csv'

    start = datetime.datetime.now()
    data = process_folder(DATA_DIR)
    if not data:
        print('目录下无有效 pcap，退出')
        exit()

    # 补零对齐
    max_len = max(len(r) for r in data)
    with open(SAVE_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in data:
            writer.writerow(r + [0] * (max_len - len(r)))

    # 用 pandas 读入，自动生成数字列
    df = pd.read_csv(SAVE_CSV, header=None)

    # 构造与列数完全一致的列名
    cols = ['label'] \
           + ['in_pkt', 'in_size', 'out_pkt', 'out_size'] \
           + ['cumul_{}'.format(i) for i in range(1, 31)] \
           + ['pkg_count', 'chunk_count', 'total_size'] \
           + ['chunk_{}'.format(i) for i in range(1, max_len - 36)] \
           + ['debounce_{}'.format(i) for i in range(1, 49)]
    # 如果 chunk 为空，上面会多算或少算，这里直接截 / 补
    if len(cols) < df.shape[1]:
        cols += ['unknown_{}'.format(i) for i in range(len(cols)+1, df.shape[1]+1)]
    df.columns = cols[:df.shape[1]]   # 保证长度严格一致

    df.to_csv(SAVE_CSV, index=None)
    end = datetime.datetime.now()
    print('合并完成，形状：', df.shape, '耗时：', (end - start).seconds, 's')