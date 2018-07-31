import settings
import os

class File:
    __path=''
    __instance=None

    def __init__(self,path):
        self.__path=path


    def __open(self,pre):
        self.__instance=open(self.__path,pre)


    def append(self,data):
        self.__open('a')
        self.__instance.write(data)


    def write(self,data):
        self.__open('w')
        self.__instance.write(data)


    def close(self):
        self.__instance.close()

        
    def unlink(self,sqlStr,params=None):
        os.remove(self.__path)

