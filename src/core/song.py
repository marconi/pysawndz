#!/usr/bin/env python

import sys
from PyQt4.Qt import *

class Song(object):
    
    def __init__(self, id=None, title=None, duration=None, artist=None, album=None, genre=None):
        self.__title = title
        self.__duration = duration
        self.__artist = artist
        self.__album = album
        self.__genre = genre
        self.__id = id
        
        if id == None:
            self.__saveSong()

    def getId(self):
        return self.__id
    
    def getTitle(self):
        return self.__title
    
    def getDuration(self):
        return self.__duration
    
    def getArtist(self):
        return self.__artist
    
    def getAlbum(self):
        return self.__album
    
    def getGenre(self):
        return self.__genre
    
    def __saveSong(self):
        query  = QSqlQuery(db)
        
        print self.__getSongArtist(self.__artist)
        return
        
        query.prepare("INSERT INTO songs(title, duration) VALUES(?, ?)")
        query.addBindValue(QVariant(self.__title))
        query.addBindValue(QVariant(self.__duration))
        if query.exec_():
            self.__id = query.lastInsertId().toInt()
        else:
            print query.lastError().text()

    def __getSongArtist(self, artist):
        query  = QSqlQuery(db)
        if query.exec_(QString("SELECT id FROM artists WHERE name = %1").arg(artist)):
            if query.size() > 0:
                row = query.record()
                return row.value(1).toInt()
            else:
                query.prepare("INSERT INTO artists(name) VALUES(?)")
                query.addBindValue(QVariant(artist))
                if query.exec_():
                    return query.lastInsertId().toInt()
                else:
                    print query.lastError().text()
        else:
            print query.lastError().text()

if __name__ == "__main__":
    #app = QApplication(sys.argv)
    
    db = QSqlDatabase("QMYSQL")
    db.setDatabaseName("pysawndz")
    db.setUserName("marc")
    db.setPassword("admin")
    db.setHostName("127.0.0.1")
    if not db.open():
        print db.lastError().text()
        sys.exit(1)
    
    song = Song(title="title101", duration="12345", artist="artist101")
    print song.getId()
    #sys.exit(app.exec_())
    
        
    
        