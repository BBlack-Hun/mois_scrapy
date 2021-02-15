import scrapy


class TutorialItem(scrapy.Item):
    title = scrapy.Field()  # 제목
    stitle = scrapy.Field() #서브타이틀
    date = scrapy.Field()  # 등록일
    writer = scrapy.Field() # 작성자
    hit = scrapy.Field() # 조회수
    text = scrapy.Field() #내용
    link_url = scrapy.Field() # 첨부링크
    linkName = scrapy.Field() # 첨부파일이름
    pass