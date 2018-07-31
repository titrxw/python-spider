import requests

class Http:
    __url=''
    __data={}
    __headers={}
    __requestSession=None
    __cookies=None

    def __init__(self,url,data):
        self.__url=url
        self.__data=data


    def setUrl(self,url):
        self.__url=url


    def getUrl(self):
        return self.__url


    def setData(self,data):
        self.__data=data


    def getData(self):
        return self.__data


    def setHeader(self,headers=None):
        if headers is None:
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116'}
        self.__headers=headers


    def getHeaders(self):
        return self.__headers

    
    def setCookies(self,cookies=None):
        self.__cookies=cookies


    def getCookies(self):
        return self.__cookies


    def setRequestSession(self,handle):
        self.__requestSession=handle


    def getRequestSession(self):
        if self.__requestSession is None:
            self.__requestSession=requests.session()

        return self.__requestSession


    def get(self):
        response=self.getRequestSession().get(self.getUrl(), cookies =self.getCookies(), headers =self.getHeaders())
        return response


    def post(self):
        result = self.getRequestSession().post(self.getUrl(), cookies =self.getCookies(),data = self.getData(), headers =self.getHeaders()) 
        return result


    def ajax(self):
        headers=self.getHeaders()
        if len(headers)<=0:
            header={
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                'X-Requested-With':"XMLHttpRequest",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116"
            }
        else:
            header=headers
            
        result=self.getRequestSession().post(self.getUrl(), data = self.getData(), headers = header)
        self.setCookies(result.cookies)
        return result