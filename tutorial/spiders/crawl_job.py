import scrapy
from bs4 import BeautifulSoup
import os
import time
import random


class CrwalJobSpider(scrapy.Spider):
    name = 'crawl_job'

    def start_requests(self):
        # 나 이 사이트 파싱할꺼임...
        yield scrapy.Request('https://www.jobkorea.co.kr/', self.semiRedirect)

    def semiRedirect(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        rr = soup.select_one('#header > div.headInner > div.subSchArea > div.subSchLink > a')['href']
        print(rr)
        yield scrapy.Request(rr, self.parse)

    def parse(self, response):
        # 2~3초 기둘...
        time.sleep(random.randint(2,3))
        print("넘어가지나??? ")
        # 없는 게 있을 수 있으므로 try except 사용
        try:
            print("들어오나??? ")
            # html태그 읽어올거임
            soup = BeautifulSoup(response.text, 'html.parser')
            # 리스트 선언
            # url_links = []
            # a 링크로 뭉태기로 긁어옴
            # url_links = soup.select('#container > div:nth-child(1) > div > ul > li:nth-child(1) > div.info-box > a')
            # container > div:nth-child(1) > div > ul > li:nth-child(1) > div.info-box > a
            url_links = soup.select_one('div > div > h2')
            print(url_links)
            # 가져온 a 태그에서
            for i in url_links:
                # 2~3초 기다림
                time.sleep(random.randint(2,3))
                print(i)
                # href에 해당하는 소스를 추출
                i = i['href']
                # 위의 링크와 결합
                j_url = response.urljoin(i)
                # itemparse를 호출
                yield scrapy.Request(j_url, self.itemparse)
        except:
            pass

    def itemparse(self, response):
        dic = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        # title 뭉치 출력
        rr = ' '.join(soup.select_one('#container > section > div.readSumWrap.clear > article > div.sumTit > h3').text.replace('\n', '').replace('\r','').split())
        # 필요한 부분만 추출
        title = rr.split(' ')[-4:]
        # 문자열로 변환 후, dic에 저장 - title
        dic['title'] = ' '.join(title)
        # 지원 자격
        dic['qulify'] = soup.select_one('#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd').text.replace('\n','').replace('\r','').replace(' ','').strip()
        # 학력
        dic['education'] = soup.select_one('#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(4) > strong').text
        # 고용형태
        dic['type'] = soup.select_one('#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(2) > ul > li > strong').text
        # 급여
        dic['money'] = soup.select_one('#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(4)').text.strip()
        # 지역 전처리
        lr = ' '.join(soup.select_one('#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(6)').text.split())
        dic['location'] = lr
        # 시간
        dic['time'] = ' '.join(soup.select_one('#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(8)').text.split())

        # 출력부
        print("제목:", dic['title'])
        print("지원자격:", dic['qulify'])
        print('학력:', dic['education'])
        print('고용형태:', dic['type'])
        print('급여:', dic['money'])
        print("지역:", dic['location'])
        print("시간:", dic['time'])
