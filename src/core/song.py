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
        
        query.prepare("INSERT INTO songs(title, duration, artist_id, genre_id, album_id) VALUES(?, ?, ?, ?, ?)")
        query.addBindValue(QVariant(self.__title))
        query.addBindValue(QVariant(self.__duration))
        artist_id = self.__getSongArtist()
        query.addBindValue(QVariant(artist_id))
        query.addBindValue(QVariant(self.__getSongGenre()))
        query.addBindValue(QVariant(self.__getSongAlbum(artist_id)))                         
        if query.exec_():
            self.__id = query.lastInsertId().toInt()[0]
        else:
            print query.lastError().text()

    def __getSongArtist(self):
        query  = QSqlQuery(db)
        sql = QString("SELECT id FROM artists WHERE name = '%1'").arg(self.__artist)
        if query.exec_(sql):
            if query.size() > 0 and query.next():
                artist_id = query.value(0).toInt()[0]
                return artist_id
            else:
                query.prepare("INSERT INTO artists(name) VALUES(?)")
                query.addBindValue(QVariant(self.__artist))
                if query.exec_():
                    return query.lastInsertId().toInt()[0]
                else:
                    print query.lastError().text()
        else:
            print query.lastError().text()
            
    def __getSongGenre(self):
        query  = QSqlQuery(db)
        sql = QString("SELECT id FROM genres WHERE name = '%1'").arg(self.__genre)
        if query.exec_(sql):
            if query.size() > 0 and query.next():
                genre_id = query.value(0).toInt()[0]
                return genre_id
            else:
                query.prepare("INSERT INTO genres(name) VALUES(?)")
                query.addBindValue(QVariant(self.__genre))
                if query.exec_():
                    return query.lastInsertId().toInt()[0]
                else:
                    print query.lastError().text()
        else:
            print query.lastError().text()
            
    def __getSongAlbum(self, artist_id):
        query  = QSqlQuery(db)
        sql = QString("SELECT id FROM albums WHERE name = '%1' AND artist_id = %2").arg(self.__album).arg(artist_id)
        if query.exec_(sql):
            if query.size() > 0 and query.next():
                album_id = query.value(0).toInt()[0]
                return album_id
            else:
                query.prepare("INSERT INTO albums(name, artist_id) VALUES(?, ?)")
                query.addBindValue(QVariant(self.__album))
                query.addBindValue(QVariant(artist_id))
                if query.exec_():
                    return query.lastInsertId().toInt()[0]
                else:
                    print query.lastError().text()
        else:
            print query.lastError().text()
        

if __name__ == "__main__":
    #testsuite
    db = QSqlDatabase("QMYSQL")
    db.setDatabaseName("pysawndz")
    db.setUserName("marc")
    db.setPassword("admin")
    db.setHostName("127.0.0.1")
    if not db.open():
        print db.lastError().text()
        sys.exit(1)
    
    song = Song(title="Du Hast", duration="12345", artist="Rammstein", genre="Rock", album="Berlin")
    print song.getId()
    song = Song(title="Tequero Puta", duration="54321", artist="Rammstein", genre="Rock", album="Berlin")
    print song.getId()
    song = Song(title="Fuer Fuer", duration="2345", artist="Ramstein", genre="Rock", album="Berlin")
    print song.getId()
    
        
    
        