import os
import requests
import re
import urllib.request
from bs4 import BeautifulSoup

#写入文件，并将下一个图片的url返回供下一次爬取
def get_list_info(url,page,mmpath):
    web_data=requests.get(url)
    soup=BeautifulSoup(web_data.text,'lxml')
    src=soup.select('body > div.main > div.content > div.main-image > p > a > img')
    hre=soup.select('body > div.main > div.content > div.main-image > p > a')
    image_url = ""
    href = ""
    for src in src:
        image_url = src.get('src').split('net')[1]
    for hr in hre:
        href = hr.get('href')
    if page < 10:
        pages='0'+str(page)
    else:
        pages =str(page)
    url_split = 'http://i.meizitu.net' + image_url
    try:
        html = urllib.request.urlopen(url_split)
        name = pages
        data = html.read()
        fileName = '{}\meizi'.format(mmpath) + name + '.jpg'
        fph = open(fileName, "wb")
        fph.write(data)
        fph.flush()
        fph.close()
    except Exception:
        print('[!]Address Error!!!!!!!!!!!!!!!!!!!!!')
    return href

#对一个标题的所有图片进行爬取
def get_page_from(channel,pages=1):
    channel=channel+'/page/{}'.format(pages)
    web_data=requests.get(channel)
    soup=BeautifulSoup(web_data.text,'lxml')
    lists = soup.select('#pins > li > span > a')
    for lists in lists:
        path='D:\MM\{}'.format(lists.get_text())
        isExists = os.path.exists(path)
        if not isExists:
            print("新建了名字叫做" + path + "的文件夹")
            os.makedirs(path)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print("名为" + path + '的文件夹已经创建！')
            continue
        u = requests.get(lists.get('href'))
        s = BeautifulSoup(u.text,'lxml')
        size = 0
        lst = s.select('body > div.main > div.content > div.pagenavi > a > span')
        string = str(lst)
        size = max(re.findall(r'\d+',string))
        href = get_list_info(lists.get('href'),1,path)
        for i in range(2, int(size)):
            href = get_list_info(href,i,path)

#从一个专题中对所有页数爬取
def get_pages_from(channel):
    url = requests.get(channel)
    soup = BeautifulSoup(url.text,'lxml')
    lst = soup.select('body > div.main > div.main-content > div.postlist > nav > div > a')
    string = str(lst)
    try:
        r = re.findall(r'\d+',string)
        size = max(r)
        for i in range(1,int(size)):
            get_page_from(channel,i)
    except:
        pass