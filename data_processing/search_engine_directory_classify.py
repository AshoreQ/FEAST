import os
import shutil
import re

def extract_words_by_year(txt_file_path):
    """
    从txt文件中按年份提取单词

    :param txt_file_path: 包含单词的txt文件路径
    :return: 字典，键为年份，值为单词列表
    """
    words_by_year = {}
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
        for line in content:
            # 使用正则表达式匹配年份和单词
            match = re.match(r"LABELS(\d{4})='(.*)'", line)
            if match:
                year = match.group(1)
                words = match.group(2).split()
                words_by_year[year] = words
    return words_by_year

def classify_files_by_year(txt_file_path, folder_path, base_new_folder_path):
    """
    根据txt文件中的单词按年份对文件夹中的文件进行分类

    :param txt_file_path: 包含单词的txt文件路径
    :param folder_path: 要分类的文件夹路径
    :param base_new_folder_path: 分类后文件存放的基础文件夹路径
    """
    # 按年份提取txt文件中的单词
    words_by_year = extract_words_by_year(txt_file_path)

    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 判断文件名是否包含txt文件中某一年份的单词
        for year, words in words_by_year.items():
            if any(word.lower() in filename.lower() for word in words):
                # 创建对应年份的新文件夹，如果已存在则不创建
                new_folder_path = os.path.join(base_new_folder_path, year)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                # 将符合条件的文件复制到对应年份的新文件夹中
                shutil.copy(file_path, new_folder_path)
                print(f"文件{filename}已复制到{new_folder_path}")

# 示例用法
txt_file_path = r'E:\FSCVA实验资料\FSCVA\搜索词清单2.txt'  # txt文件路径
folder_path = r'E:\FSCVA实验资料\FSCVA\Pcap\data3 Bing'  # 源文件夹路径
base_new_folder_path = r'E:\FSCVA实验资料\FSCVA\Pcap_processed\Bing'  # 分类后文件存放的基础文件夹路径
classify_files_by_year(txt_file_path, folder_path, base_new_folder_path)