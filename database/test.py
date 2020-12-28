import pandas as pd 
import os
f = open('A.csv','r',encoding='utf-8')
lines = f.readlines()
f.close()
for i in range(71):
    dt_frame = set()
    cnts = 0
    for line in lines:
        item = line.split(',')
        dt = pd.read_csv('data/%s/c.csv'%item[0][:-3])
        if dt.shape[0]==71:
            dt_frame.add(dt.iloc[i,0])
    print(dt_frame)