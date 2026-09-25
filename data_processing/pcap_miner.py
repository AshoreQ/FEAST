import os
from get_ip import getIp
from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap

MIN_GAP_TIME = 0.5
# bing
# MIN_GAP_TIME = 0.7


def getData(DATA_FILE):
    data = []
    # 得到这个文件夹里的所有文件名
    for pcap_file in os.listdir(DATA_FILE):
        print("处理：", pcap_file)
        # 获取数据包的源目的ip
        pcap_file = DATA_FILE + "/" + pcap_file
        ips = getIp(pcap_file)
        remote_ip = ips[0]  # 搜索引擎的ip，就是数据包的源ip
        local_ip = ips[1]  # 本机的ip，就是数据包的目的ip

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
                # 根据ip地址和数据包大小过滤
                # 不是bing
                if '202.89.233.101' not in remote_ip:
                    if (ip_pkt.src in remote_ip or remote_ip is None) and ip_pkt.dst == local_ip and len(
                            tcp_pkt.payload) != 0 and len(tcp_pkt.payload) <= 1024:
                        pkg_list.append(pkt)
                # 是bing的话单独处理
                else:
                    if is_first_pkt:  # 第一块无关的包统一加进去
                        if (ip_pkt.src in remote_ip or remote_ip is None) and ip_pkt.dst == local_ip and len(
                                tcp_pkt.payload) != 0:
                            is_first_pkt = False
                            pkg_list.append(pkt)
                    else:
                        if (ip_pkt.src in remote_ip or remote_ip is None) and ip_pkt.dst == local_ip and len(
                                tcp_pkt.payload) != 0 and len(tcp_pkt.payload) <= 1024:
                            pkg_list.append(pkt)
        if pkg_list == []:
            print(pcap_file, ':isEmpty or ip not update')
            continue
        else:
            pkg_list = [pkg_list[0]] + pkg_list  # 这一步操作是为了分块的时候不用特别判断第一块

        # 文件名格式 search_aaron_hernandez_trial_3.pcap 得到第一个“_”和"_trial"之间的 其实就是搜索词，就是标签名
        label = pcap_file[pcap_file.index('_') + 1:pcap_file.index('_trial')]

        # 分块，根据时间间隔和数据包大小
        line = [0, 0, 0]  # 第一个位置是所有有效数据包的总数量，第二个位置是分块总数量，第三个位置是所有有效数据包的有效载荷总大小
        chunk_size = 0  # 块大小
        if '202.89.233.101' not in remote_ip:
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
            line.insert(0, label)
            print(line)
            data.append(line)
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
            line.insert(0, label)
            print(line)
            data.append(line)
            # df.loc[len(df.index)] = line

    return data