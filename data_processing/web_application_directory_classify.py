import os
import shutil
import re

def extract_words(txt_file_path):
    """
    从txt文件中提取单词

    :param txt_file_path: 包含单词的txt文件路径
    :return: 单词列表
    """
    words = []
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 使用正则表达式匹配单词
        matches = re.findall(r"'(.*?)'", content)
        for match in matches:
            words.extend(match.split())
    return words

def classify_files(txt_file_path, folder_path, new_folder_path):
    """
    根据txt文件中的单词对文件夹中的文件进行分类

    :param txt_file_path: 包含单词的txt文件路径
    :param folder_path: 要分类的文件夹路径
    :param new_folder_path: 分类后文件存放的新文件夹路径
    """
    # 提取txt文件中的单词
    words = extract_words(txt_file_path)

    # 创建新文件夹，如果已存在则清空
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    else:
        shutil.rmtree(new_folder_path)
        os.makedirs(new_folder_path)

    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 判断文件名是否包含txt文件中的单词
        if any(word.lower() in filename.lower() for word in words):
            # 将符合条件的文件复制到新文件夹中
            shutil.copy(file_path, new_folder_path)
            print(f"文件{filename}已复制到{new_folder_path}")

# 示例用法
txt_file_path = r'E:\FSCVA实验资料\FSCVA\web应用程序搜索清单2.txt'  # txt文件路径
folder_path = r'E:\FSCVA实验资料\FSCVA\Pcap\medicine30'  # 源文件夹路径
new_folder_path = r'E:\FSCVA实验资料\FSCVA\Pcap_processed\Hopkinson Hospital'  # 新文件夹路径
classify_files(txt_file_path, folder_path, new_folder_path)