#-*- coding: UTF-8 -*-
import scrapy
from tutorial.items import TutorialItem
from bs4 import BeautifulSoup
import time
import random
import re
import sys


class CrawlMoisSpider(scrapy.Spider):
    name = 'crawl_mois'


    def start_requests(self):
        # 나 이 사이트 파싱할꺼임...
        # 1페이지로 이동
        url = 'https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008'
        yield scrapy.Request(url, self.CheckUrl)

    def CheckUrl(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        total = ' '.join(soup.select_one('#print_area > div.board_top_area > form > span').text.split())
        total = re.match(r'\s?전체\s?\:\s?\d+건\s?1\/(\d+)', total)        
        print(total)
        print("총 페이지 ", total.group(1))
        Limit = int(input("파싱하고 싶은 페이지 혹은 날짜를 입력하시오(날짜는 20200101같이 .을 제외하고입력 또한 입력한 날짜까지 파싱) "))
        if Limit < int(total.group(1)):
            n = 1
            while (n < Limit):
                
                url = 'https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008&searchCnd=0&searchWrd=&pageIndex='
                # url 페이지 번호 붙이기
                url += str(n)
                time.sleep(random.randint(1,2))
                # print(url)
                # 해당 페이지로 들어감.
                yield scrapy.Request(url, self.parse)
                # 완료 후 다음 페이지 ㄱㄱ
                n +=1
        else:
            date = soup.select('#print_area > div.table_wrap.type_01 > form > table > tbody > tr > td:nth-child(5)')
            n = 1
            for i in date:
                i = i.text.strip().replace('.','')
                if Limit == i:
                    break
                else:
                    # 해당 url
                    url = 'https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008&searchCnd=0&searchWrd=&pageIndex='
                    url += str(n)
                    time.sleep(random.randint(1,2))
                    # print(url)
                    # 해당 페이지로 들어감.
                    yield scrapy.Request(url, self.semiParse, Limit)
                    # 완료 후 다음 페이지 ㄱㄱ
                n +=1

    def parse(self, response):
        # 해당페이지 도착시, soup으로 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        # rr 리스트 선언
        rr = []
        # 해당 element 경로의  href 정보만 추출하여 리스트에 저장
        rr = soup.select('#print_area > div.table_wrap.type_01 > form > table > tbody > tr > td.l > div > a')
        # 반복문으로 rr 데이터 한개, 즉 테이블 한줄씩 접근
        for i in rr:
            # rr의 href 데이터만 출력
            i = i['href']
            # 2~4초 쉼
            time.sleep(1)
            # i의 href와 response 링크 조합
            url_join = response.urljoin(i)
            # request요청 보냄
            yield scrapy.Request(url_join, self.itemParse)
    
    def semiParse(self, response, Limit):
        ...


    def itemParse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 제목 full text
        trr = ' '.join(soup.select_one('#print_area > form > div > h4').text.split()).strip()
        # 부제
        try:
            strr = soup.select_one('#print_area > form > div > h4 > span').text.strip()
        except:
            strr = ''
        # 제목 추출
        trr = trr.replace(strr, '').strip()
        # 등록일 / 작성자 / 조회수
        dawrhi = ''.join(soup.select_one('#print_area > form > div > div.table_info').text.split())
        dawrhi = re.match(r'\s?등록일\:\s?(\S+)[.| ]?작성자\:\s?(\S+)조회수\:\s?(\d+).*', dawrhi)
        # 등록일        
        date = dawrhi.group(1)
        # 작성자
        writer = dawrhi.group(2)
        # 조회수
        hit = dawrhi.group(3)
        # 내용
        text = ' '.join(soup.select_one('#desc_pc').text.split()).strip()
        # 첨부링크
        link = soup.select_one('#print_area > form > div > dl.download > dd > div > ul > li > a:nth-child(1)')['href']
        jLink = response.urljoin(link)
        ### 출력 부분
        print("제목:", trr)
        print("부제:", strr)
        # print("등록일:", date)
        # print("작성자:", writer)
        # print("조회수:", hit)
        # print("내용:", text)
        # print("첨부링크:", jLink)

        ### 지정된 item에 매핑
        item = TutorialItem()

        item['title'] = trr
        item['stitle'] = strr
        item['date'] = date
        item['writer'] = writer
        item['hit'] = hit
        item['text'] = text
        item['link'] = jLink
        
        yield item