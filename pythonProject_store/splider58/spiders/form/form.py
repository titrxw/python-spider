# -*- coding: UTF-8 -*-
from splider58.spiders.form.user import  UserInfo

class Form(UserInfo):
    #请求需要的参数
    __source="index_nav"
    __redir="https://www.douban.com/"
    __login="登录"

    def __init__(self,userName,userPwd):
        super(Form,self).__init__(userName,userPwd)               #这里要用super的话父类中必须继承base类Object

    def format(self):
        return {
            "username":self.getUserName(),
            "password":self.getUserPwd(),
            "version":"2.1",
            "key":"49bac5d653633760ebb6c4c5bcdbe13a",
            "type":0
        }





