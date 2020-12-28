#coding:utf-8
import pdfplumber
import pandas
import re
import os
from split import split_pdf
import time
from config import BALANCE_TABLE,BENEFIT_TABLE,CASH_TABLE

# BALANCE_TABLE = { }
# BENEFIT_TABLE = { }
# CASH_TABLE = { }

class ParsePdf:
    def __init__(self,file_path=[],key_words=[]):
        self.file_path = file_path
        self.pages = []
        self.key_words = key_words
    def __initpdf__(self,file_path):
        return pdfplumber.open(file_path) 
    def get_first_pages_by_keyword(self,key_words=[]):
        key_words = key_words if key_words else self.key_words
        pos = self.quick_indexpage()

        for i in range(pos,pos+30):
            p = self.__initpdf__("temp/%s_result.pdf"%i).pages[0]
            self.pages += [p]
        return pos

    def check_table(self,table,tbs={}):
        i,size = 0,len(table)
        if not tbs:
            return 
        while i<size-1:
            item = table[i]
            name,cur = (item[0],item[2]) if len(item)==4 else (item[0],item[1])
            # name = re.sub(".*：|.*、|（.*）|[\n' '（）：、0-9.]",'',str(name))
            name = re.sub(".*：|.*、|（.*）|[\n' '（）：、0-9.]",'',str(name))
            if name in tbs:
                # print(name,cur)
                i += 1
            else:
                cur_s = ''
                v = 0
                while cur_s not in tbs and i<size-1:
                    v = cur if cur else v
                    if name!='None':
                        cur_s += name.strip(' ').strip('\n')
                        cur_s = cur_s.replace('净亏损以“－”号填列','').replace("损失以“－”号填列",'').replace('损失以“-”号填列','').replace('净亏损以“-”号填列','')
                    # next item
                    item = table[i+1]
                    name,cur = (item[0],item[2]) if len(item)==4 else (item[0],item[1])
                    name = re.sub(".*：|.*、|（.*）|[\n' '（）：、0-9.]",'',str(name))
                    # print('--------->',name)
                    i += 1
                print(i,cur_s,v,size)

    def print_data(self,pos):
        balance_table = []
        benefit_table = []
        cash_table = []
        is_finish = False
        i = 0
        txt = self.pages[i].extract_text()
        while i<29 and not is_finish:
            if '财务报表' in txt and '合并资产负债表' in txt and '编制单位' in txt:
                while True:
                    tbs = self.pages[i].extract_tables()
                    txt = self.pages[i].extract_text()
                    balance_table += tbs[0]
                    if '母公司资产负债表' in txt:
                        break
                    i += 1
            elif '合并利润表' in txt:
                tbs = self.pages[i].extract_tables()
                txt = self.pages[i].extract_text()
                tbs = tbs[1] if tbs[0][-1][0].rfind('负债和所有者')!=-1 else tbs[0]
                while '母公司利润表' not in txt:
                    benefit_table += tbs
                    # next page
                    tbs = self.pages[i+1].extract_tables()[0]
                    txt = self.pages[i+1].extract_text()
                    i += 1
                if str(tbs[-1][0]).rfind('每股收益')!=-1:
                    benefit_table += tbs
            elif '合并现金流量表' in txt:
                tbs = self.pages[i].extract_tables()
                txt = self.pages[i].extract_text()
                tbs = tbs[1] if tbs[0][-1][0].rfind('每股收益')!=-1 else tbs[0]
                while True:
                    # self.check_table(tbs)
                    cash_table += tbs
                    if '母公司现金流量表' in txt:
                        is_finish = True
                        break 
                    # next page
                    tbs = self.pages[i+1].extract_tables()[0]
                    txt = self.pages[i+1].extract_text()
                    i += 1
            else:
                # next page
                txt = self.pages[i+1].extract_text()
                i += 1
            print(pos+i-1,'----------------------------------------')


        # self.check_table(balance_table,tbs = BALANCE_TABLE)
        # print("--------------")
        self.check_table(benefit_table,tbs = BENEFIT_TABLE)
        print("--------------")
        # self.check_table(cash_table,tbs = CASH_TABLE)


    def quick_indexpage(self,file_dirs=None):
        index_page = self.__initpdf__('temp/0_result.pdf')
        for  page in index_page.pages:
            txt = page.extract_text()
            if txt.rfind('目录')==-1 or txt.rfind('.....................................................')==-1:continue
            # print(txt)
            index_list = txt.replace('.','').replace(' ','').split('\n')
            for index in index_list:
                if index.rfind('财务报告')==-1:
                    continue
                if index[-3:].isdigit():
                    return int(index[-3:])
                elif index[-2:].isdigit():
                    return int(index[-2:])
                elif index[-1:].isdigit():
                    return int(index[-1:])
                else:
                    return 0
        index_page.close()


if __name__=='__main__':

    start=time.time()
    test_file = "resource/aaa.pdf"
    split_pdf(test_file)
    parse = ParsePdf(test_file)
    page = parse.get_first_pages_by_keyword()
    parse.print_data(page)
    end=time.time()
    print('Running time: %s Seconds'%(end-start))