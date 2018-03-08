#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import urllib
import re
import json
import math
import time
import logging
import config
import threading

def get_log():
    '''
    输出日志到../log/logger.log文件
    '''
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../log/logger.log',
                filemode='w')


def dump_file(stri,i):
    '''
    创建文件按顺序将遍历到的文件输入到文件中
    '''
    out_file=open("../data/traverse/fund"+str(i)+".txt",'w')
    out_file.write(stri)
    out_file.close()



def sort_file(sort_fund):
    '''
    对信息排完序后将其输入到文件中
    '''
    output_file=open("../data/list/sort.utf8",'w')
    output_file.write(json.dumps(sort_fund, ensure_ascii=False))
    output_file.close()


def crawl_url_fund(fund_name_list,fund_url):
    '''
    访问基金总网页，并返回每个基金对应的序号
    '''
    crawl_information=urllib.urlopen(fund_url)
    crawl_information_read=crawl_information.read()
    get_fund=re.search(r"var r =(.*?);",crawl_information_read)
    list_worth_string=get_fund.group(1)
    list_worth=json.loads(list_worth_string)
    array_forfundnumber=[]
    for i in range(len(list_worth)):
        fund_name_list.append(list_worth[i][2])
        array_forfundnumber.append(list_worth[i][0])
    dump_file(crawl_information_read,0)
    return array_forfundnumber


def crawl_url_fund_number(ThreadName,fund_number_url_list,fund_name_list,array_forfundnumber,fund_list,time_begin):
    '''
    访问每个基金对应的网页找到净值数据返回
    如果网页为空返回空
    '''
    for i in range(len(fund_number_url_list)):
        time.sleep(0.01)
        try:
            crawl_information=urllib.urlopen(fund_number_url_list[i])
        except Exception:
            continue
        else:
            get_log()
            logging.debug("\""+ThreadName+"\":success")
            crawl_information_read=crawl_information.read()
            dump_file(crawl_information_read,i)
            data_acworthtrend=re.search(r"var Data_ACWorthTrend =(.*?);",crawl_information_read)
            if data_acworthtrend==None:
                continue
            else:
                list_worth_string=data_acworthtrend.group(1)
                list_worth=json.loads(list_worth_string)
            
                if list_worth==None:
                    continue
                else:
                    fund_number_lastlist=get_time_begin_position(list_worth,time_begin)
                    if fund_number_lastlist==None or fund_number_lastlist==[] :
                        continue
                    else:
                        fund_variance=get_variance(fund_number_lastlist)
                        everyfund_list=[array_forfundnumber[i],fund_name_list[i],fund_variance]
                        fund_list.append(everyfund_list)



def get_fund_url(dict_file,fund_name_list):
    '''
    读取配置信息中总基金网页地址
    '''
    fund_url=dict_file["fundcode_search_url"]
    array_forfundnumber=crawl_url_fund(fund_name_list,fund_url)
    return array_forfundnumber


def fund_number_url_deal(fund_number_url):
    '''
    处理基金信号对应地址找出公有部分
    '''
    deal_url_array=fund_number_url.split("%")
    return deal_url_array[0]


def start_thread(fund_number_url_array1,fund_number_url_array2,fund_number_url_array3,fund_name_list1,fund_name_list2,fund_name_list3,time_begin,array_forfundnumber1,array_forfundnumber2,array_forfundnumber3,fund_list):
    '''
    创建线程并启动
    '''
    thread_forfund1=threading.Thread(target=crawl_url_fund_number,args=("Thread-1",fund_number_url_array1,fund_name_list1,array_forfundnumber1,fund_list,time_begin))
    thread_forfund2=threading.Thread(target=crawl_url_fund_number,args=("Thread-2",fund_number_url_array2,fund_name_list2,array_forfundnumber2,fund_list,time_begin))
    thread_forfund3=threading.Thread(target=crawl_url_fund_number,args=("Thread-3",fund_number_url_array3,fund_name_list3,array_forfundnumber3,fund_list,time_begin))
    thread_forfund1.start()
    thread_forfund2.start()
    thread_forfund3.start()
    thread_forfund1.join()
    thread_forfund2.join() 
    thread_forfund3.join()    


