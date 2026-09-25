import os
from scapy.all import rdpcap
import pandas as pd

data = {
            "Bing_>2kb":[0] * 10,
            "Bing_>1kb":[0] * 10,
            ">2kb数_Bing":[0] * 10,
            ">1kb数_Bing":[0] * 10,
            "总数_Bing": [0] * 10,
            "Baidu_>2kb":[0] * 10,
            "Baidu_>1kb":[0] * 10,
            ">2kb数_Baidu": [0] * 10,
            ">1kb数_Baidu": [0] * 10,
             "总数_Baidu": [0] * 10,
        }
datastr = 'E:\\FSCVA实验资料\\FSCVA\\Pcap_processed\\Bing'  # 修改为你的数据集路径
for i in range(2013, 2023):

    # 设置数据集文件夹路径
    dataset_folder = datastr + '\\' + str(i)

    # 初始化载荷大小区间统计字典
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
    # 遍历数据集文件夹中的PCAP文件
    for filename in os.listdir(dataset_folder):
        if filename.endswith('.pcap'):
            pcap_file_path = os.path.join(dataset_folder, filename)

        # 使用Scapy读取PCAP文件
        packets = rdpcap(pcap_file_path)
        total_size += len(packets)

        # 遍历数据包
        for packet in packets:
            # 获取载荷大小
            payload_size = len(packet.payload)

            # 根据统计区间更新计数
            if payload_size <= 128:
                payload_size_intervals['0-128'] += 1
            elif payload_size <= 256:
                payload_size_intervals['129-256'] += 1
            elif payload_size <= 384:
                payload_size_intervals['257-384'] += 1
            elif payload_size <= 512:
                payload_size_intervals['385-512'] += 1
            elif payload_size <= 640:
                payload_size_intervals['513-640'] += 1
            elif payload_size <= 768:
                payload_size_intervals['641-768'] += 1
            elif payload_size <= 896:
                payload_size_intervals['769-896'] += 1
            elif payload_size <= 1024:
                payload_size_intervals['897-1024'] += 1
            elif payload_size <= 1152:
                payload_size_intervals['1025-1152'] += 1
                extra_size += 1
            elif payload_size <= 1280:
                payload_size_intervals['1153-1280'] += 1
                extra_size += 1
            elif payload_size <= 1408:
                payload_size_intervals['1281-1408'] += 1
                extra_size += 1
            elif payload_size <= 1536:
                payload_size_intervals['1409-1536'] += 1
                extra_size += 1
            elif payload_size <= 1664:
                payload_size_intervals['1537-1664'] += 1
                extra_size += 1
            elif payload_size <= 1792:
                payload_size_intervals['1665-1792'] += 1
                extra_size += 1
            elif payload_size <= 1920:
                payload_size_intervals['1793-1920'] += 1
                extra_size += 1
            elif payload_size <= 2048:
                payload_size_intervals['1921-2048'] += 1
                extra_size += 1
            else:
                payload_size_intervals['2049+'] += 1
                extra_size += 1
    data['Bing_>2kb'][i - 2013] = payload_size_intervals['2049+'] / total_size
    data['>2kb数_Bing'][i - 2013] = payload_size_intervals['2049+']
    data['>1kb数_Bing'][i - 2013] = extra_size
    data['Bing_>1kb'][i - 2013] = extra_size / total_size
    data['总数_Bing'][i - 2013] = total_size


datastr1 = 'E:\\FSCVA实验资料\\FSCVA\\Pcap_processed\\Baidu'  # 修改为你的数据集路径
for i in range(2013, 2023):
    total_size = 0
    extra_size = 0

    # 设置数据集文件夹路径
    dataset_folder1 = datastr1 + '\\' + str(i)

    # 初始化载荷大小区间统计字典
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

    # 遍历数据集文件夹中的PCAP文件
    for filename in os.listdir(dataset_folder1):
        if filename.endswith('.pcap'):
            pcap_file_path = os.path.join(dataset_folder1, filename)

        # 使用Scapy读取PCAP文件
        packets = rdpcap(pcap_file_path)

        total_size += len(packets)

        # 遍历数据包
        for packet in packets:
            # 获取载荷大小
            payload_size = len(packet.payload)

            # 根据统计区间更新计数
            if payload_size <= 128:
                payload_size_intervals['0-128'] += 1
            elif payload_size <= 256:
                payload_size_intervals['129-256'] += 1
            elif payload_size <= 384:
                payload_size_intervals['257-384'] += 1
            elif payload_size <= 512:
                payload_size_intervals['385-512'] += 1
            elif payload_size <= 640:
                payload_size_intervals['513-640'] += 1
            elif payload_size <= 768:
                payload_size_intervals['641-768'] += 1
            elif payload_size <= 896:
                payload_size_intervals['769-896'] += 1
            elif payload_size <= 1024:
                payload_size_intervals['897-1024'] += 1
            elif payload_size <= 1152:
                payload_size_intervals['1025-1152'] += 1
                extra_size += 1
            elif payload_size <= 1280:
                payload_size_intervals['1153-1280'] += 1
                extra_size += 1
            elif payload_size <= 1408:
                payload_size_intervals['1281-1408'] += 1
                extra_size += 1
            elif payload_size <= 1536:
                payload_size_intervals['1409-1536'] += 1
                extra_size += 1
            elif payload_size <= 1664:
                payload_size_intervals['1537-1664'] += 1
                extra_size += 1
            elif payload_size <= 1792:
                payload_size_intervals['1665-1792'] += 1
                extra_size += 1
            elif payload_size <= 1920:
                payload_size_intervals['1793-1920'] += 1
                extra_size += 1
            elif payload_size <= 2048:
                payload_size_intervals['1921-2048'] += 1
                extra_size += 1
            else:
                payload_size_intervals['2049+'] += 1
                extra_size += 1

    data['Baidu_>2kb'][i - 2013] = payload_size_intervals['2049+'] / total_size
    data['>2kb数_Baidu'][i - 2013] = payload_size_intervals['2049+']
    data['>1kb数_Baidu'][i - 2013] = extra_size
    data['Baidu_>1kb'][i - 2013] = extra_size / total_size
    data['总数_Baidu'][i - 2013] = total_size

df = pd.DataFrame(data, index=range(2013, 2023))
df.to_excel(r"E:\FSCVA实验资料\FSCVA\统计表格_搜索引擎.xlsx", engine='openpyxl')
print("数据已成功写入")

# # 绘制分布图
# intervals = list(payload_size_intervals.keys())
# counts = list(payload_size_intervals.values())
#
# plt.figure(figsize=(15, 8))
# bars = plt.bar(intervals, counts)
#
# # 添加数量标签
# for bar in bars:
#     yval = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')
#
# # 添加网格线
# plt.grid(axis='y', linestyle='--', alpha=0.7)
#
# plt.xlabel('payload size')
# plt.ylabel('number of packets')
# plt.xticks(rotation=90)
#
# # 保存为图片
# image_path = dataset_folder + '.png'
# plt.savefig(image_path, bbox_inches='tight')

# # 创建PDF文档并插入图片
# pdf = FPDF()
# pdf.add_page()
# pdf.image(image_path, x=10, y=10, w=180)
# pdf_path = datastr + '.pdf'
# pdf.output(pdf_path)

# print(f'PDF图片已生成并保存至：{pdf_path}')