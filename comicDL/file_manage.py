

import os
import json

#book.info
'''
{
    "bookname" : "Demo",
    "bookLink" : "http://booksite.com/Demo/",
    "chapterList" : [
        {
            "chapterName" : "C_demo",
            "chapterLink" : "http://booksite.com/Demo/1234.html",
            "chapterPath": "./C_demo/chapter.info",
        },
        {
        ...
        },
    ],
}
'''

#chapter.info
'''
{
    "bookName" : "Demo",
    "bookLink" : "http://booksite.com/Demo/",
    "chapterName" : "C_demo",
    "chapterLink" : "http://booksite.com/Demo/1234.html",
    "imgList" : [
        {
            "imgName" : "001.jpg",
            "imgLink" : "http://img.bookimg.com/123adc.jpg",
        },
        {
            "imgName" : "001.jpg",
            "imgLink" : "http://img.bookimg.com/3214adc.jpg",
        },
        ...
    ]
}

'''
def file_create(fileNameWithPath:str)->int:
    if not os.path.exists(fileNameWithPath):
        os.makedirs(fileNameWithPath)
    return 0



def json_file_get(filePath:str, fileName:str)->dict:
    fileWithPath = os.path.join(filePath, fileName)
    #若不存在，直接返回空json，不创建文件
    if not os.path.exists(fileWithPath):
        return {}
    #若存在读取json
    with open(fileWithPath, "r", encoding="UTF-8") as f:
        content = f.read()
    try:
        ret = json.loads(content)
    except json.decoder.JSONDecodeError:
        print("json解析错误")
        return {}
    except :
        print("file_manage:未知错误")
    
    return ret


def json_file_put(filePath:str, fileName:str, json_info:dict):
    fileWithPath = os.path.join(filePath, fileName)
    #若不存在，创建；若存在，则覆盖
    with open(fileWithPath, "w", encoding="UTF-8") as f:
        f.write(json.dumps(json_info))

def chapter_index_create(bookPath:str, bookLink:str, chapterName:str, chapterLink:str, imgList:list):
    tmp = {
        "bookName" : os.path.split(bookPath)[-1],
        "bookLink" : bookLink,
        "chapterName" : chapterName,
        "chapterLink" : chapterLink,
        "imgList" : [],
    }
    num = 0
    for i in imgList:
        num += 1
        endwith = os.path.splitext(i)[-1]
        tmp["imgList"].append({\
                    "imgName" : "{:0>3d}".format(num)+endwith,\
                    "imgLink" : i,})
    json_file_put(os.path.join(bookPath,chapterName), "chapter.info", tmp)



''' 
chapterList = [
{
    "chapterName" : "001.firstChater",
    "chapterPath" : "./Demo/c_demo",
    "chapterLink" : "http://demo.com/test.html"
},
...
]

'''


def book_json_generate(bookPath:str, bookLink:str, chapterList:list)->dict:
    tmp = {
        "bookName" : os.path.split(bookPath)[-1],
        "bookLink" : bookLink,
        "chapterList" : []
    }
    for i in chapterList:
        tmp["chapterList"].append({"chapterName" : i["chapterName"], \
                                   "chapterLink" : i["chapterLink"], \
                                   "chapterPath" : os.path.relpath( \
                                    i["chapterPath"], bookPath) + \
                                        "\chapter.info"})
    return tmp



def book_index_create(bookPath:str, bookLink:str, chapterList:list):
    tmp = book_json_generate(bookPath=bookPath, bookLink=bookLink, chapterList=chapterList)
    json_file_put(bookPath, "book.info", tmp)
 
