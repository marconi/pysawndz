import sys
from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import *
from utils.helpers import *
from core.songs import *
from database.database import Db

class Mainwindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        #initialize icons
        self.icons = {"play":"images/play.png",
                      "pause":"images/pause.png",
                      "stop":"images/stop.png",
                      "next":"images/next.png",
                      "previous":"images/previous.png",
                      "all_songs":"images/all_songs.png",
                      "playlist":"images/playlist.png",
                      "media_add":"images/media_add.png",
                      "media_remove":"images/media_remove.png",
                      "media_edit":"images/media_edit.png"}
        
        self.sources = Songs()

        self.setupHelpers()
        self.setupAudioObjects()
        self.setupUi()
        self.setupSignals()
        
        self.__current_sid = 0
        
        self.loadAllSongs()
        self.loadAllPlaylists()
        
    def loadAllSongs(self):
        sql = "SELECT s.id, s.title, s.path, s.duration, a.name as artist, al.name as album, g.name as genre FROM songs as s \
                INNER JOIN artists as a ON a.id = s.artist_id \
                INNER JOIN albums as al ON al.id = s.album_id \
                INNER JOIN genres as g ON g.id = s.genre_id ORDER BY s.title ASC"
        query = Db.execute(sql)
        if query:
            while query.next():
                
                song = Song(id=query.value(0).toInt()[0],
                            title=query.value(1).toString(),
                            path=query.value(2).toString(),
                            duration=query.value(3).toInt()[0],
                            artist=query.value(4).toString(),
                            album=query.value(5).toString(),
                            genre=query.value(6).toString())
                
                self.sources.addSong(song)
            self.displayAllSongs()
            
    def loadAllPlaylists(self):
        
        self.playlist.clear()
        allsongs = QListWidgetItem("All Songs")
        allsongs.setIcon(QIcon(self.icons["all_songs"]))
        self.playlist.addItem(allsongs)
        
        query = Db.select(sqlTable="playlists", sqlFields=["id", "name"])
        if query:
            while query.next():
                playlistName = QListWidgetItem(query.value(1).toString())
                playlistName.setIcon(QIcon(self.icons["playlist"]))
                playlistName.setData(Qt.UserRole, query.value(0).toInt()[0])
                self.playlist.addItem(playlistName)
                
        self.playlist.setCurrentRow(0)

    def setupHelpers(self):
        self.phelper = Playerhelper()

    def setupAudioObjects(self):
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(1000)

        self.tempMediaObject = Phonon.MediaObject()

        Phonon.createPath(self.mediaObject, self.audioOutput)

    #setup ui widgets
    def setupUi(self):

        self.resize(1000, 700)
        self.setWindowTitle("Pysawndz")

        #setup menu
        menubar = QMenuBar()
        file = menubar.addMenu("&File")

        self.importm = QAction("Import ...", self)
        self.importm.setShortcut("Ctrl+A")

        self.exit = QAction("Bye!", self)
        self.exit.setShortcut("Ctrl+Q")

        file.addAction(self.importm)
        file.addAction(self.exit)
        self.setMenuBar(menubar)

        #setup toolbar buttons
        self.toolbar = self.addToolBar("Controls")

        self.playbtn = QAction(QIcon(self.icons["play"]), "Play", self)
        self.playbtn.setShortcut("Ctrl+P")

        self.pausebtn = QAction(QIcon(self.icons["pause"]), "Pause", self)
        self.pausebtn.setShortcut("Ctrl+A")

        self.stopbtn = QAction(QIcon(self.icons["stop"]), "Stop", self)
        self.stopbtn.setShortcut("Ctrl+S")

        self.nextbtn = QAction(QIcon(self.icons["next"]), "Next", self)
        self.nextbtn.setShortcut("Ctrl+N")

        self.previousbtn = QAction(QIcon(self.icons["previous"]), "Previous", self)
        self.previousbtn.setShortcut("Ctrl+V")

        self.toolbar.addAction(self.playbtn)
        self.toolbar.addAction(self.pausebtn)
        self.toolbar.addAction(self.stopbtn)
        self.toolbar.addAction(self.previousbtn)
        self.toolbar.addAction(self.nextbtn)

        #setup the songs table view
        self.musicTable = QTableWidget(0, 5)
        self.musicTable.setHorizontalHeaderLabels(["Name", "Time", "Artist", "Albums", "Genre"])
        self.musicTable.horizontalHeader().setStretchLastSection(True)
        self.musicTable.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.musicTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.musicTable.setColumnWidth(0, 320)
        self.musicTable.setColumnWidth(1, 70)

        #setup lcdtimer
        pallete = QPalette()
        self.timeLcd = QLCDNumber()
        pallete.setBrush(QPalette.Light, Qt.darkGray)
        self.timeLcd.setPalette(pallete)
        self.timeLcd.display("00:00")

        #setup seeker
        self.seekSlider = Phonon.SeekSlider()
        self.seekSlider.setMediaObject(self.mediaObject)

        #setup volume slider
        self.volumeSlider = Phonon.VolumeSlider(self)
        self.volumeSlider.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.volumeSlider.setAudioOutput(self.audioOutput)

        #setup left pane
        self.playlist = QListWidget(self)

        #setup bottom control layout
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(self.timeLcd)
        controlsLayout.addWidget(self.seekSlider)
        controlsLayout.addWidget(self.volumeSlider)
        
        #playlist controls
        self.addPlaylist = QPushButton(QIcon(self.icons["media_add"]), '', self)
        self.editPlaylist = QPushButton(QIcon(self.icons["media_edit"]), '', self)
        self.removePlaylist = QPushButton(QIcon(self.icons["media_remove"]), '', self)
        
        #playlist add/remove/edit
        playlistControlsLayout = QHBoxLayout()
        playlistControlsLayout.addWidget(self.addPlaylist)
        playlistControlsLayout.addWidget(self.editPlaylist)
        playlistControlsLayout.addWidget(self.removePlaylist)
        
        #playlist splitter
        playlistVertical = QVBoxLayout()
        playlistVertical.addWidget(self.playlist)
        playlistVertical.addLayout(playlistControlsLayout)
        
        leftPane = QWidget()
        leftPane.setLayout(playlistVertical)

        #setup splitter panes
        self.splitter = QSplitter(self)
        self.splitter.addWidget(leftPane)
        self.splitter.addWidget(self.musicTable)
        self.splitter.setSizes([50, 800])

        #setup main layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        layout.addLayout(controlsLayout)

        #setup central widget
        self.central = QWidget()
        self.central.setLayout(layout)

        #setup content
        self.setCentralWidget(self.central)
        
    def addPlaylistAction(self):
        playlistName, response = QInputDialog.getText(self, 'Pysawndz', 'Playlist name:')

        if response:
            Db.insert("playlists", {"name": playlistName})
            self.loadAllPlaylists()
            self.playlist.setCurrentRow(self.playlist.count() - 1)

    def removePlaylistAction(self):
        
        if self.playlist.currentRow() == 0:
            return

        currentItem = self.playlist.currentItem()
        currentData = currentItem.data(Qt.UserRole).toInt()[0]
        
        Db.delete("playlists", {"id": currentData})
        Db.delete("playlist_songs", {"playlist_id": currentData})
        self.loadAllPlaylists()
        
    
    def editPlaylistAction(self):
        pass

    def setupSignals(self):
        self.connect(self.importm, SIGNAL("triggered()"), self.showOpenDialog)
        self.connect(self.exit, SIGNAL("triggered()"), self, SLOT("close()"))
        self.connect(self.playbtn, SIGNAL("triggered()"), self.mediaObject, SLOT("play()"))
        self.connect(self.stopbtn, SIGNAL("triggered()"), self.mediaObject, SLOT("stop()"))
        self.connect(self.pausebtn, SIGNAL("triggered()"), self.mediaObject, SLOT("pause()"))
        
        self.connect(self.previousbtn, SIGNAL("triggered()"), self.movePrevious)
        self.connect(self.nextbtn, SIGNAL("triggered()"), self.moveNext)
        
        self.connect(self.addPlaylist, SIGNAL("clicked()"), self.addPlaylistAction)
        self.connect(self.removePlaylist, SIGNAL("clicked()"), self.removePlaylistAction)
        self.connect(self.editPlaylist, SIGNAL("clicked()"), self.editPlaylistAction)
        
        self.connect(self.musicTable, SIGNAL("cellDoubleClicked(int, int)"), self.cellDoubleClicked)
        
        self.connect(self.playlist, SIGNAL("currentRowChanged(int)"), self.playListChanged)

        self.connect(self.mediaObject, SIGNAL("tick(qint64)"), self.tick)
        self.connect(self.mediaObject, SIGNAL("stateChanged(Phonon::State, Phonon::State)"), self.stateChanged)
        self.connect(self.mediaObject, SIGNAL("aboutToFinish()"), self.aboutToFinish)
        self.connect(self.mediaObject, SIGNAL("currentSourceChanged(const Phonon::MediaSource &)"), self.sourceChanged);
    
    def clearMusicTable(self):
        self.musicTable.clearContents()
        rowCount = self.musicTable.rowCount() - 1
        while (rowCount >= 0):
            self.musicTable.removeRow(rowCount)
            rowCount -= 1
        
    def playListChanged(self, row):
        
        if not row == 0: 
            currentRow = self.playlist.item(row)
            currentPlaylist = currentRow.data(Qt.UserRole).toInt()[0]
            
            sql = "SELECT s.id, s.title, s.path, s.duration, a.name as artist, al.name as album, g.name as genre FROM songs as s \
                    INNER JOIN artists as a ON a.id = s.artist_id \
                    INNER JOIN albums as al ON al.id = s.album_id \
                    INNER JOIN genres as g ON g.id = s.genre_id \
                    INNER JOIN playlist_songs as ps ON ps.song_id = s.id \
                    WHERE ps.playlist_id = %d \
                    ORDER BY s.title ASC" % (currentPlaylist)
            
            query = Db.execute(sql)

            if query and query.size() > 0:
                while query.next():
                    print query.value(0).toInt()[0]
            else:
                self.clearMusicTable()
                
        else:
            #all songs
            self.displayAllSongs()
    
    def movePrevious(self):
        current_index = self.sources.getSongIndex(self.sources.getSong(self.__current_sid))
        previous_song = self.sources.getByIndex(current_index - 1)
        if not previous_song == False:
            self.setCurrentSong(previous_song)
            self.musicTable.setCurrentCell(current_index - 1, 0)
            self.mediaObject.play()
            
    
    def moveNext(self):
        current_index = self.sources.getSongIndex(self.sources.getSong(self.__current_sid))
        next_song = self.sources.getByIndex(current_index + 1)
        if not next_song == False:
            self.setCurrentSong(next_song)
            self.musicTable.setCurrentCell(current_index + 1, 0)
            self.mediaObject.play()

    def showOpenDialog(self):
        filenames = QStringList()
        filenames = QFileDialog.getOpenFileNames(self,
            "Select music to import",
            QDesktopServices.storageLocation(QDesktopServices.MusicLocation),
            "*.mp3")

        if filenames.isEmpty():
            return

        self.tempMediaObject.clearQueue()
        if len(filenames) > 0:
            for f in filenames:
                
                source = Phonon.MediaSource(f)
                
                self.tempMediaObject.setCurrentSource(source)
                metaData = self.tempMediaObject.metaData()
                metaData = self.phelper.cmapToPyDict(metaData)
                
                if metaData["TITLE"] == "":
                    metaData["TITLE"] = self.phelper.getFileName(f)
                
                newSong = Song(title=metaData["TITLE"], artist=metaData["ARTIST"],
                               album=metaData["ALBUM"], genre=metaData["GENRE"], path=f,
                               duration=self.tempMediaObject.totalTime())
                
                if filenames.indexOf(f) == 0 and not self.mediaObject.state() == Phonon.PlayingState:
                    self.setCurrentSong(newSong)
                
                self.sources.addSong(newSong)

            self.displaySongs()

    def stateChanged(self, newState, oldState):

        if newState == Phonon.ErrorState:
            QMessageBox.critical(self, "Application Error",
                                 "An unrecoverable error occured, Pysawndz will now exit.",
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return

        if self.mediaObject.currentSource().type() == Phonon.MediaSource.Invalid:
            return

        if newState == Phonon.PlayingState:
            fileName = self.mediaObject.currentSource().fileName()
            self.setWindowTitle(fileName.right(fileName.length() - fileName.lastIndexOf("/") - 1))

        #metaData = self.mediaObject.metaData()

    def tick(self, time):
        self.timeLcd.display(self.calculateSongTime(time))

    def calculateSongTime(self, time, playing = True, customTime=None):
        if playing:
            remaining = self.mediaObject.totalTime() - time
        else:
            if customTime == None:
                remaining = self.mediaObject.totalTime()
            else:
                remaining = customTime
        displayTime = QTime(0, (remaining / 60000) % 60, (remaining / 1000) % 60)
        return displayTime.toString("mm:ss")

    def setCurrentSong(self, song):
        source = Phonon.MediaSource(song.getPath())
        self.setWindowTitle(song.getTitle())
        self.mediaObject.setCurrentSource(source)
        
        self.__current_sid = song.getId()

    def displayAllSongs(self):
        
        #self.musicTable.clearContents()

        if len(self.sources) > 0:
            
            for song in self.sources:

                sansFont = QFont("Helvetica [Cronyx]", 12);

                titleItem = QTableWidgetItem(song.getTitle())
                titleItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                titleItem.setFont(sansFont)

                timeItem = QTableWidgetItem(self.calculateSongTime(None, False, song.getDuration()))
                timeItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                timeItem.setFont(sansFont)

                artistItem = QTableWidgetItem(song.getArtist())
                artistItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                artistItem.setFont(sansFont)

                albumItem = QTableWidgetItem(song.getAlbum())
                albumItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                albumItem.setFont(sansFont)

                genreItem = QTableWidgetItem(song.getGenre())
                genreItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                genreItem.setFont(sansFont)
                
                if not self.sources.getSongIndex(song) < self.musicTable.rowCount():
                    currentRow = self.sources.getSongIndex(song)
                    self.musicTable.removeRow(currentRow)
                    
                    self.musicTable.insertRow(currentRow)
                    self.musicTable.setItem(currentRow, 0, titleItem)
                    self.musicTable.setItem(currentRow, 1, timeItem)
                    self.musicTable.setItem(currentRow, 2, artistItem)
                    self.musicTable.setItem(currentRow, 3, albumItem)
                    self.musicTable.setItem(currentRow, 4, genreItem)
    
                    self.musicTable.setRowHeight(currentRow, 20)
            
            currentSong = self.sources.getByIndex(0)
            if currentSong and not self.mediaObject.state() == Phonon.PlayingState:
                self.setCurrentSong(currentSong)

    def aboutToFinish(self):
        #source = self.mediaObject.currentSource()
        
        current_song = self.sources.getSong(self.__current_sid)
        current_index = self.sources.getSongIndex(current_song)

        if (current_index + 1) < len(self.sources):
            next_song = self.sources.getByIndex(current_index + 1)
            source = Phonon.MediaSource(next_song.getPath())
            self.mediaObject.enqueue(source)

    def sourceChanged(self, source):
        print "source changed"

        newSong = self.sources.getSongByPath(source.fileName())
        if newSong:
            self.setWindowTitle(newSong.getTitle())
            self.musicTable.selectRow(self.sources.getSongIndex(newSong))
        
        self.timeLcd.display("00:00")

    def cellDoubleClicked(self, row, column):
        print "cell doubleclicked"
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        song = self.sources.getByIndex(row)
        if song:
            self.setCurrentSong(song)
            self.mediaObject.play()

#test suite for mainwindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec_())