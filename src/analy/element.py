class Element:
    __name=''
    __attrName=''
    __attrValue=''
    __contentType=''
    __no=0

    def __init__(self,name,attrName,attrValue,no=0,contentType=''):
        self.__name=name
        self.__attrName=attrName
        self.__attrValue=attrValue
        self.__no=no
        self.__contentType=contentType


    def format(self):
        ruleStr=self.__name
        if self.__attrName!='' and self.__attrValue!='':
            ruleStr=ruleStr+'[@'+self.__attrName+'="'+self.__attrValue+'"]'

        if self.__no>0:
            ruleStr=ruleStr+'['+str(self.__no)+']'

        ruleStr=ruleStr+'/'
        
        if self.__contentType!='':
            if self.__contentType=='text':
                ruleStr=ruleStr+'text()'
            else:
                ruleStr=ruleStr+'@'+self.__contentType

        return ruleStr