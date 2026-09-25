import pandas as pd
import numpy as np

CSV_FILE = "../DataSet/combination/ebay1.csv"
start = 0
end = 100
rate = 20

df = pd.read_csv(CSV_FILE)
len = df.shape[0]
for i in range(0,len):
    idx = np.random.randint(start, end)
    if idx <= rate:
        #print(idx)
        df.loc[df.shape[0]] = df.iloc[i]
        for j in range(4,df.shape[1]):
            # print(df.iloc[i,j])
            df.iloc[i,j] += ((np.random.random() - 0.5) * (end / 10))
            # print(df.iloc[i, j])
            # print("-----------------")
        # print("***************")

df.to_csv(CSV_FILE, mode="w", index=None)






