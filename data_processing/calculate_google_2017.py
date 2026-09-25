import os
from scapy.all import rdpcap
import pandas as pd

data = {
    "Google2017_>2kb": 0,
    "Google2017_>1kb": 0,
    ">2kb数_Google2017": 0,
    ">1kb数_Google2017": 0,
    "总数_Google2017": 0,
}

datastr = r'E:\FSCVA实验资料\FSCVA\Pcap\data1 Google'  # 修改为你的数据集路径

payload_size_intervals = {
    '0-128': 0,
    '129-256': 0,
    '257-384': 0,
    '385-512': 0,
    '513-640': 0,
    '641-768': 0,
    '769-896': 0,
    '897-1024': 0,
    '1025-1152': 0,
    '1153-1280': 0,
    '1281-1408': 0,
    '1409-1536': 0,
    '1537-1664': 0,
    '1665-1792': 0,
    '1793-1920': 0,
    '1921-2048': 0,
    '2049+': 0
}

total_size = 0
extra_size = 0

def update_interval(payload_size):
    for interval, count in payload_size_intervals.items():
        if interval == '2049+':
            if payload_size > 2048:
                payload_size_intervals[interval] += 1
                return
        else:
            lower, upper = map(int, interval.split('-'))
            if lower <= payload_size <= upper:
                payload_size_intervals[interval] += 1
                return

# 遍历数据集文件夹中的PCAP文件
for filename in os.listdir(datastr):
    if filename.endswith('.pcap'):
        pcap_file_path = os.path.join(datastr, filename)

        try:
            packets = rdpcap(pcap_file_path)
        except Exception as e:
            print(f"无法读取文件 {pcap_file_path}: {e}")
            continue

        total_size += len(packets)

        for packet in packets:
            payload_size = len(packet.payload)
            update_interval(payload_size)
            if payload_size > 2048:
                payload_size_intervals['2049+'] += 1
            if payload_size > 1024:
                extra_size += 1

data['Google2017_>2kb'] = payload_size_intervals['2049+'] / total_size if total_size > 0 else 0
data['>2kb数_Google2017'] = payload_size_intervals['2049+']
data['>1kb数_Google2017'] = extra_size
data['Google2017_>1kb'] = extra_size / total_size if total_size > 0 else 0
data['总数_Google2017'] = total_size

df = pd.DataFrame([data])  # 将数据转换为单行DataFrame
df.to_excel(r"E:\FSCVA实验资料\FSCVA\Google2017_统计表格.xlsx", engine='openpyxl')
print("数据已成功写入")