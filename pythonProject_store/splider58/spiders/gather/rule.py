class Rule:
    __key=''
    __elements=[]
    __isParent=False

    def __init__(self,key,elements,isParent):
        self.__key=key
        self.__elements=elements
        self.__isParent=isParent

    
    def formatRule(self):
        rules=''
        if self.__isParent:
            rules='//'
        else:
            rules='.//'

        for item in self.__elements:
            rules=rules+item.format()
        
        rules=rules.rstrip('/')
        return rules


    def getKey(self):
        return self.__key


    def getRules(self):
        return self.__rules

    def getElements(self):
        return self.__elements

    def getIsParent(self):
        return self.__isParent