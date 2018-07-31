from src.store.mysql import Mysql 
from src.store.file import File 
class Store:
    class_instance=None

    def __init__(self,stype='mysql',path=''):
        if stype=='mysql':
            Store.class_instance=Mysql()
        else:
            Store.class_instance=File(path)
    

    def add(self,data):
        if stype=='mysql':
            Store.class_instance.add(data)
        else:
            Store.class_instance.append(data)