#!/usr/bin/env python  
# encoding: utf-8  

""" 
@author: @长泽雅美男友
@contact: 374454765@qq.com 
@file: Run_Hupu.py
@time: 2018/1/11 20:49 
"""
from Spider_Hupu import Spider_Hupu,CONFIG_DICT
from multiprocessing import Pool

if __name__ == '__main__':
    community = input('请 输 入 板 块 名 称: ')

    if community in CONFIG_DICT.keys():
        spider = Spider_Hupu(CONFIG_DICT.get(community))    #实例化对象
        urls = spider.get_index_urls(1,3)                   #获取板块索引页url
        p = Pool()                                          #进程池
        p.map_async(spider.main,urls)
        p.close()
        p.join()

    else:
        print('----------请  您  重  新  输  入----------')
