# -*- coding: utf-8 -*-
from analy import Analy
from scrapy.selector import Selector 
from strTool import StrTool
import re

class Gather:
    __content=''
    __rule=None
    class_tmpResult={}

    def __init__(self,content,rule):
        self.__content=content
        self.__rule=rule


    def run(self):
        response=Selector(text=self.__content)

        tmpResponse = [response]
        if  self.__rule.has_key("parent") and  self.__rule["parent"] is not None:
            tmpResponse=response.xpath(self.__rule["parent"])
        
        if len(tmpResponse) <= 0:
            yield None
        
        for item in tmpResponse:
            result = {"type":"element","value":[]}
            resultItem = Gather.class_tmpResult
            for itemrules in self.__rule['elements']:
                resultItem[itemrules['key']] = ''

                for itemrule in itemrules["rules"]:
                    tmpValue=None
                    try:
                        tmpValue = item.xpath(itemrule).extract()
                    except Exception,e:
                        print(e)            
                        # 写日志  这里不抛出异常的原因是为了保证数据的完整  不会因为其中一项数据的缺失导致整条数据的丢失
                        
                    if len(tmpValue) >0:
                        tmpValue=tmpValue[0]
                        resultItem[itemrules['key']] = resultItem[itemrules['key']] + tmpValue
                
            if self.__rule.has_key("detail") and self.__rule['detail'] is not None:
                Gather.class_tmpResult=resultItem
                url=''
                try:
                    url = item.xpath(self.__rule['detail']['url']).extract()
                except Exception,e:
                    print(e)
                    
                if len(url) >0 and url is not None:
                    url=url[0]

                result['type']='detail'
                result['value']={
                    'url':url,
                    'rules': {
                        'elements': self.__rule['detail']['elements'],
                        'detail': self.__rule['detail']['detail'],
                        'parent': self.__rule['detail']['parent'],
                        'page': self.__rule['detail']['page']
                    }
                }
            else:
                result['type']='element'
                result["value"]=resultItem
            
            yield result

        if self.__rule.has_key("page") and self.__rule["page"] is not None:
            tmpValue=None
            try:
                tmpValue = response.xpath(self.__rule["page"]).extract()
            except Exception,e:
                print(e)
            if len(tmpValue) >0:
                tmpValue =  tmpValue[0]
                yield {"type":"page","value":tmpValue}
            else:
                yield None


    def setContent(self,content):
        self.__content=content

    def setRule(self,rule):
        self.__rule=rule

    def clearTmp(self):
        Gather.class_tmpResult={}


