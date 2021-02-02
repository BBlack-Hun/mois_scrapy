#-*- coding: UTF-8 -*-
import scrapy
from tutorial.items import TutorialItem
from bs4 import BeautifulSoup
import time
import random
import re


class CrawlMoisSpider(scrapy.Spider):
    name = 'crawl_mois'

    def start_requests(self):
        # 나 이 사이트 파싱할꺼임...
        n = 1
        # 69페이지까지 크롤링 ( <70)
        while(n < 70):
            # 해당 url
            url = 'https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008&searchCnd=0&searchWrd=&pageIndex='
            # url 페이지 번호 붙이기
            url += str(n)
            time.sleep(random.randint(1,2))
            # print(url)
            # 해당 페이지로 들어감.
            yield scrapy.Request(url, self.parse)
            # 완료 후 다음 페이지 ㄱㄱ
            n +=1
        #checkUrl(url)
        

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


    def itemParse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 제목 full text
        trr = ' '.join(soup.select_one('#print_area > form > div > h4').text.split())
        # 부제
        try:
            strr = soup.select_one('#print_area > form > div > h4 > span').text.strip()
        except:
            strr = ""
        # 제목 추출
        trr = trr.replace(strr, '').split()
        # 등록일 / 작성자 / 조회수
        dawrhi = ''.join(soup.select_one('#print_area > form > div > div.table_info').text.split())
        dawrhi = re.match(r'\s?등록일\:\s?(\S+)[.| ]?작성자\:\s?(\S+)조회수\:\s?(\d+)', dawrhi)
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
        print("등록일:", date)
        print("작성자:", writer)
        print("조회수:", hit)
        print("내용:", text)
        print("첨부링크:", jLink)

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

    def checkUrl(self, url):
        return 0