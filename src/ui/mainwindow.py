import sys
from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import *
from utils.helpers import *
from core.songs import *

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
                      "playlist":"images/playlist.png"}
        
        self.sources = Songs()

        self.setupHelpers()
        self.setupAudioObjects()
        self.setupUi()
        self.setupSignals()
        
        self.__current_sid = 0
        
        #TODO: load all songs from db and display as All Songs

    def setupHelpers(self):
        self.phelper = Playerhelper()

    def setupAudioObjects(self):
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(1000)

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
        self.musicTable.setSelectionMode(QAbstractItemView.SingleSelection)
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

        allsongs = QListWidgetItem("All Songs")
        allsongs.setIcon(QIcon(self.icons["all_songs"]))
        self.playlist.addItem(allsongs)

        rammstein = QListWidgetItem("Rammstein")
        rammstein.setIcon(QIcon(self.icons["playlist"]))
        self.playlist.addItem(rammstein)

        #setup bottom control layout
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(self.timeLcd)
        controlsLayout.addWidget(self.seekSlider)
        controlsLayout.addWidget(self.volumeSlider)

        #setup splitter panes
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.playlist)
        self.splitter.addWidget(self.musicTable)
        self.splitter.setSizes([100, 350])

        #setup main layout
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        layout.addLayout(controlsLayout)

        #setup central widget
        self.central = QWidget()
        self.central.setLayout(layout)

        #setup content
        self.setCentralWidget(self.central)

    def setupSignals(self):
        self.connect(self.importm, SIGNAL("triggered()"), self.showOpenDialog)
        self.connect(self.exit, SIGNAL("triggered()"), self, SLOT("close()"))
        self.connect(self.playbtn, SIGNAL("triggered()"), self.mediaObject, SLOT("play()"))
        self.connect(self.stopbtn, SIGNAL("triggered()"), self.mediaObject, SLOT("stop()"))
        self.connect(self.pausebtn, SIGNAL("triggered()"), self.mediaObject, SLOT("pause()"))
        
        self.connect(self.previousbtn, SIGNAL("triggered()"), self.movePrevious)
        self.connect(self.nextbtn, SIGNAL("triggered()"), self.moveNext)
        
        self.connect(self.musicTable, SIGNAL("cellDoubleClicked(int, int)"), self.cellDoubleClicked)

        self.connect(self.mediaObject, SIGNAL("tick(qint64)"), self.tick)
        self.connect(self.mediaObject, SIGNAL("stateChanged(Phonon::State, Phonon::State)"), self.stateChanged)
        self.connect(self.mediaObject, SIGNAL("aboutToFinish()"), self.aboutToFinish)
        self.connect(self.mediaObject, SIGNAL("currentSourceChanged(const Phonon::MediaSource &)"), self.sourceChanged);
        
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

        self.mediaObject.clearQueue()
        if len(filenames) > 0:
            for f in filenames:
                
                source = Phonon.MediaSource(f)
                
                self.mediaObject.setCurrentSource(source)
                metaData = self.mediaObject.metaData()
                metaData = self.phelper.cmapToPyDict(metaData)
                
                if metaData["TITLE"] == "":
                    metaData["TITLE"] = self.phelper.getFileName(f)
                
                newSong = Song(title=metaData["TITLE"], artist=metaData["ARTIST"],
                               album=metaData["ALBUM"], genre=metaData["GENRE"], path=f,
                               duration=self.mediaObject.totalTime())
                
                if filenames.indexOf(f) == 0:
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
        self.setWindowTitle(self.phelper.getFileName(source.fileName()))
        self.mediaObject.setCurrentSource(source)
        
        self.__current_sid = song.getId()

    def displaySongs(self):
        
        self.musicTable.clearContents()

        if len(self.sources) > 0:

            for song in self.sources:
                
                currentRow = self.sources.getSongIndex(song)
                self.musicTable.removeRow(currentRow)

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
                
                self.musicTable.insertRow(currentRow)
                self.musicTable.setItem(currentRow, 0, titleItem)
                self.musicTable.setItem(currentRow, 1, timeItem)
                self.musicTable.setItem(currentRow, 2, artistItem)
                self.musicTable.setItem(currentRow, 3, albumItem)
                self.musicTable.setItem(currentRow, 4, genreItem)

                self.musicTable.setRowHeight(currentRow, 20)
            
            currentSong = self.sources.getByIndex(0)
            if currentSong:
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
        if source in self.sources:
            self.setWindowTitle(self.structHelper.getFileName(source))
            self.musicTable.selectRow(self.sources.index(source))
        self.timeLcd.display("00:00")

    def cellDoubleClicked(self, row, column):
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