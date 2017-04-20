
from mmspider_parase import get_page_from
import requests
import re
from bs4 import BeautifulSoup

#从一个专题中对所有页数爬取
def get_pages_from(channel):
    url = requests.get(channel)
    soup = BeautifulSoup(url.text,'lxml')
    lst = soup.select('body > div.main > div.main-content > div.postlist > nav > div > a')
    string = str(lst)
    size = max(re.findall(r'\d+',string))
    for i in range(1,int(size)):
        get_page_from(channel,i)

#获取所有专题
def get_channel(start_url):
    url = requests.get(start_url)
    soup = BeautifulSoup(url.text,'lxml')
    tagList = soup.select('body > div.main > div.main-content > div.postlist > dl > dd > a')
    channel = []
    for tag in tagList:
        channel.append(tag.get('href'))
    return channel

#从首页开始爬取
def main():
    channel = get_channel('http://www.mzitu.com/zhuanti/')
    for ch in channel:
        get_pages_from(ch)

main()
