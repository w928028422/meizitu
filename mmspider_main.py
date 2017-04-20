from multiprocessing import Pool,Lock
from mmspider_parase import get_pages_from
import requests
import re
from bs4 import BeautifulSoup

#获取所有专题
def get_channels(start_url):
    url = requests.get(start_url)
    soup = BeautifulSoup(url.text,'lxml')
    tagList = soup.select('body > div.main > div.main-content > div.postlist > dl > dd > a')
    channels = []
    for tag in tagList:
       channels.append(tag.get('href'))
    return channels

#从首页开始爬取
if __name__ == '__main__':
    channels = get_channels('http://www.mzitu.com/zhuanti')
    pool = Pool(4)

    pool.map(get_pages_from, channels)