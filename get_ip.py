from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap


def getIp(PCAP_FILE):
    res = [[], 0]
    #all
    #list_all=["202.89.233.100","202.89.233.101","172.217.2.163","39.156.66.18", "39.156.66.14"]
    list_google = ["116.196.133.53"]
    p1 = "60.249."
    p2 = "61.216."
    for i in range(0, 255):
        for j in range(0, 255):
            list_google.append(p1 + str(i) + "." + str(j))
            list_google.append(p2 + str(i) + "." + str(j))



    #list_baidu=["39.156.66.18", "39.156.66.14","202.89.233.101","202.89.233.100"]
    list_baidu=['110.242.69.21', '110.242.70.57', '220.181.111.1', '39.156.70.239', '39.156.70.46', '106.117.216.33',
                     '220.181.111.232', "39.156.66.18", "39.156.66.14","110.242.68.4","110.242.68.3","111.63.60.33","220.181.38.149","220.181.38.150"]
    p3 = "110.242."
    for i in range(0, 255):
        for j in range(0, 255):
            list_baidu.append(p3 + str(i) + "." + str(j))
    list_bing=["202.89.233.100", "202.89.233.101"]
    #
    list_jingdong=["36.110.181.162","111.225.218.3","120.52.148.92"]
    list_amazon=["54.222.60.215", "54.222.60.225", "117.11.222.168"]
    list_ebay=["184.28.15.78"]
    list_medicine=["128.220.192.230","52.175.35.166",""]
    # list_taobao=["111.62.93.135", "111.62.93.135"]
    pre="59.82."
    list_taobao = []
    for i in range(0, 255):
        for j in range(0, 255):
            list_taobao.append(pre + str(i) + "." + str(j))


    # list_jingdong = ["183.246.207.38"]
    list2=["36.110.181.162"]
    # bing
    #list1 = ["202.89.233.100", "202.89.233.101"]
    #list2 = ["172.19.0.2", "172.18.0.2"]
    #google
    #list1=["172.217.2.163","1"]
    #list2=["172.19.0.2","172.18.0.2"]
    # baidu
    #list1 = ["39.156.66.18", "39.156.66.14",]
    #list2 = ["172.19.0.2","172.18.0.2"]
    # 0 remoteip 1 ourip

    # 读读取解析pcap文件，返回packetslist
    packet_capture = rdpcap(PCAP_FILE)
    # 遍历packet
    for pkt in packet_capture:

        # 过滤出IP数据包
        if not pkt.haslayer(IP):
            continue
        ip_pkt = pkt.getlayer(IP)

        # 过滤出tcp数据包
        if ip_pkt.haslayer(TCP):
            # 这个tcp_pkt没用到，不知道是干嘛用的了
            tcp_pkt = ip_pkt.getlayer(TCP)
            # if ip_pkt.src in list1 and ip_pkt.dst in list2:
            # 根据源ip地址过滤，返回一个对应搜索引擎的IP列表 res[1]是本地ip，res[0]是访问的ip
            if ip_pkt.dst in list2:
                if res[1] == 0:
                    res[1] = ip_pkt.dst
            if res[0]==[] and ip_pkt.src in list_baidu:
                res[0] = list_baidu
            if res[0]==[] and ip_pkt.src in list_google:
                res[0]=list_google
            if res[0]==[] and ip_pkt.src in list_bing:
                res[0]=list_bing
            if res[0] == [] and ip_pkt.src in list2:
                res[0] = list2
            if res[0] == [] and ip_pkt.src in list_taobao:
                res[0] = list_taobao
            if res[0] == [] and ip_pkt.src in list_amazon:
                res[0] = list_amazon
            if res[0] == [] and ip_pkt.src in list_ebay:
                res[0] = list_ebay
            if res[0] == [] and ip_pkt.src in list_medicine:
                res[0] = list_medicine
            if res[0]!=[] and res[1]!=0:
                break
    return res