import scrapy


class CrawlNewsSpider(scrapy.Spider):
    name = 'crawl_news'
    allowed_domains = ['http://education.news.cn/index.htm']
    start_urls = ['http://http://education.news.cn/index.htm/']

    def parse(self, response):
        pass
