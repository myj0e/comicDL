'''
Author: Howv.John.Young
Date: 2023-06-02 17:43:18
LastEditTime: 2023-06-02 20:00:56
LastEditors: Howv.John.Young
Description: 
FilePath: \pythontest\comicDL\parser.py
可以输入预定的版权声明、个性签名、空行等
'''
import queue
import time
from bs4 import BeautifulSoup
from selenium import webdriver

#未初始化的全局变量
'''
script_path = ""
wait_time = ""
'''

def parser_init(scriptPath:str, paserWaitTime:float):
    global script_path
    global wait_time 
    wait_time = paserWaitTime
    script_path = scriptPath

def getImgList(chapterName:str, url:str)->list:
    try:
        driver=webdriver.Firefox(executable_path= script_path)
        #窗口最小化
        driver.minimize_window()
        driver.get(url)
    except:
        print("{}页面获取失败...".format(chapterName))
        return None
    #预留加载时间
    time.sleep(wait_time)
    #将页面拉到底
    js = "window.scrollTo(0,document.body.scrollHeight)"    #2
    driver.execute_script(js)
    #解析动态加载完的页面内容
    soup = BeautifulSoup(driver.page_source, "html.parser")
    images = soup.find_all("img", class_="loaded lazy")
    #采集所有图片
    urls = []
    for image in images:
        url = image["data-src"]
        urls.append(url)
    driver.close()
    return urls


'''
chapter = 
{
    "chapterName" : "001.firstChapter",
    "chapterLink" : "http://test.demo.com/demo/123adf.html"
}
'''

'''
ImgList = 
{
    "chapterName" : "001.firstChapter",
    "chapterLink" : "http://test.demo.com/demo/123adf.html",
    "imgs" : [
        "http://img.com/sdfdsaf.jpg",
        "http://img.com/faggdfs.jpg",
    ]
}
'''
def parser(qChapter:queue.Queue, qImgList:queue.Queue):
    while True:
        #创建初始imgList包
        imgList = {
            "chapterName" : "",
            "chapterLink" : "",
            "imgs" : []
        }
        #接受qChapter信息
        chapter = qChapter.get()
        #若收到中止包（chapterName是None）则向qImgList中发送中止反馈并跳出循环
        if chapter["chapterName"] == None:
            imgList["chapterName"] = None
            imgList["chapterLink"] = None
            imgList["imgs"] = None
            qImgList.put(imgList)
            print("parser over...")
            break
        #若收到包为正常包，则处理
        urlList = getImgList(chapter["chapterName"], chapter["chapterLink"])
        if urlList == None:
            continue
        imgList["chapterName"] = chapter["chapterName"]
        imgList["chapterLink"] = chapter["chapterLink"]
        imgList["imgs"] = urlList
        qImgList.put(imgList)
    return 0



