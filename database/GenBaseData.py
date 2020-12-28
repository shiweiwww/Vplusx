import os
import chardet
from read_byurl import *
import random
import time
import json
import sys
sys.path.append("..")
from config import DATABASE,DEFAULT_YEARS

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False
class BaseData:
    def __init__(self,AStock_path=None,years=None):
        self.AStock_path = AStock_path
        self.years = years
        self.name_2_id = {}
        self.id_2_name = {}
        self.name_to_id()

    def name_to_id(self):
        f = open(self.AStock_path,'r',encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            stockid,name,_,_,_ = line.split(',')
            stockid = stockid.strip('.SZ').strip('.SH')
            self.id_2_name[stockid]=name.strip()
            self.name_2_id[name.strip()] = stockid
    def save_info(self,path='data/info.json'):
        obj = json.dumps(self.id_2_name)
        f = open(path,'w',encoding='utf-8')
        f.write(obj)
        f.close()
    def to_csv(self,dataframe,path):
        dataframe.to_csv(path,sep=',',index=True,encoding='utf-8')
    def down_report(self,ids=None):
        for name,id in self.name_2_id.items():
            dir_path = r'data/%s'%(id)
            is_write = True
            if not mkdir(dir_path):
                nums = os.listdir(dir_path)
                if len(nums)==3:
                    is_write = False
                else:
                    is_write = True
            if is_write:
                # b = SpiderUrl.gen_data_bytype(id,type='b',years=["20141231","20151231","20161231","20171231","20181231","20191231"])
                b = SpiderUrl.gen_data_bytype(id,type='b',years = DEFAULT_YEARS)
                # p = SpiderUrl.gen_data_bytype(id,type='p',years=["20141231","20151231","20161231","20171231","20181231","20191231"])
                p = SpiderUrl.gen_data_bytype(id,type='p',years = DEFAULT_YEARS)
                # c = SpiderUrl.gen_data_bytype(id,type='c',years=["20141231","20151231","20161231","20171231","20181231","20191231"])
                c = SpiderUrl.gen_data_bytype(id,type='c',years= DEFAULT_YEARS)
                self.to_csv(b,dir_path+'/b.csv')
                self.to_csv(p,dir_path+'/p.csv')
                self.to_csv(c,dir_path+'/c.csv')
                print(name,'-',id,b.shape,p.shape,c.shape)
                time.sleep(7)
if __name__=='__main__':
    dt = BaseData('A.csv')
    dt.down_report()