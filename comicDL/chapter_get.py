'''
Author: Howv.John.Young
Date: 2023-06-01 11:44:59
LastEditTime: 2023-06-02 21:10:12
LastEditors: Howv.John.Young
Description: 
FilePath: \pythontest\comicDL\chapter_get.py
可以输入预定的版权声明、个性签名、空行等
'''
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin

import time

#未初始化的全局变量
'''
url = ""
script_path = ""
'''


def chapter_get_init(baseUrl:str, scriptPath:str):
    global url
    global script_path
    url = baseUrl
    script_path = scriptPath


def chapter_get_json(book_url:str)->list:
    #使用selenium生成完整的html内容
    driver = webdriver.Firefox(executable_path= script_path)
    #窗口最小化
    driver.minimize_window()
    print("访问 "+ book_url)
    driver.get(book_url)
    print(" <加载页面 1/4> ", end="")

   
    #若存在 <div class="moreChapter"，则加载更多
    soup = BeautifulSoup(driver.page_source, "html.parser")
    moreChapter = soup.find("div", class_="moreChapter")
    if moreChapter != None:
        #触发更多章节查看全部
        js = "charpterMore(this);"
        driver.execute_script(js)
    #预留加载时间
    print(" <执行js 2/4> ", end="")
    time.sleep(3)
    print(" <html解析 3/4> ", end="")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    list = soup.find("div", id = "chapter-list1")
    chapters = list.find_all("a")
    clist = []
    for i in chapters:
        chaptertmp = {
            "chapterName" : i.string,
            "chapterUrl" : urljoin(url, i["href"])
        }
        clist.append(chaptertmp)
    driver.close()
    print("<解析完成 4/4>")
    return clist[::-1]
