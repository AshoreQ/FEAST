from scapy.all import *
from scapy.layers.inet import IP


def count_packets(pcap_file, dst_ip, min_size, max_size):
    packets = rdpcap(pcap_file)
    count = 0
    for packet in packets:
        if packet.haslayer(IP) and packet[IP].dst == dst_ip and min_size <= len(packet) <= max_size:
            count += 1
    return count

# 参数
pcap_file = r"E:\FSCVA实验资料\FSCVA\Pcap_processed\Bing\2020\search_Coronavirus_symptoms_trial_2.pcap"  # 替换为你的 PCAP 文件路径
dst_ip = "172.19.0.2"
min_size = 195
max_size = 205

# 统计并输出结果
result = count_packets(pcap_file, dst_ip, min_size, max_size)
print(f"符合条件的数据包个数：{result}")