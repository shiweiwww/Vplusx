#coding:utf-8
import os
import sqlite3
import zlib
import json
import time
import datetime
import pandas as pd

class Dba:
    def __init__(self,database=None,pwd=None,is_server=False):
        self.database = database
        self.pwd = pwd
        self.is_server = is_server
        self.__init_handle__()

    def __init_handle__(self):
        self.conn = sqlite3.connect(self.database)

    @classmethod
    def op(cls,database=None,table_name=None,type=None,**kwgs):
        obj = cls(database)
        if type=='i':
            obj.insert(table_name,**kwgs)
        elif type=='u':
            obj.update(table_name,**kwgs)
        elif type=='s':
            return obj.select(table_name,**kwgs)
        elif type=='d':
            obj.delet(table_name,**kwgs)

    def delet(self,table_name,**kwgs):
        p,v = list(kwgs.items())[0]
        self.conn.execute("delete from %s where %s='%s'"%(table_name,p,v))
        self.conn.commit()

    def insert(self,table_name,**kwgs):
        def buffer():yield 
        wait_times = buffer()
        sql_buffer = ''
        for _ in wait_times: sql_buffer += "INSERT INTO %s %s VALUES %s;"%( table_name,tuple(kwgs.keys()),tuple(kwgs.values()) )
        self.conn.execute(sql_buffer)
        self.conn.commit()
        self.conn.close()

    def select(self,table_name,**kwgs):
        cnd = kwgs.get('cnd','')
        cnd = ' where ' + ','.join([ '%s="%s"'%(field,val) for field,val in cnd.items()]) if cnd else ''
        fields = kwgs.get('fields','')
        fields = ','.join(fields) if fields else '*'
        sql = "select %s from %s"%(fields,table_name) + cnd
        row = self.conn.execute(sql)        
        ret = [ r for r in row]
        self.conn.close()
        return ret

    def update(self,table_name,**kwgs):
        pass

class DataParse:
    def __init__(self,datafile):
        pass
    def compress_data(self,datafile):
        f = open(datafile,'r',encoding='utf-8')
        ret = f.read()
        f.close()
        return ret
    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(DataParse, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance
    @classmethod
    def write(cls,database,stockid,name,dirs=None):
        op = cls.__new__()
        path = "data/%s/"%stockid if not dirs else dirs
        b = op.compress_data(path+'b.csv')
        p = op.compress_data(path+'p.csv')
        c = op.compress_data(path+'c.csv')
        Dba.op(
            database = database,
            type='i',
            table_name = 'report',
            createtime = time.mktime(datetime.datetime.now().timetuple()),
            stockid = stockid,
            name= name,
            belance = b,
            profit = p,
            cash = c
        )
if __name__=='__main__':
    # ret = Dba.op(database='data/dba.db',type='s',table_name='report')
    # print(ret)
    # Dba.op(database='data/dba.db',type='i',table_name='report',)
    # Dba.op(database='data/dba.db',type='d',table_name='report',stockid="000001")
    # for i in range(4,10):
        # DataParse.write('00000%s'%i)
    ret = Dba.op(database='data/dba.db',type='s',table_name='report',fields=['createtime','name'],cnd={})
    print(ret)