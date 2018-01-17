# Hupu_Spider

1.功能:爬取虎扑社区图片并保存到本地

2.文件 '爆照区' 和 '这妹子真漂亮' 中为该程序爬取的少量图片

3.程序包含Spider_Hupu.py和Run_Hupu.py  我的运行环境是 windows10 64位 以及 python3.6

4.可以爬取的版块见 Spider_Hupu.py中 
	CONFIG_DICT = {
                   '爆照区':'selfie',
                   '这妹子真漂亮':'beauty',
                   '步行街主干道':'bxj',
                   '马刺专区':'spurs',
                   '破瓜区':'pogua',
                   'Ma酱馆':'masamimarryme',
                   '迪丽热巴':'Dilraba',
               	  }

    可自己添加版块名称 至 CONFIG_DICT 中 ,字典的value为版块url末尾的字母.

5.图片的保存路径可在Spider_Hupu中修改 dir 变量

6.需要安装的python库有:
	 requests
	 re
	 os
	 hashlib
	 bs4
	 lxml
	 multiprocessing

7.使用方法
	
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


    可修改需要爬取的页数,如:urls = spider.get_index_urls(1,3) , 可获取1到3页的贴子图片

    运行Run_Hupu.py,输入版块名称即可
    


