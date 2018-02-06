#!/usr/bin/python2.7
#!-*- coding:UTF-8 -*-

import urllib
import re
import json
import math
import time
import logging


#输出日志
def get_log():
    filelog="../log/logger.log"
    logging.basicConfig(filename = filelog, level = logging.DEBUG)
    logging.debug("this is a debug msg!")
#输出文件
def dump_file(stri,i):
    out_file=open("../data/fund"+str(i)+".txt",'w')
    out_file.write(stri)
    out_file.close()

#读取配置文件
def extract_file(stri):
    open_file=open(stri)
    open_file_read=open_file.read()
    #print open_file_read
    return open_file_read

#读取时间
def get_time(stri):
    var=re.search(r"begin_time: (.*?);",stri)
    time_var=var.group(1)
    try:
        time_stamp=time.mktime(time.strptime(time_var,"%Y %m %d %H:%M:%S"))
    except ValueError:
        print "Please enter the correct time format!"
    else:
        return time_stamp
        

#爬取基金网页
def crawl_url_fund(str1):
    crawl_information=urllib.urlopen(str1)
    crawl_information_read=crawl_information.read()
    var=re.search(r"var r =(.*?);",crawl_information_read)
    list_worth_string=var.group(1)
    list_worth=json.loads(list_worth_string)
    array=[]
    for i in range(len(list_worth)):
        array.append(list_worth[i][0])
    arraylist=array
    dump_file(crawl_information_read,0)
    return arraylist

#获取时间戳起始位置
def get_time_begin_position(forlist,time):
    array=[]
    for i in range(len(forlist)):
        if forlist[i][0]/1000>time:
            array.append(forlist[i])
    return array

#爬取每个及奖金对应的网页,得到净值数据
def crawl_url_fund_number(str1,i):
    try:
        crawl_information=urllib.urlopen(str1)
    except Exception:
        return None
    else:
        crawl_information_read=crawl_information.read()
        dump_file(crawl_information_read,i+1)
        var=re.search(r"var Data_ACWorthTrend =(.*?);",crawl_information_read)
        if var==None:
            return None
        else:
            list_worth_string=var.group(1)
            list_worth=json.loads(list_worth_string)
            return list_worth

#读取基金网页
def get_fund_url(str1):
    var=re.search(r"fundcode_search_url: (.*?);",str1)
    fund_url=var.group(1)
    array=crawl_url_fund(fund_url)
    return array
#读取每个基金对应的网页
def get_fund_number_url(str1):
    open_file=extract_file(str1)
    var=re.search(r"pingzhongdata_url: (.*?)%s",open_file)
    array=get_fund_url(open_file)
    time=get_time(open_file)
    last_type=".js"
    for i in range(len(array)):
        fund_number_url=var.group(1)+str(array[i])+".js"
        list_middle=crawl_url_fund_number(fund_number_url,i)
        if list_middle==None:
            continue
        else:
            last_list=[]
            last_list=get_time_begin_position(list_middle,time)
            sort_variance(last_list)
#获得平均值
def get_avg(forlist):
    sum=0
    for i in range(len(forlist)):
        sum+=forlist[i][1]
    avg=sum/len(forlist)
    return avg
#方差排序
def sort_variance(forlist):
    avg=get_avg(forlist)
    for i in range(1,len(forlist)):
        for j in range(0,len(forlist)-1):
            if math.pow(forlist[j][1]-avg,2)>math.pow(forlist[j+1][1]-avg,2):
                forlist[j],forlist[j+1]=forlist[j+1],forlist[j]
def main():
    i=0
    get_log()
    conf_position="../conf/config.conf"
    get_fund_number_url(conf_position)
if __name__ == "__main__":
    main()
    
    




    





