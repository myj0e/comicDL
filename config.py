'''
Author: Howv.John.Young
Date: 2023-06-02 13:04:25
LastEditTime: 2023-06-03 13:41:53
LastEditors: Howv.John.Young
Description: "
FilePath: \pythontest\config.py
可以输入预定的版权声明、个性签名、空行等
'''
################################ 基本参数 ############################
#列表用于管理所有基本参数，检查列表项中内容是否有定义
basic_variable = [
    "VERSION",
    "DOMAIN_URL",
    "DOWNLOADER_THREADS_NUM",
    "PARSER_THREADS_NUM",
    "DOWNLOAD_RETRY_TIMES",
    "DOWNLOAD_FILE_NAME",
    "SCRIPT_PATH",
    "SEARCH_PARAM",
    "PARSER_WAIT_TIME",
    "DOWNLOAD_GAP_TIME",
]
#####################################################################
#程序版本
VERSION = "1.0.0"

#目标网站url
DOMAIN_URL = ""

#启用downloader线程数
DOWNLOADER_THREADS_NUM = 3

#启用parser线程数
PARSER_THREADS_NUM = 3

#下载失败重试次数
DOWNLOAD_RETRY_TIMES = 3

#下载路径文件名，默认以当前路径为根目录
DOWNLOAD_FILE_NAME = "download"

#script（即deckodirver程序的位置）
SCRIPT_PATH = "./script/geckodriver"

#搜索参数
SEARCH_PARAM = "search.php?keyword="

#解析章节图片等待时间，为保证页面js执行完成建议不小于3（秒），加载等待的时间可作为规避爬虫检测的手段
PARSER_WAIT_TIME = 10

#下载图片所用等待时间，图片以章为组，DOWNLOAD_GAP_TIME为组间间隔时间，默认0.5(秒)
DOWNLOAD_GAP_TIME = 0.5

############################## 自动生成参数 ##########################


#搜索标题用的url
SEARCH_URL = ""

#下载路径
DOWNLOAD_PATH = ""

#当前运行路径
CWD = ""


############################## 初始化函数 #############################
#init接口
import os

def init()->int:
###参数完整性检查###
    ret = 0
    for i in basic_variable:
        if(i not in globals()):
            ret = -1
            print("config文件参数缺失: "+i)
    #若发生缺失，报错退出
    if ret != 0:
        return ret
###自动生成参数###
    #参数全局声明
    global SEARCH_URL
    global CWD
    global DOWNLOAD_PATH

    SEARCH_URL = DOMAIN_URL + "/" + SEARCH_PARAM
    CWD = os.getcwd()
    DOWNLOAD_PATH = os.path.join(CWD, DOWNLOAD_FILE_NAME)
    return 0
