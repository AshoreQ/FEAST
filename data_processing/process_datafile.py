import os


AUTO_WORD = "autoword.txt"


# 删除在autoword.txt文件中的搜索词pcap文件,DataFile是要删除的文件所在的文件夹
def deletePcapFileByFileName(DataFile):

    with open(AUTO_WORD) as f:
        word_list = f.read().splitlines()
        print(word_list)

    for i in range(1, 15):
        train = DataFile + "/TrainData" + str(i)
        test = DataFile + "/TestData" + str(i)
        print(train)
        for pcap_file in os.listdir(train):
            rm = False
            for word in word_list:
                if word in pcap_file:
                    rm = True
            if rm:
                print("delete:",pcap_file)
                os.remove(train + "/" + pcap_file)

        print(test)
        for pcap_file in os.listdir(test):
            rm = False
            for word in word_list:
                if word in pcap_file:
                    rm = True
            if rm:
                print("delete:",pcap_file)
                os.remove(test + "/" + pcap_file)


if __name__ == "__main__":
    deletePcapFileByFileName("../Data/Data2020")


