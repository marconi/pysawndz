import sys
from PyQt4.QtCore import *
from PyQt4.QtSql import *
from database.database import Db

class Song(object):
    
    def __init__(self, id=None, title=None, duration=None, artist=None, album=None, genre=None, path=None):
        self.__title = title
        self.__duration = duration
        self.__artist = artist
        self.__album = album
        self.__genre = genre
        self.__id = id
        self.__path = path
        self.dirty = False

        if not id == None:
            self.updateSong()

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
    
    def getPath(self):
        return self.__path
    
    def saveSong(self):

        artist_id = self.__getSongArtist()
        
        param = {
            "title": self.__title,
            "duration": self.__duration,
            "artist_id": artist_id,
            "genre_id": self.__getSongGenre(),
            "album_id": self.__getSongAlbum(artist_id),
            "path": self.__path
        }
        
        self.__id = Db.insert("songs", param)

    def __getSongArtist(self):
        
        if not self.__artist == None:
            query = Db.select("artists", ["id"], {"name": self.__artist})
            if query and query.size() > 0 and query.next():
                return query.value(0).toInt()[0]
            else:
                return Db.insert("artists", {"name": self.__artist})
        else:
            query = Db.execute("SELECT a.id FROM artists as a, songs as s WHERE s.artist_id = a.id AND s.id = %d" % (self.__id))
            if query and query.next():
                return query.value(0).toInt()[0]
            
    def __getSongGenre(self):
        
        if not self.__genre == None:
            query = Db.select("genres", ["id"], {"name": self.__genre})
            if query and query.size() > 0 and query.next():
                return query.value(0).toInt()[0]
            else:
                return Db.insert("genres", {"name": self.__genre})
        else:
            query = Db.execute("SELECT g.id FROM genres as g, songs as s WHERE s.genre_id = g.id AND s.id = %d" % (self.__id))
            if query and query.next():
                return query.value(0).toInt()[0]
            
    def __getSongAlbum(self, artist_id):
        
        if not self.__album == None:
            query = Db.select("albums", ["id"], {"name": self.__album, "artist_id": artist_id})
            if query and query.size() > 0 and query.next():
                return query.value(0).toInt()[0]
            else:
                return Db.insert("albums", {"name": self.__album, "artist_id": artist_id})
        else:
            query = Db.execute("SELECT a.id FROM albums as a, songs as s WHERE s.album_id = a.id AND s.id = %d" % (self.__id))
            if query and query.next():
                return query.value(0).toInt()[0]
    
    def updateSong(self):
        
        param = {}
        query = Db.select("songs", ["title", "duration", "artist_id", "genre_id", "album_id", "path"], {"id": self.__id})
        if query and query.next():
            if self.__title == None:
                self.__title = str(query.value(0).toString())
            else:
                param["title"] = self.__title
            
            if self.__duration == None:
                self.__duration = query.value(1).toInt()[0]
            else:
                param["duration"] = self.__duration
                
            if self.__path == None:
                self.__path = str(query.value(5).toString())
            else:
                param["path"] = self.__path
            
            #only update song's artist and album if they are both present
            if not self.__artist == None and not self.__album == None:
                param["artist_id"] = self.__getSongArtist()
                param["album_id"] = self.__getSongAlbum(param["artist_id"])
            else:
                #else, just load defaults
                self.__artist = query.value(2).toInt()[0]
                self.__album = query.value(4).toInt()[0]
            
            if self.__genre == None:
                self.__genre = query.value(3).toInt()[0]
            else:
                param["genre_id"] = self.__getSongGenre()
        
            Db.update("songs", param, {"id": self.__id})
            
        else:
            self.dirty = True
        
    def __str__(self):

        out = ""
        query = Db.execute("SELECT a.name as artist, al.name as album, g.name as genre FROM artists as a, albums as al, genres as g WHERE g.id = %d AND a.id = %d AND al.id = %d" % \
                           (self.__genre, self.__artist, self.__album))
        if query and query.next():
            out = "ID: %d\nTitle: %s\nDuration: %d\nArtist: %s\nAlbum: %s\nGenre: %s\nPath: %s" % \
                (self.__id, self.__title, self.__duration, query.value(0).toString(), query.value(1).toString(), query.value(2).toString(), self.__path)
        else:
            out = "ID: %d\nTitle: %s\nDuration: %d\nPath: %s" % \
                (self.__id, self.__title, self.__duration, self.__path)

        return out

if __name__ == "__main__":
    #testsuite

    s = Song(title="sample", artist="aaa", album="ccc", genre="eee")
    s.saveSong()
    print s.getId()
    
        