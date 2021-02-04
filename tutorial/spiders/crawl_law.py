from urllib.parse import unquote
from tutorial.law_items import LawItem
import scrapy
from scrapy import Selector
from bs4 import BeautifulSoup
import time
import random
import re
import xml.etree.ElementTree as ET
from datetime import datetime

from soupsieve.css_types import Selector

class CrawlLawSpider(scrapy.Spider):
    name = 'crawl_law'

    def start_requests(self):
        url = 'https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=HTML'
        # parse로 이동
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        ### 날짜를 추출
        dates = soup.select('#lawSearchForm > div > table > tbody > tr > td:nth-child(8)')
        sample_url = 'https://www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST={}&type=XML'
        ### 링크 추출 및 날짜 전처리
        links = soup.select('#lawSearchForm > div > table > tbody > tr')
        for i, j in zip(links[:10], dates[:10]):
            i = i.select_one('td > a')['href']
            i = re.match(r'\/\S+MST=(\d+).*',i).group(1)
            j = str(datetime.strptime(j.text.replace('.','/')[:-1], "%Y/%m/%d").date()).replace('-','')
            ### 테스트용
            # print(j)
            durl = sample_url.format(i)
            # 2-3초 여유를 둔다.
            time.sleep(random.randint(2,3))
            # Request를 보낸다.
            yield scrapy.Request(durl, self.itemParse, meta={'id': i, 'fYd': j})

    def itemParse(self, response):
        soup = BeautifulSoup(response.text, 'xml')

        ### 각 필요한 내용 추출 - 전처리
        # 제목
        title = soup.select_one('법령명_한글').text
        # 약칭
        stitle = soup.select_one('법령명약칭').text
        # 시행일 전처리
        date = soup.select_one('시행일자').text
        date = str(datetime.strptime(date, "%Y%m%d").date())
       
        # 소관부처
        froms = soup.select_one('소관부처').text
        # 번호
        number = soup.select_one('전화번호').text
        # 내용 전처리
        contents = soup.select('조문내용')
        content = ''
        for i in contents:
            content += i.text.replace('\n','').replace('\t','').replace('\"','').strip()
        # 부칙
        Addendum = []
        Addendums = soup.select('부칙내용')
        for i in Addendums:
            i = i.text.replace('\n','').replace('\"','').strip()
            Addendum.append(i)
        # 다운로드 링크
        Link = 'https://www.law.go.kr/LSW/lsNewHwpSave.do?trSeq={}&efDvPop=&nwJoYnInfo=Y&lastCheck=Y&ancYnChk=0&lsiSeq={}&efYd={}&chrClsCd=010202&joNo=0001:00,0002:00,0003:00,0003:02,0004:00,0005:00,0006:00,0007:00&nwJoYnInfo=Y&efGubun=Y&joAllCheck=Y&joEfOutPutYn=on&mokChaChk=N'.format(response.meta['id'], response.meta['id'], response.meta['fYd'])
        
        ### 출력부
        # print("제목: ", title)
        # print('약칭: ', stitle)
        # print('시행일: ', date)
        # print('소관부처: ', froms)
        # print('번호: ', number)
        # print("내용: ", content)
        # print("부칙: ", Addendum)
        # print("파일 링크:", Link)


        ### Item 화
        item = LawItem()

        item['title'] = title
        item['stitle'] = stitle
        item['date'] = date
        item['froms'] = froms
        item['number'] = number
        item['content'] = content
        item['Addendum'] = Addendum
        item['Link'] = Link

        yield item

        if (Link):
            yield scrapy.Request(Link, self.save)


    # 첨부 파일 저장 -1
    def save(self, response):
        soup = BeautifulSoup(response.text, 'xml')
        title = soup.find('FIELDBEGIN')
        title = title['Name']
        
        # 저장을 위한 파일 이름
        response.meta['filename'] = title
        yield self.rSave(response)
    
    # 첨부 파일 저장 -2
    def rSave(self, response):
        filename = response.meta['filename']
        path = '/var/icngroup/jhkim95/Downloads/lawsFiles/'+ filename +'.hwp'
        with open(path, 'wb') as f:
            f.write(response.body)