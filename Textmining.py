# https://github.com/vz-risk/VCDB/issues/9530

from collections import Counter
from bs4 import BeautifulSoup, NavigableString
import os
import requests
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
# import lxml.html
from urllib import urlopen
from urlparse import urlparse
import numpy
import itertools
import csv
import json
import time



os.getenv('PORT', '8080')
os.getenv('IP', '0.0.0.0')

count = 0
sublinks =[]
links = []

def resolve_redirects(url):
    try:
        return urllib2.urlopen(url).read()
    except HTTPError, e:
        if e.code == 429:
             time.sleep(8);
             return resolve_redirects(url)
        raise



baseurl ='https://github.com/vz-risk/VCDB/issues?page='
#str(pagenum)
parturl = '&q=is%3Aissue+is%3Aopen'
f = open('file_final3.txt', 'w')
for i in range (0, 180):
    fullurl = baseurl + str(i) + parturl 
    text = resolve_redirects(fullurl)
    # text = urllib2.urlopen(fullurl, timeout=20).read()
    soup = BeautifulSoup(text, "html5lib")
    soup.prettify()
    #print(soup)    kukllukll
    for data in soup.find_all("div", class_="float-left col-9 p-2 lh-condensed"):
        link = "https://github.com/" + data.find('a')['href']
        #print link
        page_content = urlopen(link)    # getting links from second level page
        beautiful_content = BeautifulSoup(page_content.read(), "html5lib")
        beautiful_content.prettify()
        #==================Time
        text = urllib2.urlopen(link).read()
        soup = BeautifulSoup(text, "html5lib")
        soup.prettify()
        #print(soup)
        datatime = soup.find_all("div", class_="TableObject-item TableObject-item--primary")
        for div in datatime:
            links = div.findAll('relative-time')
            for a in links:
                time=a['datetime']
                #print(time)
        #======================= Tag
        datatag = soup.find_all("div", class_="labels css-truncate")
        tag = ''
        for div in datatag:
            linktag = div.findAll('a')
            for a in linktag:
                #print a['title']
                tag +=a['title']
                tag +=':'
        #=======================Contributor
        datacontributor = soup.find_all("div", class_="participation-avatars")
        for div in datacontributor:
            links = div.findAll('a')
            for a in links:
                #print a['aria-label']
                Contributor=a['aria-label']
        #=======================
        
        div = beautiful_content.find('div', {'class': "edit-comment-hide"})
        try:
            div = div.find("p").find("a")
            #print(div['href'])
            urllink= div['href']
            #print(urllink)
        except: pass
         page = requests.get(urllink, allow_redirects=False)#get html text from the urllinks
         page
         soup = BeautifulSoup(page.content, 'html.parser')
         htmltext=soup.prettify("utf-8") # this is raw html data
        print(htmltext)
        print(urllink + ','+time+ ',' + tag +',' + Contributor +','+ time)
        #f.write(str(urllink) + '\n')
        with open('data.csv','a') as scorefile:#======== CSV writer
            scorefilewriter = csv.writer(scorefile)
            scorefilewriter.writerow([urllink,'data/'+time,tag,Contributor,time])
        scorefile.close()
        resfile = open(str(time) + ".txt","w")
        resfile.write(str(htmltext))
        resfile.close()

f.close()
#p.agent_info = u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()



