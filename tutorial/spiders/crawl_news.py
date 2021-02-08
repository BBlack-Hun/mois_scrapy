import scrapy
from bs4 import BeautifulSoup
import requests
import time
import random
import json
import re
from tutorial.news_items import NewsItem



class CrawlNewsSpider(scrapy.Spider):
    name = 'crawl_news'
    AJAX_URLS = 'http://da.wa.news.cn/nodeart/page?nid=11228087&pgnum={}&cnt=10&attr=&tp=1&orderby=1'
    flag = False
    cnt = 1

    def start_requests(self):
        AJAX_URL = self.AJAX_URLS.format(self.cnt)
        while self.flag != True :
            AJAX_URL = self.AJAX_URLS.format(self.cnt)
            yield scrapy.Request(AJAX_URL, self.oParse)
            time.sleep(random.randint(2,3))
            self.cnt += 1

    def oParse(self, response):
        ## json으로 읽기 (json)
        jsonresponse = json.loads(response.text)
        if jsonresponse['status'] != '-1':
            # data 항목 추출
            dataList = jsonresponse['data']
            # 링크만 접근
            for i in dataList['list']:
                ptime = i['PubTime']
                ptime = re.match(r'(\d.*)\s\d.*', ptime).group(1).strip().replace('-','')
                if int(ptime) < 20210101:
                    self.flag = True
                    break
                else:
                    durl = i['LinkUrl']
                    # time.sleep(random.randint(1,2))
                    
                    yield scrapy.Request(durl, self.itemParser, dont_filter=True)
        else:
            self.flag = True
            print("빠염 ㅎㅎㅎㅎㅎㅎ")
                
            

    def itemParser(self, response):
        # BeautifulSoup을 사용하여, 내용을 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ### 데이터 처리부
        # 제목 전처리
        title = soup.select_one('body > div.header.domPC > div.header-cont.clearfix > div.head-line.clearfix > h1').text.strip()
        # 날짜 전처리
        date = soup.select_one("body > div.header.domPC > div.header-cont.clearfix > div.header-time.left").text.replace('/', '').strip()        
        date = re.match(r'(\d.*)\s\d.*', date).group(1).replace(' ','-')
        # 출처 전처리
        froms = ' '.join(soup.select_one('body > div.header.domPC > div.header-cont.clearfix > div.source').text.split()).strip()
        froms = re.match(r'^\w+\：(\S+)', froms).group(1)
        # 내용 전처리
        contents = soup.select('#detail > p')
        content = ''
        for i in contents:
            if str(i).startswith("<p>"):
                content += ' '.join(i.text.split()).strip()
                # content += i.text.strip() + "{}".format("" if i.text.strip()[-1] == '?' or i.text.strip()[-1] == '。' else " "  )
        # 작성자 전처리 
        writer = ' '.join(soup.select_one('#articleEdit > span.editor').text.split()).strip()
        writer = re.match(r'.*\:(\S+).*', writer).group(1)
        
        # 출력부
        # print("제목: ", title)
        # print("등록일: ", date)
        # print("출처: ", froms)
        # print("내용: ", content)
        # print('작성자: ', writer)

        # # item 연동
        items = NewsItem()

        items['title'] = title
        items['date'] = date
        items['froms'] = froms
        items['text'] = content
        items['writer'] = writer

        yield items