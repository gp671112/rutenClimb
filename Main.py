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

# 寫入檔案  
def writeFile(filePath, data , isList):      
    if isList:
        file = open(filePath, "w")
        for i in range(data.__len__()):
            
            file.write(data[i] + "\n")
    else:
        file = open(filePath, "a")
        file.write(datetime.datetime.now().__str__() + "\n")
        file.write(data + "\n")
        
    file.close()
    
def climb():
    
    # http-get parm
    parm = "?" + urllib.parse.urlencode({"enc": 'u',
                                        "k":"970",
                                        "c":"0011000500210001",
                                        "ctab":"1",
                                        "searchfrom":"searchbars",
                                        "f":"0",
                                        "m":"1",
                                        "fy":"0",
                                        "h":"0",
                                        "p1":"5000",
                                        "p2":"7000" })    
    url = "http://search.ruten.com.tw/search/s000.php" + parm
    
    request = urllib.request.Request(url, headers={
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    })
    
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    
    data = opener.open(request, timeout=1000).read().decode()
    
    pattern = '<a href="http://goods.+ title=".+">'
    match = re.findall(pattern, data)
    
    filePath = "list.txt"
    
    # 測試檔案是否存在
    if not os.path.isfile(filePath): 
        writeFile(filePath, match, True)
    
    isMatch = True;
    file = open(filePath, "r")
    
    # 比對每行，若有新的商品則以ring.mp3提醒
    # 若是第一次執行，line為none，isMatch保持true
    line = file.readlines()     
    # line = line.strip('\n')      
                
    for aMatch in match: 
        aMatch += "\n"
              
        if aMatch not in line:
            isMatch = False
            newTxt = "new.txt"
            writeFile(newTxt, aMatch, False)
            
    if not isMatch:
        os.startfile("ring.mp3")
        
    file.close()
    
    writeFile(filePath, match, True)

if __name__ == "__main__":
    
    while True:
        climb()
        print(datetime.datetime.now().__str__() + "查詢完成")
        delay = random.randint(3, 10) * 60
        time.sleep(delay)
    
    
    
