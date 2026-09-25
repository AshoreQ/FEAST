import os

import pandas as pd
from scapy.all import rdpcap
from scapy.layers.inet import TCP, IP


# for year in range(2013, 2023):
#     year_folder = os.path.join(folder_path, str(year))
#     for file in os.listdir(year_folder):
#         match = re.match(r"search_(.*)_trail_(\d+)", file)
#         if match:
#             search_term = match.group(1)
#             num = match.group(2)
#             print(f"Search Term: {search_term}, Num: {num}")
#
# def extract_packet_sizes(pcap_file):
#     packets = rdpcap(pcap_file)
#     sizes = [len(packet) for packet in packets]
#     return sizes
#
# # 示例：提取文件夹中所有PCAP文件的流量大小
# for year in range(2013, 2023):
#     for file in os.listdir(year_folder):
#         if file.endswith(".pcap"):
#             pcap_file = os.path.join(year_folder, file)
#             sizes = extract_packet_sizes(pcap_file)
#             print(f"File: {file}, Sizes: {sizes}")
#
# def calculate_flow_ranges(search_term, sizes):
#     char_ranges = {}
#     for char in search_term:
#         char_ranges[char] = (min(sizes), max(sizes))
#     return char_ranges
#
# from scapy.all import *
#


def extract_flow_packets(pcap_file, src_ip_lst, protocol, size_range):
    # 读取pcap文件
    packets = rdpcap(pcap_file)

    # 过滤符合条件的包
    filtered_packets = []
    for packet in packets:
        if IP in packet and packet[IP].src in src_ip_lst:
            if TCP in packet:  # 假设TLS流量使用端口443
                if size_range[0] <= len(packet) <= size_range[1]:
                    filtered_packets.append(packet)

    return filtered_packets

def process_pcap_files(folder_path, src_ip_lst, protocol, size_range):
    global search_name_lst
    global final_dct
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pcap'):
                pcap_file = os.path.join(root, file)
                packets = extract_flow_packets(pcap_file, src_ip_lst, protocol, size_range)
                # print(f"Processing {pcap_file}: {len(packets)} packets found")

                # 提取搜索词并统计每个字符对应的流量包大小
                search_term = file.split('_')[1:-2]  # 假设文件名格式为 search_xxx_xxx_..._xxx_trail_YYY.pcap
                search_term = ''.join(search_term)  # 拼接搜索词
                # print(f"Search Term: {search_term}")
                search_name_lst.append(search_term)
                if search_term not in final_dct:
                    final_dct[search_term] = {}

                # 提取前len(search_term)个符合条件的流量包
                # pos: 字符编号
                if len(packets) >= len(search_term):
                    for pos, char in enumerate(search_term):
                        packet_size = len(packets[pos])
                        if pos not in final_dct[search_term]:
                            final_dct[search_term][pos] = [packet_size]
                        else:
                            final_dct[search_term][pos].append(packet_size)
                        # print(f"Character '{char}' corresponds to packet size: {packet_size} bytes")

                    # 新增统计搜索词字符相邻之间的这段时间间隔的累计流量包大小
                # if len(packets) >= len(search_term) + 1:
                #     for pos in range(1, len(search_term) + 1):
                #         # 计算相邻字符之间的累计流量包大小
                #         start_time = packets[pos - 1].time
                #         end_time = packets[pos].time
                #         time_interval_packets = [pkt for pkt in rdpcap(pcap_file) if start_time <= pkt.time < end_time]
                #         # max_size = 0
                        # for pkt in time_interval_packets:
                        #     if not pkt.haslayer(IP):
                        #         continue
                        #     ip_pkt = pkt.getlayer(IP)
                        #     if not ip_pkt.haslayer(TCP):
                        #         continue
                        #     tcp_pkt = ip_pkt.getlayer(TCP)
                        #     max_size = max(max_size, len(tcp_pkt.payload))
                        # # 存储相邻字符的累计流量包大小
                        # if f"{pos - 1}-{pos}" not in final_dct[search_term]:
                        #     final_dct[search_term][f"{pos - 1}-{pos}"] = [max_size]
                        # else:
                        #     final_dct[search_term][f"{pos - 1}-{pos}"].append(max_size)

folder_path = r"E:\FSCVA实验资料\FSCVA\Pcap_processed\Bing"
search_name_lst = []
final_dct = {}
src_ip_lst = ['202.89.233.100', '202.89.233.101', '202.89.233.102']
for i in range(2013, 2023):
    file_path = folder_path + f"\\{i}"
    process_pcap_files(file_path, src_ip_lst, 'TLSv1.2', (196, 205))
print("write to excel")
for search_term, dct in final_dct.items():
    print(search_term)
    df = pd.DataFrame.from_dict(final_dct[search_term])
    df.to_excel(r"E:\FSCVA实验资料\FSCVA\Pcap_processed\Bing\search_words_dct" + f"\\{search_term}.xlsx", engine='openpyxl')
print("end")