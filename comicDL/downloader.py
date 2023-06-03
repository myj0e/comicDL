'''
Author: Howv.John.Young
Date: 2023-06-01 15:47:21
LastEditTime: 2023-06-02 21:15:41
LastEditors: Howv.John.Young
Description: 
FilePath: \pythontest\comicDL\downloader.py
可以输入预定的版权声明、个性签名、空行等
'''
import requests
import queue
import time
import os



#未初始化的全局变量
'''
download_gap_time = 0.5
download_retry_times = 3
'''

def downloader_init(downloadRetryTimes:int, downloadGapTime:float):
    global download_gap_time
    global download_retry_times
    download_gap_time = downloadGapTime
    download_retry_times = downloadRetryTimes



def download(downLoadPath:str,fileName:str, link:str)->int:
    filePath = os.path.join(downLoadPath,fileName)
    if not os.path.exists(filePath):
        try:
            r = requests.get(link)
        except ConnectionError:
            print("{}-{}下载网络错误".format(os.path.split(downLoadPath),fileName))
            return None
        except Exception:
            print("{}-{}下载错误".format(os.path.split(downLoadPath),fileName))
            return None
        with open(filePath, "wb") as f:
            f.write(r.content)
        return 0
    else:
        print(fileName + "已存在", end = "")
        return 0

'''
msg type
{
    "downLoadPath" : "/path/pathA/",
    "chapterUrl" : "http://test.com/123.html",
    "enable" : 1
}
'''


def downloader(qImgUrls:queue.Queue):
    while True:
        msg = qImgUrls.get()
        #判断是否继续
        if msg["enable"] != 1:
            print("downloader over...")
            break

        #还有数据，继续
        chapterName = msg["chapterName"]
        downLoadPath = msg["downloadPath"]
        urlList = msg["imgUrls"]
        
        #对图片逐个下载，并升序命名
        num = 0
        for i in urlList:
            num += 1
            endwith = os.path.splitext(i)[-1]
            #下载失败时重新尝试的次数
            retry_times = download_retry_times
            if download(downLoadPath, "{:0>3d}".format(num)+endwith, i) != None:
                pass
            else:
                while retry_times > 0:
                    print("{}-{}重新尝试...{}".format(os.path.split(downLoadPath),"{:0>3d}".format(num)+endwith,retry_times))
                    retry_times -= 1
                    download_state = download(downLoadPath, "{:0>3d}".format(num)+endwith, i)
                    if download_state != None:
                        break
                if download_state == None:
                    print("{}-{}多次失败，中止尝试".format(os.path.split(downLoadPath),"{:0>3d}".format(num)+endwith))
                else:
                    print("{}-{}下载成功".format(os.path.split(downLoadPath),"{:0>3d}".format(num)+endwith))

        print("\n>>>《{}》处理完成".format(chapterName))
        #防爬虫
        time.sleep(download_gap_time)
    
    return 0

