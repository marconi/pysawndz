#!/usr/bin/env python

from core.song import Song

class Songs(object):
    
    def __init__(self):
        self.songs = {}
        
    def addSong(self, newSong):
        if isinstance(newSong, Song) and not newSong.getId() in self.songs:
            self.songs[newSong.getId()] = newSong

    def getSong(self, song_id):
        if song_id in self.songs:
            return self.songs[song_id]
        return False
    
    def removeSong(self, song_id):
        if song_id in self.songs:
            self.songs.pop(song_id)
            
    def __len__(self):
        return len(self.songs)
    
    def __iter__(self):
        for s in self.songs.values():
            yield s

if __name__ == "__main__":
    #testsuite
    songs = Songs()
    song1 = Song(id=1, title="Du Hastx1", duration="12345", artist="Ramstein", genre="Rock", album="Berlin")
    songs.addSong(song1)

    song2 = Song(id=2, title="Du Hastx2", duration="12345", artist="Ramstein", genre="Rock", album="Berlin")
    songs.addSong(song2)
    
    for s in songs:
        print str(s.getId()) + " : " + s.getTitle()
        
    