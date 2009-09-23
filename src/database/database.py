
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *

from settings import *

class Db(object):
    
    __db = None
    
    @staticmethod
    def __getInstance():
        Db.__db = QSqlDatabase(db_settings["DB_TYPE"])
        Db.__db.setDatabaseName(db_settings["DB_NAME"])
        Db.__db.setUserName(db_settings["DB_USER"])
        Db.__db.setPassword(db_settings["DB_PASSWD"])
        Db.__db.setHostName(db_settings["DB_HOST"])
        if not Db.__db.open():
            print Db.__db.lastError().text()
            sys.exit(1)
    
    @staticmethod
    def insert(sqlTable=None, sqlData={}):
        #initiate an instance if there's none
        if Db.__db == None:
            Db.__getInstance()
        
        if len(sqlData) == 0 or sqlTable == None:
            return False
        
        #prepare fields
        sqlFields = ", ".join(sqlData.keys())
        
        #prepare values
        sqlValues = ", ".join([":%s" % (k) for k in sqlData.keys()])
        
        #build the query
        sql = "INSERT INTO %s(%s) VALUES(%s)" % (sqlTable, sqlFields, sqlValues)
        
        query  = QSqlQuery(Db.__db)
        query.prepare(sql)
        for k, v in sqlData.items():
            #bind each item to be inserted
            query.bindValue(":" + k, QVariant(v))

        if query.exec_():
            return query.lastInsertId().toInt()[0]
        else:
            print query.lastError().text()
    
    @staticmethod
    def select(sqlTable=None, sqlFields=[], sqlWhere={}, sqlStart=None, sqlOffset=None):
        #initiate an instance if there's none
        if Db.__db == None:
            Db.__getInstance()
        
        #table is required
        if sqlTable == None:
            return False
        
        query  = QSqlQuery(Db.__db)
        
        if isinstance(sqlFields, list) and len(sqlFields) > 0:
            #use the fields if present
            sql = "SELECT %s FROM %s" % (", ".join(sqlFields), sqlTable)
        else:
            #else select all fields
            sql = "SELECT * FROM %s" % (sqlTable)
        
        #check if theres a where
        if isinstance(sqlWhere, dict) and len(sqlWhere) > 0:
            sqlwhere = []
            whereCounter = 1
            for k, v in sqlWhere.items():
                if isinstance(v, str):
                    #if its a string, add quotes
                    v = "'%s'" % (v)
                sqlwhere.append(str(QString("%s = %s" % (k, "%" + str(whereCounter))).arg(v)))
                whereCounter += 1
            sql += " WHERE " + " AND ".join(sqlwhere)
        
        #check if offset/limit is present
        if not sqlStart == None and not sqlOffset == None:
            sql += " LIMIT %d, %d" % (sqlStart, sqlOffset)
        
        query.exec_(sql)
        if query.size() > 0:
            return query
        else:
            return False
        
    @staticmethod
    def update(sqlTable=None, sqlData={}, sqlWhere={}):
        #initiate an instance if there's none
        if Db.__db == None:
            Db.__getInstance()
        
        #table and data are required
        if sqlTable == None or len(sqlData) == 0:
            return False
        
        query  = QSqlQuery(Db.__db)
        
        #prepare the items to be updated
        sqlset = []
        setCounter = 1
        for k, v in sqlData.items():
            if isinstance(v, str):
                #if its a string, add quotes
                v = "'%s'" % (v)
            sqlset.append(str(QString("%s = %s" % (k, "%" + str(setCounter))).arg(v)))
            setCounter += 1
        sqlItems = ", ".join(sqlset)

        sql = "UPDATE %s SET %s" % (sqlTable, sqlItems)
        
        #check if theres a where
        if isinstance(sqlWhere, dict) and len(sqlWhere) > 0:
            sqlwhere = []
            whereCounter = 1
            for k, v in sqlWhere.items():
                if isinstance(v, str):
                    v = "'%s'" % (v)
                sqlwhere.append(str(QString("%s = %s" % (k, "%" + str(whereCounter))).arg(v)))
                whereCounter += 1
            sql += " WHERE " + " AND ".join(sqlwhere)

        if query.exec_(sql):
            return query.numRowsAffected()
        else:
            return False
        
    @staticmethod
    def delete(sqlTable=None, sqlWhere={}):
        
        #initiate an instance if there's none
        if Db.__db == None:
            Db.__getInstance()
        
        #table is required
        if sqlTable == None :
            return False
        
        query  = QSqlQuery(Db.__db)
        
        sql = "DELETE FROM %s" % (sqlTable)
        
        #check if theres a where
        if isinstance(sqlWhere, dict) and len(sqlWhere) > 0:
            sqlwhere = []
            whereCounter = 1
            for k, v in sqlWhere.items():
                if isinstance(v, str):
                    v = "'%s'" % (v)
                sqlwhere.append(str(QString("%s = %s" % (k, "%" + str(whereCounter))).arg(v)))
                whereCounter += 1
            sql += " WHERE " + " AND ".join(sqlwhere)
            
        print sql
        
        if query.exec_(sql):
            return query.numRowsAffected()
        else:
            return False
        
if __name__ == "__main__":
#    print Db.insert("albums", {"artist_id": 1, "name": "Rammstein", "album_date": "2009-03-03"})
#    result = Db.select("albums", ["name", "album_date"], {"album_date": "2009-03-03", "id": 4})
#    if result:
#        while result.next():
#            print result.value(0).toString() + " : " + result.value(1).toString()
#    else:
#        print "No record found!"
#
#    print Db.update("albums", {"name": "Paramore", "album_date": "2009-01-01"})
    
#    print Db.delete("albums")
    pass
