import MySQLdb
import MySQLdb.cursors
import splider58.settings

class Mysql:
    __instance=None
    __conn=None
    __cur=None

    def __init__(self):
        try:
            self.__conn = MySQLdb.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD,db=settings.MYSQL_DBNAME)
            self.__cur = Mysql.class_conn.cursor()
            self.__conn.set_character_set('utf8')
            self.__cur.execute('SET NAMES utf8;')
            self.__cur.execute('SET CHARACTER SET utf8;')
            self.__cur.execute('SET character_set_connection=utf8;')
        except Exception,e:
            raise Exception(e.message)

    def execute(self,sqlStr,params=None):
        try:
            self.__cur.execute(sqlStr, params)
            self.__conn.commit()
        except Exception,e:
            raise Exception(e.message)


    def insert(self,sqlStr,params=None):
        self.execute(sqlStr,params)


    def add(self,table,data):
        sql="insert into "+table+"("

        colums=''
        seat=''
        for key,value in data.items():
            colums=colums+"'"+key+"',"
            seat=seat+"%("+key+")s,"

        colums=colums[:-1]
        seat=seat[:-1]

        sql=sql+colums+") values ("+seat+")"
        self.execute(sql,data)
        

    def update(self,sqlStr,params=None):
        self.execute(sqlStr,params)


    def delete(self,sqlStr,params=None):
        self.execute(sqlStr,params)

    def getOne(self,sqlStr,params=None):
        self.execute(sqlStr,params)
        return self.__cur.fetchone()


    def getAll(self,sqlStr,params=None):
        self.execute(sqlStr,params)
        return self.__cur.fetchall()

