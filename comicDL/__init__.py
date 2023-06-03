'''
Author: Howv.John.Young
Date: 2023-06-01 14:29:30
LastEditTime: 2023-06-02 21:13:09
LastEditors: Howv.John.Young
Description: 
FilePath: \pythontest\comicDL\__init__.py
可以输入预定的版权声明、个性签名、空行等
'''
from .chapter_get import chapter_get_init
from .downloader import downloader_init
from .title_get import title_get_init
from .parser import parser_init

def comicDL_init(baseUrl:str, \
                 scriptPath:str, \
                searchUrl:str, \
                paserWaitTime:float, \
                downloadGapTime:float, \
                downloadRetryTimes:int ):
    print("初始化：\n\
          目标url：{}\n\
          geckodriver路径：{}\n\
          搜索url{}".format(baseUrl,scriptPath,searchUrl))

    chapter_get_init(baseUrl, scriptPath)
    downloader_init(downloadRetryTimes, downloadGapTime)
    parser_init(scriptPath, paserWaitTime)
    title_get_init(searchUrl)
