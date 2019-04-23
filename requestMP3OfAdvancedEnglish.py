from bs4 import BeautifulSoup
import urllib.request
import requests
import re

INDEX = 'http://www.tingliku.com/tingli/gaojiyingyu/'
INDEX_tail = ['', 'index_2.html']
INDEX_root = 'http://www.tingliku.com'

MP3url = []

for p in INDEX_tail:
    pageUrl = INDEX + p
    print(pageUrl)
    url = urllib.request.urlopen(pageUrl)
    #print(url)
    content = url.read()
    #print(content)
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    for box in soup.findAll('div', {'class': 'news_list box'}):
        #print(box)
        for link in box.findAll('h3'):
            #print("this is link: ", link.a['href'])
            subUrl = link.a['href']
            title = link.a.text
            #print(title)

            ## subpage
            subPage = urllib.request.urlopen(subUrl)
            subContent = subPage.read()
            subSoup= BeautifulSoup(subContent, 'html.parser')
            #print(subSoup)
            ## handle with subpage, i.e. each article
            for link in subSoup.findAll('div', {'class': 'layout'}):
                aud = link.find('object', {'type': 'application/x-shockwave-flash'})
                audioUrl = INDEX_root+ aud.audio['src']
                #print("this is audio: ", aud)
                #print( audioUrl)
                if re.search(".mp3$", audioUrl):
                    MP3url.append({"title": title, "url": audioUrl})

print(MP3url)


for item in MP3url:
    print("this is ", item['url'])
    #print("a", r)
    link = item['url']
    r= requests.get(link)
    with open(item['title']+'.mp3', 'wb') as f:
        f.write(r.content)
        print("file written. ")

print("All files done. ")


