# -*- coding: UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import logging
import pymysql

class TutorialPipeline:
    def __init__(self):
        # self.conn = pymysql.connect(host ="localhost", port=3306, user="root", password="root", db="mois", charset="utf8")
        # self.cursor = self.conn.cursor()
        try:
            # db 연결
            self.conn = pymysql.connect(host ="localhost", port=3306, user="root", password="root", db="mois", charset="utf8")
            # print("1")
            self.curs = self.conn.cursor()
            # print("2")
        except:
            print("연결 안됨 ㅎㅎ")

    def process_item(self, item, spider):
        # # db 갯수 저장
        # result = self.curs.execute('insert count(*) from board')
        # print(result)
        
        # # 테이블에 데이터가 존재한다면 테이블을 새로 생성 (하면 안됨....)
        # if result > 1:
        #     print("데이터가 존재합니다. ㅎㅎ")
        # # 테이블에 데이터가 존재하지 않을 경우 바로 insert
        # else:
        #     # sql문
        #     sql = "insert into board(title, stitle, regDt, writer, hit, content, link) values (%s, %s, %s, %s, %s, %s, %s)"
        #     # insert
        #     self.curs.execute(sql, (item['title'], item['stitle'], item['date'], item['writer'], item['hit'], item['text'], item['link']))
        #     # commit
        #     self.conn.commit()
        ### 닥치고 저장하기 ㅎㅎ
        sql = "insert into board(title, stitle, regDt, writer, hit, content, link) values (%s, %s, %s, %s, %s, %s, %s)"
        self.curs.execute(sql, (item['title'], item['stitle'], item['date'], item['writer'], item['hit'], item['text'], item['link']))
        self.conn.commit()