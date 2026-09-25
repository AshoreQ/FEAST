import  dpkt
import socket
import string
import numpy as np
import pandas as pd

def ip_to_str(ipv6, address):
    '''
    Transform a int ip address to a human readable ip address (ipv4).
    '''
    ip_fam = socket.AF_INET

    if ipv6:
        ip_fam = socket.AF_INET6

    return socket.inet_ntop(ip_fam, address)

def load_pcap(fname):
    '''
    Load a pcap file into a pandas dataframe.
    '''
    if fname.endswith('.pcap'):
        rows = []
        for ts, buf in dpkt.pcap.Reader(open(fname, 'rb')):
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == dpkt.ethernet.ETH_TYPE_IP or eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                ip = eth.data
                if ip.p == dpkt.ip.IP_PROTO_TCP:
                    tcp = ip.data
                    rows.append((ip_to_str(eth.type == dpkt.ethernet.ETH_TYPE_IP6, ip.src), ip_to_str(eth.type == dpkt.ethernet.ETH_TYPE_IP6, ip.dst), ts*1000, len(tcp.data), ip.p))
            df = pd.DataFrame(rows, columns=['src', 'dst', 'frame_time', 'frame_length', 'protocol'])
    return df

def fixed_length(arr, k, pad_value=0.0):
    """
    将 1-D 序列截断或补长到固定长度 k
    arr : list / ndarray
    k   : 目标长度
    pad_value : 填充值
    return : ndarray, shape=(k,)
    """
    arr = np.asarray(arr, dtype=float)
    if len(arr) == k:
        return arr
    if len(arr) > k:                      # 截断
        return arr[:k]
    pad_len = k - len(arr)                # 补长
    return np.concatenate([arr, [pad_value] * pad_len])

def get_outgoing_packets(df, server_ips):
    """
    从完整流量中筛选出 outgoing（客户端 → 服务器）的包。
    假设服务器 IP 已知（可通过 DNS 或手动指定）。
    """
    local_ips = ['192.168.247.139', '192.168.125.100', '192.168.25.129', '192.168.88.128', '192.168.139.131',
                            '192.168.101.129'
        , '172.20.0.2', '192.168.238.129', '192.168.248.129', '192.168.200.138', '192.168.125.100', '192.168.195.128'
        , "172.21.0.2", "172.19.0.2", "172.18.0.2", "172.20.0.2", "172.22.0.2", "172.23.0.2", "172.25.0.2", "172.27.0.2"
        , "172.30.0.2", "172.26.0.2", "192.168.0.2", "192.168.112.2", "192.168.96.2", "192.168.32.2", "192.168.139.129"]
    outgoing = df[(df['dst'].isin(server_ips)) & (df['src'].isin(local_ips))].copy()
    outgoing = outgoing.sort_values('frame_time').reset_index(drop=True)
    return outgoing

def extract_discriminative_features(outgoing_df, max_len=50):
    """
    提取用于事件处理模型识别的判别性特征。
    输入: outgoing_df (DataFrame with columns: frame_time, frame_length)
    输出: dict of scalar features
    """
    if len(outgoing_df) < 2:
        # 无法计算差分，返回默认值
        return {
            'mean_interval': 0.0,
            'std_interval': 0.0,
            'cv_interval': np.inf,
            'multi_char_ratio': 0.0,
            'num_requests': len(outgoing_df),
            'sizes_seq': fixed_length([], max_len),
            'intervals_seq': fixed_length([], max_len - 1)
        }

    # 1. 包大小序列（payload size）
    sizes = outgoing_df['frame_length'].values.astype(float)
    delta_sizes = np.diff(sizes)  # 每次请求增加的字节数

    # 2. 时间间隔（ms）
    ts = outgoing_df['frame_time'].values
    intervals = np.diff(ts)  # 单位：毫秒

    # 3. 统计特征
    mean_int = np.mean(intervals)
    std_int = np.std(intervals)
    cv = std_int / mean_int if mean_int > 1e-6 else np.inf

    # 4. 多字符合并比例：delta > 1.5 视为一次合并（因每字符≈1字节）
    multi_char_ratio = np.mean(delta_sizes > 1.5)

    # 5. 固定长度序列（用于后续 ML 或可视化）
    sizes_seq = fixed_length(sizes, max_len, pad_value=0.0)
    intervals_seq = fixed_length(intervals, max_len - 1, pad_value=0.0)

    return {
        'mean_interval': float(mean_int),
        'std_interval': float(std_int),
        'cv_interval': float(cv),
        'multi_char_ratio': float(multi_char_ratio),
        'num_requests': len(outgoing_df),
        'sizes_seq': sizes_seq,
        'intervals_seq': intervals_seq
    }