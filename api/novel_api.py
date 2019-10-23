#!/usr/bin/env python
# -*- coding: utf-8 -*-
#小说接口
import requests
import uuid
from lxml import etree
import sys
import re
import base64
import random
from urllib import quote
from pyquery import PyQuery as pq
reload(sys)
sys.setdefaultencoding('utf-8')
novel_list = {'novel01':{'charset':'utf-8','search_url':'https://so.biqusoso.com/s.php?ie=utf-8&siteid=qb5200.tw&q=','xpath':{'novel_list':'//div[@class="search-list"]/ul/li[position()>1]','book_name':'span[position()=2]/a/text()','author_name':'span[position()=3]/text()','novel_url':'span[position()=2]/a/@href','chapter_list':'//div[@class="listmain"]/dl/dd[position()>12]','chapter_url':'a/@href','chapter_name':'a/text()','content':'#content','title':'//div[@class="content"]/h1/text()','prev_url':'//div[@class="page_chapter"]/ul/li[position()=1]/a/@href','next_url':'//div[@class="page_chapter"]/ul/li[position()=3]/a/@href','catalog_url':'//div[@class="page_chapter"]/ul/li[position()=2]/a/@href'},'filter_content':'chaptererror();|请记住本书首发域名：www.qb5200.tw。全本小说网手机版阅读网址：m.qb5200.tw','re_content':'www.qb5200.tw','site_url':'https://www.qb5200.tw'},
'novel02':{'charset':'gbk','search_url':'http://www.quanshuwang.com/modules/article/search.php?searchtype=articlename&searchkey=','xpath':{'novel_list':'//div[@class="mainnav"]/section/ul/li','book_name':'span/a[position()=1]/text()','author_name':'span/a[position()=2]/text()','novel_url':'span/a[position()=1]/@href','novel_catalog_url':'//div[@class="b-oper"]/a[position()=1]/@href','chapter_list':'//div[@class="chapterNum"]/ul/div[position()=2]/li','chapter_url':'a/@href','chapter_name':'a/text()','content':'.mainContenr','title':'//h1/strong/text()','prev_url':'//div[@class="backs"]/a[position()=1]/@href','next_url':'//div[@class="backs"]/a[position()=3]/@href','catalog_url':'//div[@class="backs"]/a[position()=2]/@href'},'filter_content':'style5();|style6();','filter_chapter':u'章 节目录|目录','site_url':'http://www.quanshuwang.com'},
'novel03':{'charset':'utf-8','search_url':'https://www.dingdianxs.com/modules/article/search.php?searchkey=','xpath':{'novel_list':'//div[@class="novelslistss"]/li','book_name':'span[@class="s2"]/a/text()','author_name':'span[@class="s4"]/text()','novel_url':'span[@class="s2"]/a/@href','chapter_list':'//div[position()=3]/div[position()=1]/dl/dd','chapter_url':'a/@href','chapter_name':'a/text()','content':'#content','title':'//h1/text()','prev_url':'//div[position()=5]/a[position()=2]/@href','next_url':'//div[position()=5]/a[position()=4]/@href','catalog_url':'//div[position()=5]/a[position()=3]/@href'},'site_url':'https://www.dingdianxs.com'},
'novel04':{'charset':'gbk','search_url':'https://www.yuanzunxs.cc/modules/article/search.php?searchkey=','xpath':{'novel_list':'//div[@class="bookbox"]/div[@class="p10"]/div[@class="bookinfo"]','book_name':'h4[@class="bookname"]/a/text()','author_name':'div[@class="author"]/text()','novel_url':'h4[@class="bookname"]/a/@href','chapter_list':'//div[@class="content"]/dl[@class="book chapterlist"]/div[@id="list-chapterAll"]/dd','chapter_url':'a/@href','chapter_name':'a/text()','content':'.readcontent','title':'//h1/text()','prev_url':'//div[@class="content"]/div[@class="book read"]/p[@class="text-center"]/a[@id="linkPrev"]/@href','next_url':'//div[@class="content"]/div[@class="book read"]/p[@class="text-center"]/a[@id="linkNext"]/@href','catalog_url':'//div[@class="content"]/div[@class="book read"]/p[@class="text-center"]/a[@id="linkIndex"]/@href','filter_content':'本章未完，点击下一页继续阅读'},'site_url':'https://www.yuanzunxs.cc'}
}

