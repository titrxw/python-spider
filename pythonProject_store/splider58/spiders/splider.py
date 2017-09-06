# -*- coding: utf-8 -*-
import scrapy
import hashlib
import urlparse
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from splider58.items import Splider58Item


class SpliderSpider(CrawlSpider):
    # handle_httpstatus_list=[404,500,302]          系统会接收的请求状态   默认是200   也就是说除了200  其他的状态不处理
    name = 'splider'
    baseUrl="http://ty.58.com/ershoufang/"
    urlPrex="x.shtml"
    allowed_domains = ['58.com']
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1'
    }

    def start_requests(self):
        url = 'http://ty.58.com/ershoufang/pn1/'
        yield scrapy.Request(url, headers=self.headers)

    def parse(self, response): 
        items = response.xpath('//ul[@class="house-list-wrap"]/li')
        if len(items)>0:
            for hitem in items:
                url=hitem.xpath(".//@logr").extract()[0]
                url=url.split('_')
                
                item = Splider58Item()
                item['id']=url[3]
                item['url']=self.baseUrl+url[3]+self.urlPrex
                item['title']=hitem.xpath('.//h2[@class="title"]/a/text()').extract()[0]
                item['homeType']=hitem.xpath('.//p[@class="baseinfo"][1]/span[1]/text()').extract()[0]
                item['homeSize']=hitem.xpath('.//p[@class="baseinfo"][1]/span[2]/text()').extract()[0]

                homeDirect=hitem.xpath('.//p[@class="baseinfo"][1]/span[2]/text()').extract()
                if homeDirect:
                    item['homeDirect']=homeDirect

                homeFloor=hitem.xpath('.//p[@class="baseinfo"][1]/span[2]/text()').extract()
                if homeFloor:
                    item['homeFloor']=homeFloor

                item['homeAddress']=''
                address=hitem.xpath('.//p[@class="baseinfo"][2]/span/a[1]/text()').extract()
                if len(address)>0:
                    item['homeAddress']=address[0]
                
                address=hitem.xpath('.//p[@class="baseinfo"][2]/span/a[2]/text()').extract()
                if len(address)>0:
                    item['homeAddress']=item['homeAddress']+address[0]

                address=hitem.xpath('.//p[@class="baseinfo"][2]/span/a[3]/text()').extract()
                if len(address)>0:
                    item['homeAddress']=item['homeAddress']+address[0]
                    
                item['homeUser']=''
                item['homeUser']=hitem.xpath('.//span[@class="jjrname-outer"]/text()').extract()
                if len(item['homeUser'])>0:
                    item['homeUser']=item['homeUser'][0]
                
                item['homeCompany']=''
                item['homeCompany']=hitem.xpath('.//div[@class="jjrinfo"]/text()').extract()
                if len(item['homeCompany'])>0:
                    item['homeCompany']=item['homeCompany'][0]
                    item['homeCompany']=item['homeCompany'].replace(' ','')
                    item['homeCompany']=item['homeCompany'].replace('\n','')
                    item['homeCompany']=item['homeCompany'].replace('\r','')
                    item['homeCompany']=item['homeCompany'].replace('-','')
                    item['homeCompany'] = item['homeCompany'][:-1];  

                item['homeTotal']=hitem.xpath('.//p[@class="sum"]/b/text()').extract()[0]
                item['homeUnivalent']=hitem.xpath('.//p[@class="unit"]/text()').extract()[0]
                time.sleep(0.5)
                yield scrapy.Request(item['url'], headers=self.headers,callback=self.parse_child,meta={'item':item})

            sel=response.xpath('//div[@class="pager"]/a[@class="next"]/@href').extract()
            if len(sel)>0:
                yield scrapy.Request(sel[0], headers=self.headers)


    def parse_child(self, response):
        if 'item' in response.meta:
            item = response.meta['item']
        if item:
            item['elseInfo']=response.xpath('//div[@class="house-basic-item2"]/p[3]/span[1]/text()').extract()
            if len(item['elseInfo'])>0:
                item['elseInfo']=item['elseInfo'][0]
            else:
                yield scrapy.Request(item['url'], headers=self.headers,callback=self.parse_child,meta={'item':item})
            yield item

        
