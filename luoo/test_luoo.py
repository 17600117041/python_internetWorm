# encoding=utf8
import requests
from bs4 import BeautifulSoup
import re
import os

tagListUrl = 'http://www.luoo.net/tag/?p='
mp3Url = 'http://mp3-cdn2.luoo.net/low/luoo/radio%s/%s.mp3'
# 定义文件保存路径
targetPath = "/Users/zhangda/PhpstormProjects/python/mp3"
# radio930/01.mp3
def gethtml(url):
    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel Mac OS X 10.12; rv: 54.0) Gecko / 20100101 Firefox / 54.0",
        "Accept-Encoding" : "gzip, deflate",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cache-Control" : "max-age=0"
    }
    try:
        responses = requests.get(url,headers=headers)
        responses.encoding = "utf-8"
        html = responses.text
        soup = BeautifulSoup(html,"html.parser")
        return soup
    except:
        print(str(url) + ":html parse error in getUserData()")


# def getHtmlObj():
#     soup = BeautifulSoup(html)
#     return soup

def getTagList():
    soup = gethtml(tagListUrl)
    datas = {}
    total_div_obj = soup.find("div",class_="vol-list")
    vol_list_obj = total_div_obj.find_all("div",class_="item")
    for itemobj in vol_list_obj:
        title = itemobj.find("a").attrs['title'].strip()
        url = itemobj.find("a").attrs['href'].strip()
        # likes  = itemobj.find("span",class_="favs").text('|', strip=True).split('|')
        likes  = itemobj.find("span",class_="favs").get_text(strip=True)
        comments  = itemobj.find("span",class_="comments").get_text(strip=True)
        number_obj = itemobj.find("a",class_="name").get_text(strip=True)
        num = re.findall("[0-9]+",number_obj)
        if num :
            datas[num[0]] = {}
            datas[num[0]]["title"] = title
            datas[num[0]]["url"] = url
            datas[num[0]]["likes"] = likes
            datas[num[0]]["comments"] = comments
            datas[num[0]]["num"] = num[0]
        else:
            continue
        # break
    return datas

def getVolList():
    datas = getTagList()
    downLoadInfo = {}
    for data,values in datas.items():
        volUrl = values['url']
        num = values['num']
        downLoadInfo[num] = {}
        volSoup = gethtml(volUrl)
        ulObj = volSoup.find_all("li",class_="track-item")
        idsObj = volSoup.find_all("a",class_="trackname")
        for obj in idsObj:
            id = obj.get_text()
            mp3_name = re.findall("\D+", id)[0].replace(".","")
            id = re.findall("[0-9]{2,3}",id)[0]
            downLoadMp3(num,id,mp3_name)

def downLoadMp3(num,id,file_name):
    file_url =  mp3Url % (num, id)
    local_file_dict = targetPath+'/'+num
    if not os.path.exists(local_file_dict):
        os.makedirs(local_file_dict)

    local_file = '%s/%s.%s.mp3' % (local_file_dict, id, file_name)
    if not os.path.isfile(local_file):
        print('downloading: ' + file_name)
        res = requests.get(file_url)
        with open(local_file, 'wb') as f:
            f.write(res.content)
            f.close()
        print('done.\\n')
    else:
        print('break: ' + file_name)

getVolList()