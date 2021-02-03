import scrapy
from bs4 import BeautifulSoup

class CrawlLawSpider(scrapy.Spider):
    name = 'crawl_law'

    def start_requests(self):
        url = 'https://www.law.go.kr/LSO/openApi/guideResult.do'
        # parse로 이동
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        pass
