#####
# File Name: ptt_beauty_crawler.py
# Author: alen6516
# Created Time: 2018-02-06
#####
import re, sys, os, errno
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

class Beauty_crawler():
    def __init__(self):
        self.download_path='./'
        

    def set_path(self):
        self.download_path=input("give the path:\n")
        if self.download_path[-1]!='/':
            self.download_path+='/'
        if self.download_path[0]=='~':
            self.download_path=os.path.expanduser("~")+self.download_path[1:]

    def get_path(self):
        return self.download_path    

    def _get_title(self, soup):
        return soup.find('meta', property="og:title")["content"]
    
    def makedir(self, dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def download(self):
        target=input("give the target url:\n")
        res=requests.get(target, verify=False)
        soup = BeautifulSoup(res.text)
        pa1='https://i.imgur.com/.+\.jpg'
        pa2='https://imgur.com/.+'

        title = self._get_title(soup)
        path=self.download_path+title+'/'
        self.makedir(path)

        for a in soup.find_all('a', href=True):
            str=a['href']
            ans1=re.findall(pa1, str)
            ans2=re.findall(pa2, str)
            if ans1:
                for url in ans1:
                    urlretrieve(url, path+url.split('/')[-1])
            if ans2:
                for url in ans2:
                    url="https://i."+url.split('https://')[1]+'.jpg'
                    urlretrieve(url, path+url.split('/')[-1])


if __name__=='__main__':
    crawler=Beauty_crawler()
    op="1"
    while op!="0":
        op=input("[0]exit, [1] download, [2] set path, [3] show curr path:\n")
        if op=="0":
            sys.exit()
        
        elif op=="1":
            crawler.download()

        elif op=="2":
            crawler.set_path()

        elif op=="3":
            print("current download_path:\n%s" % crawler.get_path())
        
        else:
            print("wrong op, try again")