class Novel():
    def __init__(self):
        self.novel_id = None
    def randomm(self):
        novel_site = [i for i in novel_list]
        self.novel_id = random.choice(novel_site)
    def base64_to_url(self,url=None,siteid=None,status=None,data=None):
        if status == 'add':
            data = url + '|' + siteid
            res = base64.b64encode(data)
        elif status == 'delete':
            res = base64.b64decode(data)
        return res
    def get_novel(self,name):
        self.randomm() #随机获取小说site
        self.novel_id = 'novel04'
        print self.novel_id
        charset = novel_list.get(self.novel_id).get('charset')
        name = quote(name.encode(charset))
        target_url = novel_list.get(self.novel_id).get('search_url') + name
        res = requests.get(target_url)
        
        res = self.check_encoding(data=res)
        root = etree.HTML(res)
        novels = root.xpath(novel_list.get(self.novel_id).get('xpath').get('novel_list'))
        result = []
        for novel in novels:
            author_name = novel.xpath(novel_list.get(self.novel_id).get('xpath').get('author_name'))[0]
            book_name = novel.xpath(novel_list.get(self.novel_id).get('xpath').get('book_name'))[0]
            url = novel.xpath(novel_list.get(self.novel_id).get('xpath').get('novel_url'))[0]
            url = self.base64_to_url(url=url,siteid=self.novel_id,status='add')
            result.append({ 'author_name': author_name, 'book_name': book_name, 'url': url})
        return result
    def get_chapter(self,url,sort_id):
        #self.novel_id = site_id
        resutl = self.base64_to_url(data=url,status='delete')
        url = resutl.split('|')[0]
        self.novel_id = resutl.split('|')[1]
        if url.startswith('http') is False and url.startswith('https') is False:
            url = novel_list.get(self.novel_id).get('site_url') + url
        else:
            pass
        res = requests.get(url)
        res = self.check_encoding(data=res)
        root = etree.HTML(res)
        if novel_list.get(self.novel_id).get('xpath').get('novel_catalog_url',None):
            #判断是否存在目录url 获取参数 如果存在 需要先通过小说url 获取目录url 在获取目录
            catalog_url = root.xpath(novel_list.get(self.novel_id).get('xpath').get('novel_catalog_url'))[0] 
            if catalog_url.startswith('http') is False and catalog_url.startswith('https') is False:
                #catalog_url = 'http://' + url.split('/')[2] + catalog_url
                catalog_url = novel_list.get(self.novel_id).get('site_url') + catalog_url
            rest = requests.get(catalog_url)
            rest = self.check_encoding(data=rest)
            root = etree.HTML(rest)
            chapters = root.xpath(novel_list.get(self.novel_id).get('xpath').get('chapter_list'))
        else:
            #a = '//div[position()=3]/div[position()=1]/dl/dd'
            #chapters = root.xpath(a)
            chapters = root.xpath(novel_list.get(self.novel_id).get('xpath').get('chapter_list'))
        result = []
        for chapter in chapters:
            urls = chapter.xpath(novel_list.get(self.novel_id).get('xpath').get('chapter_url')) #判断http uri完整性
            if len(urls) == 0:
                #判断章节url是否为空
                continue
            urls = urls[0]
            if urls.startswith('http') is False and urls.startswith('/') is False:
                urls = url + urls #判断 url 123.html 自动附加当前url + 123.html
            elif urls.startswith('http') is False:
                urls = 'http://' + url.split('/')[2] + urls
            name = chapter.xpath(novel_list.get(self.novel_id).get('xpath').get('chapter_name'))[0]
            urls = self.base64_to_url(url=urls,siteid=self.novel_id,status='add')
            result.append({'url': urls, 'name': name })
        if sort_id is None or int(sort_id) == 2:
            pass
        elif int(sort_id) == 3:
            result.reverse()
        return result
    def get_content(self,url):
        resutl = self.base64_to_url(data=url,status='delete')
        url = resutl.split('|')[0]
        self.novel_id = resutl.split('|')[1]
        res = requests.get(url) 
        res = self.check_encoding(data=res)
        root = etree.HTML(res)
        #reg = r'{content}'.format(content=novel_list.get('novel01').get('xpath').get('content'))
        #reg = r'<div id="content">(.*?)</div>'
        doc = pq(res)
        if novel_list.get(self.novel_id).get('filter_content',None):
            #判断内容是否存在并过滤
            content = doc(novel_list.get(self.novel_id).get('xpath').get('content')).text()
            rest = novel_list.get(self.novel_id).get('filter_content',None)
            for k in rest.split('|'):
                content = content.replace(k,'')
        else:
            content = doc(novel_list.get(self.novel_id).get('xpath').get('content')).text()
        if novel_list.get(self.novel_id).get('filter_chapter',None):
            #判断章节名称是否存在过滤
            title = root.xpath(novel_list.get(self.novel_id).get('xpath').get('title'))[0]
            rest = novel_list.get(self.novel_id).get('filter_chapter',None)
            for k in rest.split('|'):
                title = title.replace(k,'')
        else:
            title = root.xpath(novel_list.get(self.novel_id).get('xpath').get('title'))[0]
        prev_url = root.xpath(novel_list.get(self.novel_id).get('xpath').get('prev_url'))[0]
        next_url = root.xpath(novel_list.get(self.novel_id).get('xpath').get('next_url'))[0]
        if prev_url.startswith('http') is False:
            prev_url = 'http://' + url.split('/')[2] + prev_url
        if next_url.startswith('http') is False:
            next_url = 'http://' + url.split('/')[2] + next_url
        prev_url = self.base64_to_url(url=prev_url,siteid=self.novel_id,status='add')
        next_url = self.base64_to_url(url=next_url,siteid=self.novel_id,status='add')
        if prev_url == '' or prev_url is None:
            prev_url = ''
        elif next_url == '' or next_url is None:
            next_url = ''
        else:
            pass
        result = { 'title': title, 'content': content, 'prev_url': prev_url, 'next_url': next_url }
        #result = 123
        return result
    def get_request(self):
        pass
    def check_encoding(self,data):
        try:
            prop = requests.models.Response.content
            _content = prop.fget(data)
            if data.encoding == 'ISO-8859-1':
                encodings = requests.utils.get_encodings_from_content(_content)
                if encodings:
                    data.encoding = encodings[0]
                else:
                    data.encoding = data.apparent_encoding
                    _content = _content.decode(data.encoding, 'replace').encode('utf8', 'replace')
                #self._content = _content
                return _content
            else:
                return data.text
        except Exception as e:
            print 'check_encoding.ERROR',e
            return data.text


if __name__ == '__main__':
    obj = Novel()
    print obj.get_novel(name=u'完美世界')
  
