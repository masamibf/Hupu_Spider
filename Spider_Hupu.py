#!/usr/bin/env python  
# encoding: utf-8  

""" 
@author: @长泽雅美男友
@contact: 374454765@qq.com 
@file: Spider_Hupu.py 
@time: 2018/1/11 20:24 
"""

import requests
from requests.exceptions import RequestException
import re
import os
from hashlib import md5
from bs4 import BeautifulSoup

CONFIG_DICT = {
                   '爆照区':'selfie',
                   '这妹子真漂亮':'beauty',
                   '步行街主干道':'bxj',
                   '马刺专区':'spurs',
                   '破瓜区':'pogua',
                   'Ma酱馆':'masamimarryme',
                   '迪丽热巴':'Dilraba',

               }

class Spider_Hupu():

    def __init__(self,community):
        self.session = requests.session()
        self.community = community              #社区名称

    def get_index_urls(self,start_index,end_index):
        """获取指定社区的索引页链接"""
        urls = []
        cnts = [cnt for cnt in range(start_index, end_index + 1, 1)]
        for i in cnts:
            url = 'https://bbs.hupu.com/' + self.community + '-' + str(i)
            urls.append(url)
        return urls

    def get_html(self,link):
        """获取网页源代码"""
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer':'https://bbs.hupu.com/',
            'Cookie':'_dacevid3=f2768d87.c2ea.bd0f.3aa6.65c6cd7601ee; __dacevst=f7814401.814d7f26|1515989710077; _HUPUSSOID=04b4155c-c968-4af5-b776-a180bbb89540; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=31096195|6ZW/5rO96ZuF576O55S35Y+L|4a7f|ddc068e803fcfcfe30218821f5e0463d|03fcfcfe30218821|aHVwdV8yZDRmMmUyZmZkYzk4ZGRi; us=c5efb32fa9b2fc29b7fbf59d51b22fe0f3e7c4fc901f7607470f7d6c8007785fd7583c534e2d10653b0570a361cbad46d97031dc73a2b3d1671421936135f429; ua=15791537; _cnzz_CV30020080=buzi_cookie%7Cf2768d87.c2ea.bd0f.3aa6.65c6cd7601ee%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1515987645; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1515987910; __gads=ID=93d0b7e08ab4f9c6:T=1515987646:S=ALNI_Mafo9adqg17okWqS55xWlSF-BYitg; PHPSESSID=36dd7695985bee3528fd8cdb8ab2c476; _fmdata=4E4734B88C1B882C12BA46110118A593D67338BF76EED181FCADBFEC7D831367FA2599D096EE9C802EA096A37AC7EC197DD35772CE3BE30B'
        }
        try:
            response = self.session.get(link,headers = headers)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            print("请求页面失败")
            return None

    def parse_index_html(self,html):
        # 解析索引页 返回详情页链接
        link_ahead = 'https://bbs.hupu.com'
        soup = BeautifulSoup(html, 'lxml')
        data = soup.select('div.titlelink.box > a')
        for i in data[1:]:
            link = i.get('href')
            link = link_ahead + link
            yield link

    def parse_page_html(self,page_html):
        """解析详情页 下载图片并保存"""
        imgs = []
        name = re.findall(r'<title>\n.*? - (.*?) - 虎扑社区\n</title>',page_html,re.S)[0]     #板块名称 作为文件夹名称
        title = re.findall(r'data-title="(.*?)" tid', page_html)[0]                          #帖子标题 作为子文件夹名称
        img = re.findall(r'https://i(.*?).hoopchina.com.cn/(.*?)\?x-oss', page_html)         #图片链接
        for i, j in img:
            img = "https://i" + i + ".hoopchina.com.cn/" + j
            imgs.append(img)
            imgs = list(set(imgs))  # 去重
        for img_link in imgs:
            self.download_image(name,title,img_link)

    def download_image(self,name,title,link):
        """请求图片链接 并下载"""
        try:
            response = self.session.get(link)
            if response.status_code == 200:
                formats = link.split('.')[-1]  # 获取文件格式
                self.save_image(name,title,response.content, formats)
            return None
        except RequestException:
            print('请求图片失败')

    def save_image(self,name,title, content,formats):
        """保存图片   文件夹名称,子文件名称,图片数据,图片格式"""
        dir_name = 'D:\我的python程序\★爬虫练习\★虎扑图片\\' + name + '\\' + title
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)  # 如果不存在则新建文件夹
        img_path = os.path.join(dir_name, "%s.%s" % (md5(content).hexdigest(), formats))
        if not os.path.exists(img_path):
            print('正在保存图片--- ' + img_path)
            with open(img_path, 'wb') as f:
                f.write(content)
                f.close()

    def main(self,url):
        """主函数"""
        index_html = self.get_html(url)
        for link in self.parse_index_html(index_html):
            page_html = self.get_html(link)
            if page_html:
                self.parse_page_html(page_html)

