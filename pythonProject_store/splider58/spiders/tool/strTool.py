class StrTool:
    @classmethod
    def trim(cls,tmpstr):
        tmpstr=tmpstr.split(' ')
        tmpstr=''.join(tmpstr)
        return tmpstr


    def replace(cls,tmpstr,beforeStr,afterStr=''):
        tmpstr=tmpstr.split(beforeStr)
        tmpstr=afterStr.join(tmpstr)
        return tmpstr