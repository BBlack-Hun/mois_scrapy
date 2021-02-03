# -*- coding: UTF-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from urllib.parse import urlparse
from itemadapter import ItemAdapter

from scrapy.pipelines.files import FilesPipeline
import os
import datetime
import logging
import pymysql

class TutorialPipeline:
    def __init__(self):
        # self.conn = pymysql.connect(host ="localhost", port=3306, user="root", password="root", db="mois", charset="utf8")
        # self.cursor = self.conn.cursor()
        try:
            # db 연결
            self.conn = pymysql.connect(host ="localhost", port=3306, user="user", password="1q2w3e4r!", db="mois", charset="utf8")
            # print("1")
            self.curs = self.conn.cursor()
            # print("2")
        except:
            print("연결 안됨 ㅎㅎ")

    ### 로컬에 저장
    def file_path(self, request, response=None, info=None):
        return 'files/' + os.path.basename(urlparse(request.url).path)

    def process_item(self, item, spider):
        ### DB에 저장
        sql = "insert into board(title, stitle, regDt, writer, hit, content, link) values (%s, %s, %s, %s, %s, %s, %s)"
        # self.curs.execute(sql, (item['title'], item['stitle'], item['date'], item['writer'], item['hit'], item['text'], item['link_url']))
        # self.conn.commit()