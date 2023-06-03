'''
Author: Howv.John.Young
Date: 2023-06-01 11:00:42
LastEditTime: 2023-06-02 21:15:09
LastEditors: Howv.John.Young
Description: 
FilePath: \pythontest\main.py
可以输入预定的版权声明、个性签名、空行等
'''
from comicDL import comicDL_init
from comicDL.title_get import title_get
from comicDL.chapter_get import chapter_get_json
from comicDL.file_manage import file_create
from comicDL.downloader import downloader
from comicDL.parser import parser
import config
import comicDL.file_manage as fm

from urllib.parse import urljoin
import os
import sys
import threading
import queue


#未初始化的全局变量
'''
download_path = ""
book_path = ""
book_name = ""
book_code = ""
downloader_threads_num = 1
parser_threas_num = 1
domainUrl = ""
book_link = ""
'''




class tdownloaders(threading.Thread):
    def __init__(self, qimgs:queue.Queue):
        threading.Thread.__init__(self)
        self.qimgs = qimgs
    def run(self):
        downloader(self.qimgs)


class tparsers(threading.Thread):
    def __init__(self, qChapter:queue.Queue, qImgList:queue.Queue):
        threading.Thread.__init__(self)
        self.qChapter = qChapter
        self.qImgList = qImgList
    def run(self):
        parser(self.qChapter, self.qImgList)



def init()->int:
    #声明全局变量
    global download_path
    global book_path
    global book_name
    global book_code
    global downloader_threads_num
    global parser_threads_num
    global domainUrl
    global book_link
    
    #config init
    if config.init() != 0:
        return -1
    #模块init，必须在config init后执行
    comicDL_init(config.DOMAIN_URL, \
                config.SCRIPT_PATH, \
                config.SEARCH_URL, \
                config.PARSER_WAIT_TIME, \
                config.DOWNLOAD_GAP_TIME, \
                config.DOWNLOAD_RETRY_TIMES )
    #初始化赋值
    book = title_get()
    if(book == None):
        return -1
    book_name = book["title"]
    book_code = book["link_code"]
    book_link = urljoin(config.DOMAIN_URL,book_code)+"/"
    downloader_threads_num = config.DOWNLOADER_THREADS_NUM
    parser_threads_num = config.PARSER_THREADS_NUM
    domainUrl = config.DOMAIN_URL

    download_path = config.DOWNLOAD_PATH
    book_path = os.path.join(download_path, book_name)
    return 0

def main()->int:
    #初始化，搜索
    if init() != 0:
        print("初始化错误")
        return -1
    clist = chapter_get_json(book_link)
    if clist == None:
        print("章节获取错误")
        return -1

    #创建下载线程,并启用
    qImgUrls = queue.Queue()    #downloader用于  @@接收待下载图片url@@  的消息队列
    downloader_threads = []
    for j in range(downloader_threads_num):
        t = tdownloaders(qImgUrls)
        t.start()
        downloader_threads.append(t)
    #创建解析线程，并启用
    parser_threads = []
    qChapter = queue.Queue()    #parser用于  @@接受待解析章节url@@  的消息队列
    qImgList = queue.Queue()    #parser用于  @@发送解析得到的章节图片url列表@@  的消息队列
    for j in range(parser_threads_num):
        t = tparsers(qChapter, qImgList)
        t.start()
        parser_threads.append(t)


    #创建文件夹
    num = 0
    chapterInfoList = []
    file_create(download_path)
    file_create(book_path)
    for i in clist:
        num += 1
        #生成章节目录
        chapterName = str(i["chapterName"])
        #消除win路径不可用特殊字符，均使用下划线代替
        chapterName = chapterName.replace('?','_')
        chapterName = chapterName.replace('"','_')
        chapterName = chapterName.replace('\'','_')
        chapterName = chapterName.replace('*','_')
        chapterName = chapterName.replace('<','_')
        chapterName = chapterName.replace('>','_')
        chapterName = chapterName.replace('\\','_')
        chapterName = chapterName.replace('/','_')
        chapterName = chapterName.replace('|','_')
        chapterName = chapterName.replace(' ','_')
        chapterName = chapterName.replace(':','_')
        chapterInfoList.append({"chapterName" : "{:0>4d}".format(num)+"."+ chapterName,\
                                "chapterPath" : os.path.join(book_path, \
                                                "{:0>4d}".format(num)+"."+ chapterName),\
                                "chapterLink" : i["chapterUrl"]})
    #创建作品索引
    fm.book_index_create(book_path,book_link,chapterInfoList)
    for i in chapterInfoList:
        #创建章节文件夹
        file_create(i["chapterPath"])
        #送入消息队列
        chapter = {
            "chapterName" : i["chapterName"],
            "chapterLink" : i["chapterLink"]
        }
        qChapter.put(chapter)
    #紧随其后，在正常内容发送完，创建并发送parser线程终结信息
    chapter = {
        "chapterName" : None,
        "chapterLink" : None
    }
    for i in range(parser_threads_num):
        qChapter.put(chapter)


    #接受parser返回结果
    parser_nums = parser_threads_num
    while parser_nums > 0:
        imgList = qImgList.get()
        if imgList["chapterName"] == None:
            parser_nums -= 1
            continue
        #创建章节索引
        fm.chapter_index_create(book_path, book_link, imgList["chapterName"], \
                                    imgList["chapterLink"], imgList["imgs"])
        msg = {
            "enable" : 1,
            "downloadPath" : os.path.join(book_path, imgList["chapterName"]),
            "chapterName" : imgList["chapterName"],
            "imgUrls" : imgList["imgs"] 
        }
        #每接受一个parser返回的urllist后就向downloader发送一个下载任务
        #当所有parser返回都转发完后，downloader任务也告知完毕
        qImgUrls.put(msg)
    #紧随其后，发送downloader任务完成消息
    #创建downloader线程终结信息
    msg0 = {
        "enable" : 0,
        "downloadPath" : "",
        "chapterName" : "",
        "imgUrls" : []
    }
    for i in range(downloader_threads_num):
        qImgUrls.put(msg0)


    #结束线程
    for j in parser_threads:
        j.join()
    for j in downloader_threads:
        j.join()
    return 0


if __name__ == "__main__":
    sys.exit(main())
