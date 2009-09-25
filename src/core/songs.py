from os import path
from core.song import Song
from database.database import Db

class Songs(object):
    
    def __init__(self):
        self.songs = []
        
    def addSong(self, newSong):
        if isinstance(newSong, Song) and not newSong.getId() in self.songs:
            #check if the file still exist
            if path.isfile(newSong.getPath()) and path.exists(newSong.getPath()):
                query = Db.select("songs", ["id"], {"path": newSong.getPath()})
                if query and query.next():
                    songInList = False
                    for song in self.songs:
                        if song.getPath() == newSong.getPath():
                            songInList = True
                    if not songInList:
                        loadedSong = Song(id=query.value(0).toInt())
                        if not loadedSong.dirty:
                            self.songs.append(loadedSong)
                else:
                    newSong.saveSong()
                    if not newSong.dirty:
                        self.songs.append(newSong)
                            
            else:
                #else, delete its record
                Db.delete("songs", {"id": newSong.getId()})

    def getSong(self, song_id):
        for song in self.songs:
            if song_id == song.getId():
                return song
        return False
    
    def removeSong(self, song_id):
        for song in self.songs:
            if song_id == song.getId():
                self.songs.remove(song)
            
    def __len__(self):
        return len(self.songs)
    
    def __iter__(self):
        for s in self.songs:
            yield s
            
    def getByIndex(self, index=None):
        if not index == None and index < len(self.songs) and index >= 0: 
            return self.songs[index]
        return False
    
    def getSongIndex(self, song):
        if song in self.songs:
            return self.songs.index(song)
        return False

if __name__ == "__main__":
    #testsuite
    songs = Songs()
    song1 = Song(id=1)
    songs.addSong(song1)

    song2 = Song(id=2)
    songs.addSong(song2)
    
    for s in songs:
        print str(s) + "\n"
        
    