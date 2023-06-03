'''
Author: Howv.John.Young
Date: 2023-06-01 12:19:22
LastEditTime: 2023-06-02 21:08:52
LastEditors: Howv.John.Young
Description: 
FilePath: \pythontest\comicDL\title_get.py
可以输入预定的版权声明、个性签名、空行等
'''
import requests
from bs4 import BeautifulSoup

#未初始化的全局变量
'''
search_url = ""
'''



def title_get_init(searchUrl:str):
    global search_url
    search_url = searchUrl

def title_get()->list:

    while True:
        user_input_title = ""
        while user_input_title == "":
            user_input_title = input("请输入漫画名，关键词(勿带书名号等符号)：")
        try:
            r = requests.get(url=search_url+user_input_title)
        except ConnectionError:
            print("漫画名获取网络错误...")
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        books = soup.find("div", class_="bookList_3")
        booklist = books.find_all('div', class_='item ib')
        titles = []
        for i in booklist:
            titles.append({"link_code":i.p.a["href"].strip("/"),"title":i.p.a["title"]})
        #若未能检索到相关作品，返回搜索框
        if titles != []:
            break
        else:
            print("未能检索到相关作品")
    index_offset1 = 1
    print("搜索到以下漫画：")
    print("---------------------------------")
    for i in titles:
        print("|  ",end="")
        print(str(index_offset1)+"." + i["title"])
        index_offset1 += 1
    print("---------------------------------")
    
    #输入检测
    while True:
        offset_str = input("请输入对应标号：")
        try:
            offset = int(offset_str) - 1
        except ValueError:
            print("输入错误请重新输入")
        else:
            if offset >= 0 and offset < len(titles):
                break
            else:
                print("标号不存在，请重新输入")
        
    #检测成功
    print("下载《"+ titles[offset]["title"] +"》...")
    return titles[offset]
