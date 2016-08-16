'''
Created on 2016年7月31日

@author: Administrator

'''
import datetime
import http.cookiejar
import os
import random
import re
import time
import urllib.parse
import urllib.request

# result = []
# newProduct = ""

# 寫入檔案  
def writeFile(data , isList):   
    if isList:
        file = open("list.txt", "w")
        for i in range(data.__len__()):
            
            file.write(data[i] + "\n")
    else:
        file = open("new.txt", "a")
        file.write(datetime.datetime.now().__str__() + "\n")
        file.write(data + "\n")
        
    file.close()
    
def crawler(url):
    request = urllib.request.Request(url, headers={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
    
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    
    htmlText = opener.open(request, timeout=1000).read()
    
    try:
        htmlText = htmlText.decode()  # utf8
    except:
        htmlText = htmlText.decode("big5")
        
    return htmlText        

# 露天拍賣
def rutenParse(htmlText):      
    pattern = '<a href="http://goods.+ title=".+">' 
    return re.findall(pattern, htmlText)

# 滄者極限
def coolalerParse(htmlText):
    pattern = '<a class="title" href="showthread.php/.+970.+</a>' 
    return re.findall(pattern, htmlText)

# PCDVD
def pcdvdParse(htmlText):
    pattern = '<a href="showthread.php.+970.+</a>' 
    return re.findall(pattern, htmlText)

if __name__ == "__main__":   
    
    # 露天拍賣 
    parm = "?" + urllib.parse.urlencode({"enc": 'u',
                                        "k":"970",
                                        "c":"0011000500210001",
                                        "ctab":"1",
                                        "searchfrom":"searchbars",
                                        "f":"0",
                                        "m":"1",
                                        "fy":"0",
                                        "h":"0",
                                        "p1":"5500",
                                        "p2":"7000" })    
    url = "http://search.ruten.com.tw/search/s000.php" + parm
    
    result = ""
    result = rutenParse(crawler(url))
    
    # 滄者極限
    url = "http://www.coolaler.com/forumdisplay.php/127-NVIDIA-%E9%A1%AF%E7%A4%BA%E5%8D%A1"
    
    for str in coolalerParse(crawler(url)):
        result.append(str)

    
    
    # PCDVD
    url = "http://www.pcdvd.com.tw/forumdisplay.php?f=37"
    # result = pcdvdParse(crawler(url))
    
#     file = open("html.html", "w", encoding='utf-8-sig')
#     html = crawler(url)
#     file.write(html)
#     file.close()
    
    # 比對list與result
    filePath = "list.txt"
    
    # 測試檔案是否存在
    if not os.path.isfile(filePath): 
        writeFile(result, True)
    
    isMatch = True;
    file = open(filePath, "r")
    
    # 比對每行，若有新的商品則以ring.mp3提醒
    # 若是第一次執行，line為none，isMatch保持true
    line = file.readlines() 
                
    for aMatch in result: 
        aMatch += "\n"
              
        if aMatch not in line:
            isMatch = False
            writeFile(aMatch, False)
            
    if not isMatch:
        os.startfile("ring.mp3")
        
    file.close()
    
    writeFile(result, True)
    
    
    pass
    
#     while True:
#         rutenParse()
#         print(datetime.datetime.now().__str__() + "查詢完成")
#         delay = random.randint(3, 10) * 60
#         time.sleep(delay)
