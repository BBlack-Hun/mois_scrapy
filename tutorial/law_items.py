import scrapy


class LawItem(scrapy.Item):
    title = scrapy.Field()  # 제목
    stitle = scrapy.Field()  # 약칭
    date = scrapy.Field()  # 시행일
    froms = scrapy.Field() # 소관부처
    number = scrapy.Field() # 소관부처 번호
    content = scrapy.Field() #내용
    Addendum = scrapy.Field() # 부칙
    link = scrapy.Field() # 파일 링크
    linkname = scrapy.Field() # 파일 이름
    path = scrapy.Field() # 저장용
    pass