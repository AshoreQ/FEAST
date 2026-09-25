## Folder Description

### 1. src/container_isolated_browser

```shell
container_isolated_browser:
    - Code for generating the dataset
    - Contains an autoword.txt file, which configures the search items to be captured
    - Dockerfile configures Docker. After configuration, run: ./Dockerfile
    - After configuring the search engine in automate_search.sh, run it via the command line
    - Command line includes:
        - docker-compose build
        - docker-compose up -d
        - docker exec -it auto_isolated_browser_1 bash
        - mkdir temp   Create a temp folder inside the container
        - ./automate_search.sh [i]   Generate pcap dataset and place it in the temp folder
        - docker cp debf4a79c426:test  /home/admin1/NetworkSideChannel-master/Pcap   Copy the temp folder from the container to the disk (debf4a79c426: change to your own container ID; change the destination path to your own address)
        - rm -rf test   Delete the dataset inside the container to avoid insufficient space
        - docker-compose down
```

### 2. src/data_processing

```shell
data_processing:
    - Code for data processing
    - autoword.txt: Contains the search items for the dataset. The dataset must correspond to the search items, neither more nor less.
    - determine.py: Configure which datasets to run
    - get_features.py: Extract features
    - get_ip.py: Add the search engine server and local IP addresses
    - pcap_miner.py: Filter
    - Run ./determine.py to start classification
```

### 3. src/models

```shell
model:
    - Machine learning code
```

### 4. src/network_side_channel

```shell
network_side_channel:
    - Sample code for testing side-channel vulnerabilities
```

### 5. EventQLeak

 https://pan.baidu.com/s/1tPIIF3v5n8kYYHmVjc7ziA?pwd=pjq3 

### 6. Appendix.pdf

This document contains supplementary experimental results omitted from the main paper, along with the corresponding figures and tables.

