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
import pymongo

class TutorialPipeline(object):
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
        self.curs.execute(sql, (item['title'], item['stitle'], item['date'], item['writer'], item['hit'], item['text'], item['link_url']))
        self.conn.commit()

class NewsPipeline(object):

    # collection_name = 'ch_News'
    collection_name = 'law'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)        
        self.client['admin'].authenticate('admin', 'admin')
        self.db = self.client[self.mongo_db]
        
    
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        self.db[self.collection_name].insert(dict(item))
        return item