import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()  # 제목
    date = scrapy.Field()  # 등록일
    froms = scrapy.Field() # 출처
    text = scrapy.Field() #내용
    writer = scrapy.Field() # 작성자
    pass