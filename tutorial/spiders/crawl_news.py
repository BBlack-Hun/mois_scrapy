import scrapy
from bs4 import BeautifulSoup
import time
import random
import json
import re
from tutorial.news_items import NewsItem



class CrawlNewsSpider(scrapy.Spider):
    name = 'crawl_news'

    def start_requests(self):
        ### 해당 url로 이동
        # AJAX_URLS = 'http://da.wa.news.cn/nodeart/page?nid=11228087&pgnum=2&cnt=10&attr=&tp=1&orderby=1'
        jQuery = 1612410466223
        for i in range(1, 100):
            try:
                AJAX_URLS = 'http://da.wa.news.cn/nodeart/page?nid=11228087&pgnum={}&cnt=10&attr=&tp=1&orderby=1&callback=jQuery112402859590184527312_1612410232223&_={}'.format(i, jQuery)
                jQuery+=1
                print("테스트입니다. ", AJAX_URLS)
                time.sleep(3)
                yield scrapy.FormRequest(AJAX_URLS, self.oParse)
            except:
                break


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
            time.sleep(random.randint(1,2))
            yield scrapy.Request(durl, self.itemParser)

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
        print("제목: ", title)
        print("등록일: ", date)
        print("출처: ", froms)
        print("내용: ", content)
        print('작성자: ', writer)

        # # item 연동
        items = NewsItem()

        items['title'] = title
        items['date'] = date
        items['froms'] = froms
        items['text'] = content
        items['writer'] = writer

        yield items