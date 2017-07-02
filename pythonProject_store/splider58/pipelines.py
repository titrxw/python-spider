# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from splider58 import settings
from scrapy.exceptions import DropItem
import time
import MySQLdb
import MySQLdb.cursors

class Splider58Pipeline(object):
    errorStatusSavePath="d:/pythonProject/error.json"
    cur=None
    conn=None
    fileHandle=None

    def __init__(self):
        self.conn=MySQLdb.connect(host=settings.MYSQL_HOST,user= settings.MYSQL_USER,passwd=settings.MYSQL_PASSWD,db=settings.MYSQL_DBNAME)
        self.cur=self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        self.fileHandle=open(self.errorStatusSavePath,"a")


    def insert_data(self,no,title,company,total):
        _time=time.time()
        _time=int(_time)
        sql = 'INSERT INTO house_res(`no`,`title`,`company`,`total`,`time`,'from') VALUES  (%(no)s,%(title)s,%(company)s,%(total)s,%(time)s,%(from)s)'
        value = {
            'no':no,
            'title':title,
            'company':company,
            'total':total,
            'time':_time,
            'from':'58'
        }
        self.cur.execute(sql,value)
        self.conn.commit()


    def select_no(self,no):
        sql= 'SELECT EXISTS (SELECT 1 FROM house_res WHERE no = %(no)s)'
        value = {
            'no':no
        }
        self.cur.execute(sql,value)
        return  self.cur.fetchall()[0]


    def process_item(self, item, spider):
        if len(item['elseInfo']) <=0:
            self.fileHandle.writelines(item['url']+"\n\r")
            raise DropItem("Missing detail in %s" % item)
        else:
            # ret = self.select_no(item['id'])
            # if ret[0] !=1:
            #     self.insert_data(item['id'],item['title'],item['homeCompany'],float(item['homeTotal']))
            return item


    def spider_closed(self, spider):#爬虫结束时关闭文件
        self.fileHandle.close()
        self.cur.close()
        self.conn.close()
