#!/usr/bin/python2.7
#!-*- coding:UTF-8 -*-

import urllib
import re
import json
import math
import time
import logging
import config

#输出日志
def get_log():
    filelog="../log/logger.log"
    logging.basicConfig(filename = filelog, level = logging.DEBUG)
    logging.debug("this is a debug msg!")
#输出遍历文件
def dump_file(stri,i):
    out_file=open("../data/traverse/fund"+str(i)+".txt",'w')
    out_file.write(stri)
    out_file.close()
#输出排序后列表到文件
def sort_file(array,i):
    list_output_file=open("../data/list/"+str(i)+".txt",'w')
    list_output_file.write(str(array))
    list_output_file.close()

#读取时间
def get_time(dict_file):
    var_time=dict_file["begin_time"]
    try:
        time_stamp=time.mktime(time.strptime(var_time,"%Y %m %d %H:%M:%S"))
    except ValueError:
        print "Please enter the correct time format!"
    else:
        return time_stamp
        

#基金网页
def crawl_url_fund(fund_url):
    crawl_information=urllib.urlopen(fund_url)
    crawl_information_read=crawl_information.read()
    get_fund=re.search(r"var r =(.*?);",crawl_information_read)
    list_worth_string=get_fund.group(1)
    list_worth=json.loads(list_worth_string)
    array_forfundnumber=[]
    for i in range(len(list_worth)):
        array_forfundnumber.append(list_worth[i][0])
    dump_file(crawl_information_read,0)
    return array_forfundnumber

#获取时间戳起始位置
def get_time_begin_position(fund_number_list,time):
    fund_number_lastlist=[]
    for i in range(len(fund_number_list)):
        if fund_number_list[i][0]/1000>time:
            fund_number_lastlist.append(fund_number_list[i])
    return fund_number_lastlist

#每个及奖金对应的网页,得到净值数据
def crawl_url_fund_number(fund_number_url,i):
    time.sleep(0.5)
    try:
        crawl_information=urllib.urlopen(fund_number_url)
    except Exception:
        return None
    else:
        crawl_information_read=crawl_information.read()
        dump_file(crawl_information_read,i)
        data_acworthtrend=re.search(r"var Data_ACWorthTrend =(.*?);",crawl_information_read)
        if data_acworthtrend==None:
            return None
        else:
            list_worth_string=data_acworthtrend.group(1)
            list_worth=json.loads(list_worth_string)
            return list_worth

#读取基金网页
def get_fund_url(dict_file):
    fund_url=dict_file["fundcode_search_url"]
    array_forfundnumber=crawl_url_fund(fund_url)
    return array_forfundnumber
#处理基金网页
def fund_number_url_deal(fund_number_url):
    deal_url_array=fund_number_url.split("%")
    return deal_url_array[0]
#读取每个基金对应的网页
def get_fund_number_url(dict_file):
    var_url=dict_file["pingzhongdata_url"]
    fund_number_url_head=fund_number_url_deal(var_url)
    array_forfundnumber=get_fund_url(dict_file)
    time=get_time(dict_file)
    print len(array_forfundnumber)
    for i in range(6160,len(array_forfundnumber)):
        fund_number_url=fund_number_url_head+str(array_forfundnumber[i])+".js"
        list_middle=crawl_url_fund_number(fund_number_url,i)
        if list_middle==None:
            continue
        else:
            print i
            fund_number_lastlist=get_time_begin_position(list_middle,time)
            sort_variance_fund=sort_variance(fund_number_lastlist)
            if sort_variance_fund==None:
                print "time out"
            else:
                sort_file(sort_variance_fund,i)
#获得平均值
def get_avg(fund_number_lastlist):
    sum=0
    if len(fund_number_lastlist)==0:
        return None
    else:
        for i in range(len(fund_number_lastlist)):
            sum+=fund_number_lastlist[i][1]
        avg=sum/len(fund_number_lastlist)
        return avg
#方差排序
def sort_variance(fund_number_lastlist):
    avg=get_avg(fund_number_lastlist)
    if avg==None:
        return None
    else:
        for i in range(1,len(fund_number_lastlist)):
            for j in range(0,len(fund_number_lastlist)-1):
                if math.pow(fund_number_lastlist[j][1]-avg,2)>math.pow(fund_number_lastlist[j+1][1]-avg,2):
                    temp=fund_number_lastlist[j]
                    fund_number_lastlist[j]=fund_number_lastlist[j+1]
                    fund_number_lastlist[j+1]=temp
        return fund_number_lastlist
def main():
    i=0
    get_log()
    conf_position="../conf/config.conf"
    properties=config.Properties()
    dict_file=properties.get_colon_segment_file(conf_position)
    get_fund_number_url(dict_file)
if __name__ == "__main__":
    main()
    
    




    





