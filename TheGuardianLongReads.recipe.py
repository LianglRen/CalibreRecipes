# -*- coding: utf-8 -*-
#modified on 2019 Oct 17, add and highlight Podcast article, add date of each article.
from calibre.web.feeds.recipes import BasicNewsRecipe
import re
from datetime import date

#!/usr/bin/python
# encoding: utf-8
#from calibre.web.feeds.recipes import BasicNewsRecipe

class GuardianLongRead(BasicNewsRecipe): # 

    #///////////////////
    # set metadata
    #///////////////////
    title = "The Guardian's Long Reads "+date.today().strftime("%Y-%b%d") # name of book
    description = "The Guadian's Long Read" # description of book
    cover_url = 'https://i.guim.co.uk/img/media/5bcc6f2d35078f96362a96f951b184180ef94228/0_0_1920_1152/master/1920.jpg?width=620&quality=85&auto=format&fit=max&s=199300c942a7bde8cf4a2e3860f72efb' #
    #masthead_url = '' # cover figure
    __author__ = 'Liangliang Ren' # author
    language = 'en_GB' # language
    #encoding = 'utf-8' # 

    timefmt = ' [%a, %d %b %Y]'
    no_stylesheets = True
    INDEX = 'https://www.theguardian.com/news/series/the-long-read'
    # auto_cleanup = True                   
    #language = 'zh-CN', content__article-body from-content-api js-article__body
    keep_only_tags = [
        {'class': ['content__main-column', 
        'content__dateline',
        'immersive-main-media__media', 
        'content__article-body from-content-api js-article__body'] }
    ]  # 
    remove_tags = [
        {'class':['contributions__epic contributions__epic--moment', 
        'rich-link__container', 
        'submeta ', 
        'content__meta-container js-content-meta u-cf', 
        'block-share block-share--gallery'] }
    ]
    max_articles_per_feed = 20           # defualt is 200 articles

    #def get_title(self, link):
    #    return(link.contents[0])#.strip()

    def parse_index(self):
        # soup = self.index_to_soup(self.INDEX)
        # pages_info = soup.findALL(**{'class': 'pages'}).text.split()
        # print 'pages_info:', pages_info
        start_page = 1      # int(pages_info[1])
        end_page = 1      # default is 25
        articles = []

        for p in range(start_page, end_page+1):     # deal with each html page 
            print(p)
            soup_page = self.index_to_soup(self.INDEX + '?page=' + str(p))
            #print(soup_page)
            for section in soup_page.findAll('div', {'class': 'fc-container--rolled-up-hide fc-container__body'}): 
                #each section contains at least one article, date, title, url, description.
                #print(section)
                #
                # get the date of section
                print("*********************************************")
                print(section['data-id'])
                date_id = section['data-id']
                #print("%s\n",date_id)
                for subsection in section.findAll('div', {'class': 'fc-item__container'}):
                    
                    ## get title and url of article.
                    #print("This is subsection.")
                    #for link in subsection.findAll('div', {'class':'fc-item__header'}): # get the url
                    
                        #print(link.a)
                    href = subsection.a
                    url = href['href']
                    print(url)
                    #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    tilloc = subsection.find('span', {'class': 'js-headline-text'})
                    til = tilloc.text
                    #print(href.contents)
                    print(til)

                    ## description
                    descriploc = subsection.find('div', {'class': 'fc-item__standfirst'})
                    if descriploc is None:
                        description = " "
                    else:
                        description = descriploc.text
                    
                    print(description)


                    #pod = re.search(" podcast$", til)
                    #if pod:
                    #    print("this is podcast: ", til)
                    #    continue  
                    #else:
                        #articles.append({'title': til, 'url': url})  

                    articles.append({'title': til, 'url': url, 'description':description, 'date':date_id}) 


                print("##############################################")
               
                    


            #div = soup_page.find('section') # ,('div', {'class':'fc-container--rolled-up-hide fc-container__body'})


            print('Page %d done' % p)
        #articles.reverse()                 # 
        #res = [(u"The Guardian's Long Read", articles)]    # return tuple
        # self.abort_recipe_processing('test')  # 
        return [(u"The Guardian's Long Read test", articles)]
