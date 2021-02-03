from tutorial.pipelines import MyCustomPipeline
import scrapy
from bs4 import BeautifulSoup
import time
import random
import json
import re
from tutorial.news_items import NewsItem



class CrawlNewsSpider(scrapy.Spider):
    name = 'crawl_news'

    pipeline = set([
        MyCustomPipeline
    ])
    
    def start_requests(self):
        ### 해당 url로 이동
        AJAX_URL = 'http://da.wa.news.cn/nodeart/page?nid=11228087&pgnum=1&cnt=10&attr=&tp=1&orderby=1&callback=jQuery112407663660505059227_1612334311918&_=1612334311919'
        yield scrapy.FormRequest(AJAX_URL, self.oParse)

    def oParse(self, response):
        ## json 전처리 (str)
        response = response.text.split('(')[1].replace(')','')
        #print(response)
        ## json으로 읽기 (json)
        jsonresponse = json.loads(response)
        # test 출력
        # print(jsonresponse)
        # list 항목 추출
        dataList = jsonresponse['data']
        # 첫번째 링크만 접근
        for i in dataList['list']:
            print("링크: ", i['LinkUrl'])
            durl = i['LinkUrl']
            yield scrapy.Request(durl, self.itemParser)

    def itemParser(self, response):
        # BeautifulSoup을 사용하여, 내용을 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        ### 데이터 처리부
        # 제목 전처리
        title = soup.select_one('body > div.header.domPC > div.header-cont.clearfix > div.head-line.clearfix > h1 > span.title').text.strip()
        # 날짜 전처리
        date = soup.select_one("body > div.header.domPC > div.header-cont.clearfix > div.header-time.left").text.strip()
        # 출처 전처리
        froms = ' '.join(soup.select_one('body > div.header.domPC > div.header-cont.clearfix > div.source').text.split()).strip()
        froms = re.match(r'^\w+\：(\S+)', froms).group(1)
        # 내용 전처리
        contents = soup.select('#detail > p')
        content = ''
        for i in contents:
            if str(i).startswith("<p>"):
                content += i.text.strip() + "{}".format("" if i.text.strip()[-1] == '?' or i.text.strip()[-1] == '。' else " "  )
        # 작성자 전처리 
        writer = ' '.join(soup.select_one('#articleEdit > span.editor').text.split()).strip()
        writer = re.match(r'.*\:(\S+).*', writer).group(1)
        
        # 출력부
        print("제목: ", title)
        print("등록일: ", date)
        print("출처: ", froms)
        print("내용: ", content)
        print('작성자: ', writer)

        # item 연동
        item = NewsItem()

        item['title'] = title
        item['date'] = date
        item['froms'] = froms
        item['text'] = content
        item['writer'] = writer

        yield item