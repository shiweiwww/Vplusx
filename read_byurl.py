#coding:utf-8
import requests
import pandas as pd

class SpiderUrl:
    def __init__(self,url=None,stock_code=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Cookie':"UOR=www.baidu.com,finance.sina.com.cn,; SINAGLOBAL=123.117.176.248_1602391648.642016; Apache=123.117.176.248_1602391648.642017; UM_distinctid=17515fc2c7c160-014d90c5914974-c781f38-240000-17515fc2c7d508; lxlrttp=1578733570; ULV=1602478419209:2:2:2:123.117.176.248_1602391648.642017:1602391646758; __gads=ID=0da06223e7f65877-221c3df411c400e3:T=1602663993:RT=1602663993:S=ALNI_MYB4lvzxRo9BizTf6tEXyHwuxd2vg; U_TRS1=000000f8.affced6c.5f86b7c2.dc280116; U_TRS2=000000f8.b004ed6c.5f86b7c2.e9fe1804; vjuids=-112041c01.17550984b8e.0.4f411e2b74902; vjlast=1603374960.1603374960.30; _ga=GA1.3.1656219609.1603552931; Qs_lvt_335601=1603699124; Qs_pv_335601=467004930034088700; ULOGIN_IMG=tc-a83b37bd75b943bb920f972f65441fc44f5e; SCF=AisvVkKbeKlGWv5NNcrrF4qkqwvt5LXTiUaaqb4f-tfvbXuvSM7hsqSVSdsk19EQnPrjZspdhjsyAW6DXRry3jY.; sso_info=v02m6alo5qztKWRk6ClkKOApZCTiKWRk5SlkJOgpY6DkKWRk5ClkKOgpY6DnZ-atqm6m5aUpp2WpaSPk5i0jZOQtYyzpLOMo6DA; SessionID=tqnoo5ulqs1no5h4542pq84120; SGUID=1608540596057_66363841; MONEY-FINANCE-SINA-COM-CN-WEB5=; FIN_ALL_VISITED=sh601012; SR_SEL=1_511; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWwH7WzgZS-MvE0fzzzFNjL5NHD95QcSh-XSKe4e0zRWs4Dqcjyi--Ri-z7i-2Ei--fi-2RiKnXi--Xi-zRiKnNPc_3wJfL; ALF=1640517434; FINA_V_S_2=sz000895,sh601012; SUB=_2A25y42w2DeRhGeBK7lYU8yfPyTSIHXVRmdr-rDV_PUJbm9AKLXimkW9NR7qdYk42y8td_28VkQvSLLqTsU4K7g-H; _s_upa=34",
        }
        self.stock_code = stock_code
        self.belance_url = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/%s/ctrl/all.phtml"%stock_code
        self.benefit_url = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/%s/ctrl/all.phtml"%stock_code 
        self.cash_url = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/%s/ctrl/all.phtml"%stock_code
        self.years = ["20141231","20151231","20161231","20171231","20181231","20191231"]

    def get_from_url(self,url=None):
        self.req = requests.get(url,headers=self.headers)
        data = self.req.content
        return data
    def filter_by_years(self,data,years=None):
        years = self.years if not years else years
        dt = str(data, encoding = "gbk").split('\n')
        index = []
        cols = []
        values = []
        for i,line in enumerate(dt):
            it = line.split('\t')
            if len(it)<5:
                continue
            if i<=1:
                cols = it[1:] if not cols else cols
            else:
                index += [it[0]]
                values += [it[1:]]
        ret = pd.DataFrame(values,index=index,columns=cols)
        return ret.loc[:,years]
    # return type：DataFrame
    def get_belance(self):
        data = self.get_from_url(self.belance_url)
        data = self.filter_by_years(data)
        return data

    # return type：DataFrame
    def get_benefit(self):
        data = self.get_from_url(self.benefit_url)
        data = self.filter_by_years(data)
        return data

    # return type：DataFrame
    def get_cash(self):
        data = self.get_from_url(self.cash_url)
        data = self.filter_by_years(data)
        # print(data.head())
        return data
    @classmethod
    def gen_data_bytype(cls,stock_code,type=None):
        obj = cls(url=None,stock_code=stock_code)
        if type=='b':
            return obj.get_belance()
        elif type=='p':
            return obj.get_benefit()
        elif type=='c':
            return obj.get_cash()
        else:
            try:
                raise 'type must is in (b=belance,p=profit,c=cash)'
            except:
                pass
if __name__=="__main__":
    b = SpiderUrl.gen_data_bytype('000895',type='b')
    p = SpiderUrl.gen_data_bytype('000895',type='p')
    c = SpiderUrl.gen_data_bytype('000895',type='d')
    print(b.head())
    print(p.head())
    print(c.head())