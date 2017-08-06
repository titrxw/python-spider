from splider58.spiders.analy.element import Element
from splider58.spiders.analy.rule import Rule

class Analy:

    class_ruleObjs=None

    @classmethod
    def getFormatRules(cls,rules=None):
        if cls.class_ruleObjs is None:
            if rules is None:
                return None

            rule=cls.formatRule(rules)

            if rule is None:
                return False

            cls.class_ruleObjs=cls.formatRuleObj(rule)

        return cls.class_ruleObjs

    @classmethod
    def formatRuleObj(cls,rule):
        ruleObjs={"parent":None,"elements":[],"page":None}

        if rule.has_key("parent") and rule['parent'] is not None:
            ruleObjs["parent"]=rule['parent'].formatRule()

        for itemrules in rule['elements']:
            formatRule=[]
            key=""
            for itemrule in itemrules:
                key=itemrule.getKey()
                formatRule.append(itemrule.formatRule())

            ruleObjs["elements"].append({"key":key,"rules":formatRule})

        if rule.has_key("page") and rule['page'] is not None:
            ruleObjs["page"] = rule['page'].formatRule()

        if rule.has_key("detail") and rule['detail'] is not None and len(rule['detail'])>0:
            detail={'url':'','elements':[],'parent':None}
            if rule['detail']['url'] is not None:
                ruleObjs["detail"]=cls.formatRuleObj(rule['detail'])
                ruleObjs["detail"]['url']=rule['detail']['url'].formatRule()

        return ruleObjs

        

    @classmethod
    def formatRule(cls,data):
        ruleObjs={'parent':None,'elements':[],'detail':[],"page":None}

        pElements=[]
        if data.has_key("parent") and data['parent'] is not None:
            for pelement in data['parent']:
                pElements.append(Element(name=pelement['name'],attrName=pelement['attrName'],attrValue=pelement['attrValue'],contentType=pelement['contentType'],no=pelement['no']))

            ruleObjs['parent']=Rule('',pElements,True)

        for item in data["elements"]:
            elementsList=[]
            for elements in item['rule']:
                elementList = []
                for element in elements["elements"]:
                    elementList.append(Element(name=element['name'],attrName=element['attrName'],attrValue=element['attrValue'],contentType=element['contentType'],no=element['no']))

                isParent=False
                if elements['isParent']==1:
                    isParent=True
                elementsList.append(Rule(item['key'], elementList, isParent))

            ruleObjs['elements'].append(elementsList)

        pElements=[]
        if data.has_key("page") and data['page'] is not None:
            for pelement in data['page']:
                pElements.append(Element(name=pelement['name'],attrName=pelement['attrName'],attrValue=pelement['attrValue'],contentType=pelement['contentType'],no=pelement['no']))

            ruleObjs['page']=Rule('',pElements,True)

        
        if data.has_key("detail") and data['detail'] is not None:
            ruleObjs['detail']={'parent':None,'url':None,'elements':[]}
            
            elementList = []
            for element in data['detail']['url']['elements']:
                elementList.append(Element(name=element['name'],attrName=element['attrName'],attrValue=element['attrValue'],contentType=element['contentType'],no=element['no']))

                isParent=False
                if data['detail']['url']['isParent']==1:
                    isParent=True

            ruleObjs['detail']=cls.formatRule(data['detail'])
            ruleObjs['detail']['url']=Rule(data['detail']['key'], elementList, isParent)

        return ruleObjs


    @classmethod
    def flush(cls):
        cls.class_ruleObjs=None


    @classmethod
    def setFormatRules(cls,rules):
        cls.class_ruleObjs=rules


    