def get_fund_number_url(dict_file,fund_list):
    '''
    将每个基金对应的网页均分到两个列表中
    '''
    fund_name_list=[]
    var_url=dict_file["pingzhongdata_url"]
    fund_number_url_head=fund_number_url_deal(var_url)
    array_forfundnumber=get_fund_url(dict_file,fund_name_list)
    time_begin=get_time(dict_file)
    print len(array_forfundnumber)
    fund_number_url_array1=[]
    fund_number_url_array2=[]
    fund_number_url_array3=[]
    fund_name_list1=[]
    fund_name_list2=[]
    fund_name_list3=[]
    array_forfundnumber1=[]
    array_forfundnumber2=[]
    array_forfundnumber3=[]
    for i in range(len(array_forfundnumber)):
        fund_number_url=fund_number_url_head+str(array_forfundnumber[i])+".js"
        if i%3==0:
            fund_name_list1.append(fund_name_list[i])
            fund_number_url_array1.append(fund_number_url)
            array_forfundnumber1.append(array_forfundnumber[i])
        elif i%3==1:
            fund_name_list2.append(fund_name_list[i])
            fund_number_url_array2.append(fund_number_url)
            array_forfundnumber2.append(array_forfundnumber[i])
        elif i%3==2:
            fund_name_list3.append(fund_name_list[i])
            fund_number_url_array3.append(fund_number_url)
            array_forfundnumber3.append(array_forfundnumber[i])
    start_thread(fund_number_url_array1,fund_number_url_array2,fund_number_url_array3,fund_name_list1,fund_name_list2,fund_name_list3,time_begin,array_forfundnumber1,array_forfundnumber2,array_forfundnumber3,fund_list)


def get_time(dict_file):
    '''
    读取配置文件中的时间要求，并返回
    '''
    var_time=dict_file["begin_time"]
    try:
        time_stamp=time.mktime(time.strptime(var_time,"%Y %m %d %H:%M:%S"))
    except ValueError:
        print "Please enter the correct time format!"
    else:
        return time_stamp



def get_time_begin_position(fund_number_list,time):
    '''
    得到净值数据中时间戳的起始位置
    '''
    fund_number_lastlist=[]
    for i in range(len(fund_number_list)):
        if fund_number_list[i][0]/1000>time:
            fund_number_lastlist.append(fund_number_list[i])
    return fund_number_lastlist



def get_avg(fund_number_lastlist):
    '''
    获得数据平均值
    '''
    sum=0
    if len(fund_number_lastlist)==0:
        return None
    else:
        for i in range(len(fund_number_lastlist)):
            sum+=fund_number_lastlist[i][1]
        avg=sum/len(fund_number_lastlist)
        return avg


def get_variance(fund_number_lastlist):
    '''
    获得净值数据的方差
    '''
    avg_number=get_avg(fund_number_lastlist)
    sum=0
    fund_variance_sum=0
    for i in range(len(fund_number_lastlist)):
        fund_variance_sum+=math.pow(fund_number_lastlist[i][1]-avg_number,2)
        sum+=1
    fund_variance=fund_variance_sum/sum
    return fund_variance


def sort_variance(fund_list):
    '''
    对数据按方差排序
    '''
    for i in range(1,len(fund_list)):
        for j in range(0,len(fund_list)-1):
            if fund_list[j][2]>fund_list[j+1][2]:
                temp=fund_list[j]
                fund_list[j]=fund_list[j+1]
                fund_list[j+1]=temp
    return fund_list


def change_ascii(sort_fund_list):
    '''
    改变列表中字符串的ascii格式
    '''
    sort_fund=[]
    for i in range(len(sort_fund_list)):
        sort_everyfund=[]
        for j in range(2):
            sort_everyfund.append(sort_fund_list[i][j].encode("utf-8"))
        sort_everyfund.append(sort_fund_list[i][2])
        sort_fund.append(sort_everyfund)
    return sort_fund


def main():
    conf_position="../conf/config.conf"
    properties=config.Properties()
    fund_list=[]
    dict_file=properties.get_colon_segment_file(conf_position)
    get_fund_number_url(dict_file,fund_list)
    sort_fund_list=sort_variance(fund_list)
    sort_fund=json.dumps(sort_fund_list, encoding="UTF-8", ensure_ascii=False)
    print sort_fund
    sort_fund=change_ascii(sort_fund_list)
    sort_file(sort_fund)


if __name__ == "__main__":
    main()
    
    




    





