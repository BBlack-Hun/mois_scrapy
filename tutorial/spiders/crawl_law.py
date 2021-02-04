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
        url = soup.selcet_one('body > div.conbody > div.area_contents > div.contents > div > dl:nth-child(3) > dd:nth-child(3) > table > tbody > tr:nth-child(5) > td')
        print(url)
        pass
