import json
from database.read_byurl import SpiderUrl
from database.DBA import Dba,DataParse
from config import DATABASE,DEFAULT_YEARS,DATAOBJ

def load_info():
    f = open(DATAOBJ,'r',encoding='utf-8')
    obj = f.read()
    f.close()
    return json.loads(obj)
class DataSource(SpiderUrl):
    info = load_info()
    def __init__(self,url=None,stock_code=None,years=None):
        super().__init__(url,stock_code,years)
    @classmethod
    # @override
    def gen_data_bytype(cls,stock_code,type=None,years=None):
        ret = Dba.op(database= DATABASE,type='s',table_name='report',fields=[],cnd={'stockid':stock_code})
        if not ret:
            b = super().gen_data_bytype(stock_code,'b',years)
            p = super().gen_data_bytype(stock_code,'p',years)
            c = super().gen_data_bytype(stock_code,'c',years)
            b.to_csv('temp/b.csv',sep=',',index=True,encoding='utf-8')
            p.to_csv('temp/p.csv',sep=',',index=True,encoding='utf-8')
            c.to_csv('temp/c.csv',sep=',',index=True,encoding='utf-8')
            DataParse.write( DATABASE,stock_code,cls.info[stock_code],dirs='temp/')
            ret = Dba.op(database= DATABASE,type='s',table_name='report',fields=[],cnd={'stockid':stock_code})
        return ret[0] if ret else -1
if __name__=='__main__':
    ret = DataSource.gen_data_bytype('601869')
    print(ret)
    # batch insert
    # obj = DataSource.info
    # for id,name in obj.items():
        # print(id,name)
        # DataParse.write(DATABASE,id,name,dirs='database/data/%s/'%id)
