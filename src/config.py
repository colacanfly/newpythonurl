#!/usr/bin/python2.7
#-*- coding:UTF-8 -*-

class Properties:
    def get_colon_segment_file(self,input_file):
        get_file=open(input_file,'r')
        lines=get_file.readlines()
        list_forfile=[]
        for line in lines:
            try:
                list_line=line.strip('\n').split(" : ",1)
            except Exception:
                print "配置文件错误"
            else:
                list_forfile.append(list_line)
        dict_file=dict(list_forfile)
        return dict_file
