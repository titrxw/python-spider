# -*- coding: utf-8 -*-
from src.net.https import Https 
from src.gather.gather import Gather 
from src.store.mysql import Mysql 
from src.analy.analy import analy 
import time

data={
    'parent':[
        {
            "name":"ul",
            "attrName":"class",
            "attrValue":"house-list-wrap",
            "contentType":"",
            'no':0
        },
        {
            "name":"li",
            "attrName":"",
            "attrValue":"",
            "contentType":"",
            'no':0
        }
    ],
    'elements':[
        {
            "key":"title",
            "rule":[
                {
                    "isParent":0,
                    "elements":[
                        {
                            "name": "h2",
                            "attrName": "class",
                            "attrValue": "title",
                            "contentType": "",
                            'no': 0
                        },
                        {
                            "name": "a",
                            "attrName": "",
                            "attrValue": "",
                            "contentType": "text",
                            'no': 0
                        }
                    ]
                }
            ]
        }
    ],
    "detail":{
        'key':"url",
        'url':{
            "isParent":0,
            "elements":[
                {
                    "name": "h2",
                    "attrName": "class",
                    "attrValue": "title",
                    "contentType": "",
                    'no': 0
                },
                {
                    "name": "a",
                    "attrName": "",
                    "attrValue": "",
                    "contentType": "href",
                    'no': 0
                }
            ]
        },
        'elements':[
            {
                "key":"money",
                "rule":[
                    {
                        "isParent":1,
                        "elements":[
                            {
                                "name":"span",
                                "attrName":"class",
                                "attrValue":"price",
                                "contentType":"text",
                                'no':0
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

def save(data={}):
    if len(data)>0:
        stime="time"
        _time=time.time()
        _time=int(_time)
        data[stime]=_time
        try:
            mysql.add("house_store",data)
        except Exception as e:
            raise Exception(e.message)
    else:
        print(data)


def getContent(netTool,method):
    if method=="get":
        return netTool.get()
    if method=="post":
        return netTool.post()
    if method=="ajax":
        return netTool.ajax()
    return ""


def tryAgain(netTool,method):
    content=getContent(netTool,method)
    if netTool.getCode() !=200:
        time.sleep(2)
        content=getContent(netTool,method)
        if netTool.getCode() !=200:
            content=""
            print("error")
    return content


def runSpider(netTool,tgather,method="get",encode="utf-8"):
    time.sleep(1)
    content=tryAgain(netTool,method)
    if content is not None:
        if encode!="utf-8":
            content=content.decode(encode)
        tgather.setContent(content)
        for itemResult in  tgather.run():
            if itemResult is not None:
                if itemResult["type"]=="element":
                    if len(itemResult["value"]) >0:
                        tgather.clearTmp()
                        try:
                            save(itemResult["value"])
                        except Exception as e:
                            print(e)

                if itemResult["type"]=="page":
                    netTool.setUrl(itemResult["value"])
                    global pageNo
                    pageNo=pageNo+1
                    runSpider(netTool,tgather,method=method,encode=encode)

                if itemResult["type"]=="detail":
                    if len(itemResult["value"]["url"])>0:
                        try:
                            netTool.setUrl(itemResult["value"]["url"])
                            gather=Gather("",itemResult["value"]['rules'])
                            runSpider(netTool,gather,method=method,encode=encode)
                        except Exception as e:
                            print(e)
                    else:
                        print(itemResult)
                        # 表示类似详情页的链接获取失败但是之前的数据还存在，需要保存之前的数据

    else:
        print(netTool)

global pageNo
pageNo=1
https=Https(url="http://ty.58.com/ershoufang/?PGTID=0d100000-002e-4b5d-d2dc-a94ed11f9725&ClickID=1",data={})
rule=Analy.getFormatRules(data)
gather=Gather("",Analy.getFormatRules(data))
runSpider(https,gather)