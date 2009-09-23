
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *

from settings import *

class Db(object):
    
    def __init__(self):
        self.db = QSqlDatabase(db_settings["DB_TYPE"])
        self.db.setDatabaseName(db_settings["DB_NAME"])
        self.db.setUserName(db_settings["DB_USER"])
        self.db.setPassword(db_settings["DB_PASSWD"])
        self.db.setHostName(db_settings["DB_HOST"])
        if not self.db.open():
            print self.db.lastError().text()
            sys.exit(1)
        
    def insert(self, sqlTable=None, sqlDict={}):
        if len(sqlDict) == 0 or sqlTable == None:
            return False
        
        sqlFields = ", ".join(sqlDict.keys())
        sqlValues = ", ".join([":%s" % (k) for k in sqlDict.keys()])
        sql = "INSERT INTO %s(%s) VALUES(%s)" % (sqlTable, sqlFields, sqlValues)
        
        query  = QSqlQuery(self.db)
        query.prepare(sql)
        for k, v in sqlDict.items():
            query.bindValue(":" + k, QVariant(v))

        if query.exec_():
            return query.lastInsertId().toInt()[0]
        else:
            print query.lastError().text()
            
    def select(self, sqlTable=None, sqlFields=[], sqlWhere={}, sqlStart=None, sqlOffset=None):
        if sqlTable == None:
            return False
        query  = QSqlQuery(self.db)
        
        if isinstance(sqlFields, list) and len(sqlFields) > 0:
            sql = "SELECT %s FROM %s" % (", ".join(sqlFields), sqlTable)
        else:
            sql = "SELECT * FROM %s" % (sqlTable)
        
        if isinstance(sqlWhere, dict) and len(sqlWhere) > 0:
            sqlwhere = []
            whereCounter = 1
            for k, v in sqlWhere.items():
                if isinstance(v, str):
                    v = "'%s'" % (v)
                sqlwhere.append(str(QString("%s = %s" % (k, "%" + str(whereCounter))).arg(v)))
                whereCounter += 1
            sql += " WHERE " + " AND ".join(sqlwhere)
        
        if not sqlStart == None and not sqlOffset == None:
            sql += " LIMIT %d, %d" % (sqlStart, sqlOffset)
        
        print sql
        
        query.exec_(sql)
        if query.size() > 0:
            return query
        else:
            return False
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Db()
    #print db.insert("albums", {"artist_id": 1, "name": "Rammstein", "album_date": "2009-03-03"})
    result = db.select("albums", ["name", "album_date"], {"album_date": "2009-04-04", "id": 2})
    while result.next():
        print result.value(0).toString() + " : " + result.value(1).toString()
    app.exec_()
    
