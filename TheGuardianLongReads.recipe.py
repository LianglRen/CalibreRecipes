from calibre.web.feeds.recipes import BasicNewsRecipe
import re
from datetime import date

#!/usr/bin/python
# encoding: utf-8
#from calibre.web.feeds.recipes import BasicNewsRecipe

class GuardianLongRead(BasicNewsRecipe): # 继承 BasicNewsRecipe 类的新类名

    #///////////////////
    # 设置电子书元数据
    #///////////////////
    title = "The Guardian's Long Reads" # 电子书名
    description = 'The Guadian The long read' # 电子书简介
    cover_url = 'https://i.guim.co.uk/img/media/5bcc6f2d35078f96362a96f951b184180ef94228/0_0_1920_1152/master/1920.jpg?width=620&quality=85&auto=format&fit=max&s=199300c942a7bde8cf4a2e3860f72efb' # 电子书封面
    #masthead_url = '' # 页头图片
    __author__ = 'Liangliang Ren' # 作者
    language = 'en_GB' # 语言
    #encoding = 'utf-8' # 编码

    timefmt = ' [%a, %d %b %Y]'
    no_stylesheets = True
    INDEX = 'https://www.theguardian.com/news/series/the-long-read'
    # auto_cleanup = True                   # 如果没有手动分析文章结构，可以考虑开启该选项自动清理正文内容
    #language = 'zh-CN', content__article-body from-content-api js-article__body
    keep_only_tags = [
        {'class': ['content__main-column', 
        'content__dateline',
        'immersive-main-media__media', 
        'content__article-body from-content-api js-article__body'] }
    ]  # 仅保留文章的content__article-body from-content-api js-article__body中的内容，其中为自己分析得到的正文范围
    remove_tags = [
        {'class':['contributions__epic contributions__epic--moment', 
        'rich-link__container', 
        'submeta ', 
        'content__meta-container js-content-meta u-cf', 
        'block-share block-share--gallery'] }
    ]
    max_articles_per_feed = 200           # 默认最多文章数是100，可改为更大的数字以免下载不全

    #def get_title(self, link):
    #    return(link.contents[0])#.strip()

    def parse_index(self):
        # soup = self.index_to_soup(self.INDEX)
        # pages_info = soup.findALL(**{'class': 'pages'}).text.split()
        # print 'pages_info:', pages_info
        start_page = 1      # int(pages_info[1])
        end_page = 25      # int(pages_info[3])
        articles = [] 

        for p in range(start_page, end_page+1):     # 处理每一个目录页
            soup_page = self.index_to_soup(self.INDEX + '?page=' + str(p))
            for section in soup_page.findAll('div', {'class':'fc-item__container'}): # each article
                #print(section)
                for link in section.findAll('h3', {'class':'fc-item__title'}): # get the url
                    print("*********************************************")
                    #print(link.a)
                    href = link.a
                    url = href['href']
                    #print(til)
                    print(url)
                      
                for span in link.findAll('span', {'class':'js-headline-text'}): # get the title
                    print(span.contents[0])
                    til = span.contents[0]
                    #til = self.get_title(href)
                ## ignore the podcast, duo to which are slection of the Guardian’s long read articles which are published in the paper and online. 
                pod = re.search(" podcast$", til)
                #print("POD: ", pod)
                #print("til: ", til)
                if pod:
                    print("this is podcast: ", til)
                    continue  
                else:
                    articles.append({'title': til, 'url': url})                     


                    print("##############################################")
                    


            #div = soup_page.find('section') # ,('div', {'class':'fc-container--rolled-up-hide fc-container__body'})


            #soup_titles = soup_page.findAll(**{'class': 'u-faux-block-link__overlay js-headline-text'})     # 从目录页中提取正文标题和链接, , fc-item__container
            #for link in div.findAll('div', {'class':'fc-item__container'}):
            #    print("*********************************************")
            #    print(link.a)
            #    print("##############################################")
                #href = soup_title.a
                #articles.append({'title': href['title'][18:], 'url': href['href']}) 
            #print(articles)
            print('page %d done' % p)
        #articles.reverse()                 # 文章倒序，让其按照时间从前到后排列
        res = [(u'The long read', articles)]    # 返回tuple，分别是电子书名字和文章列表
        # self.abort_recipe_processing('test')  # 用来中断电子书生成，调试用
        return res
