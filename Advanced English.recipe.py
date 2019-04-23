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
    title = "高级英语 Advanced English(张汉熙)" # 电子书名
    description = '张汉熙版《高级英语》"Advanced English" 适用于已掌握英语基础知识的进入高年级的学生。有些课文全部选自原文，有些经过压缩或节选。' \
                  '课文的内容及题材力求多样化，以便学生接触不同的文体，吸收较广泛的知识。张汉熙高级英语是英语专业通向专业八级之路的教材，需要认真地研读和思考。' \
                  '教材有点儿老，但是每一篇文章都是经典之作。为了学习其中的专业八级词汇，可以一边听录音，一边对照课文。' # 电子书简介
    cover_url = 'https://images-na.ssl-images-amazon.com/images/I/51B7wMqNQdL.jpg' # 电子书封面
    #masthead_url = '' # 页头图片
    __author__ = 'Liangliang Ren' # 作者
    language = 'en_GB' # 语言
    #encoding = 'utf-8' # 编码

    timefmt = ' [%a, %d %b %Y]'
    no_stylesheets = True
    INDEX = 'http://www.tingroom.com/lesson/advancedenglish/advancedenglish'
    INDEX_master = 'http://www.tingroom.com'
    # auto_cleanup = True                   # 如果没有手动分析文章结构，可以考虑开启该选项自动清理正文内容
    #language = 'zh-CN', # content__article-body from-content-api js-article__body
    keep_only_tags = [
        {'class':'title_viewbox'},
        {'id': 'zoom'}
    ]  # 仅保留文章的content__article-body from-content-api js-article__body中的内容，其中为自己分析得到的正文范围

    #remove_tags = [{'class':'contributions__epic contributions__epic--moment' }]
    max_articles_per_feed = 200           # 默认最多文章数是100，可改为更大的数字以免下载不全

    #def get_title(self, link):
    #    return(link.contents[0])#.strip()

    def parse_index(self):
        # soup = self.index_to_soup(self.INDEX)
        # pages_info = soup.findALL(**{'class': 'pages'}).text.split()
        # print 'pages_info:', pages_info
        start_page = 1      # int(pages_info[1])
        end_page = 2      # int(pages_info[3])
        articles = [] 

        for p in range(start_page, end_page+1):     # 处理每一个目录页
            soup_page = self.index_to_soup(self.INDEX + str(p) + '/index.html')
            #print(soup_page)
            for section in soup_page.findAll('ul', {'class': 'e2'}):  # each page
                #print("Section is: ", section)
                for link in section.findAll('li'): # get the url
                    print("*********************************************")
                    #print(link.prettify())
                    href = link.a
                    print(href)
                    #print(href['href'])
                    #print("title text: ", href.contents[0])
                    #print(link.get_text())


                    url = self.INDEX_master + href['href']
                    til = href.contents[0]
                    print(url)
                    print("title is: ", til)


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
        res = [('高级英语 Advanced English(张汉熙)', articles)]    # 返回tuple，分别是电子书名字和文章列表
        # self.abort_recipe_processing('test')  # 用来中断电子书生成，调试用
        return res
