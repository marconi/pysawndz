#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import *
from utils.helpers import *

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

        self.setupHelpers()
        self.setupAudioObjects()
        self.setupUi()
        self.setupSignals()

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
        self.musicTable.setColumnWidth(0, 220)
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
        self.connect(self.musicTable, SIGNAL("cellDoubleClicked(int, int)"), self.cellDoubleClicked)

        self.connect(self.mediaObject, SIGNAL("tick(qint64)"), self.tick)
        self.connect(self.mediaObject, SIGNAL("stateChanged(Phonon::State, Phonon::State)"), self.stateChanged)
        self.connect(self.mediaObject, SIGNAL("aboutToFinish()"), self.aboutToFinish)
        self.connect(self.mediaObject, SIGNAL("currentSourceChanged(const Phonon::MediaSource &)"), self.sourceChanged);

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
            self.source = []
            self.setCurrentSong(Phonon.MediaSource(filenames[0]))
            for f in filenames:
                source = Phonon.MediaSource(f)
                self.sources.append(source)

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

    def calculateSongTime(self, time, playing = True):
        if playing:
            remaining = self.mediaObject.totalTime() - time
        else:
            remaining = self.mediaObject.totalTime()
        displayTime = QTime(0, (remaining / 60000) % 60, (remaining / 1000) % 60)
        return displayTime.toString("mm:ss")

    def setCurrentSong(self, song):
        self.setWindowTitle(self.phelper.getFileName(song.fileName()))
        self.mediaObject.setCurrentSource(song)

    def displaySongs(self):

        self.ui.musicTable.clearContents()

        if len(self.sources) > 0:

            for song in self.sources:

                self.mediaObject.setCurrentSource(song)
                metaData = self.mediaObject.metaData()
                metaData = self.structHelper.cmapToPyDict(metaData)

                sansFont = QFont("Helvetica [Cronyx]", 12);

                if metaData["TITLE"] == "":
                    title = self.structHelper.getFileName(song)
                else:
                    title = metaData["TITLE"]

                titleItem = QTableWidgetItem(title)
                titleItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                titleItem.setFont(sansFont)

                timeItem = QTableWidgetItem(self.calculateSongTime(None, False))
                timeItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                timeItem.setFont(sansFont)

                artistItem = QTableWidgetItem(metaData["ARTIST"])
                artistItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                artistItem.setFont(sansFont)

                albumItem = QTableWidgetItem(metaData["ALBUM"])
                albumItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                albumItem.setFont(sansFont)

                genreItem = QTableWidgetItem(metaData["GENRE"])
                genreItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                genreItem.setFont(sansFont)

                currentRow = self.sources.index(song)

                self.ui.musicTable.insertRow(currentRow)
                self.ui.musicTable.setItem(currentRow, 0, titleItem)
                self.ui.musicTable.setItem(currentRow, 1, timeItem)
                self.ui.musicTable.setItem(currentRow, 2, artistItem)
                self.ui.musicTable.setItem(currentRow, 3, albumItem)
                self.ui.musicTable.setItem(currentRow, 4, genreItem)

                self.ui.musicTable.setRowHeight(currentRow, 20)

            self.setCurrentSong(self.sources[0])

    def aboutToFinish(self):
        source = self.mediaObject.currentSource()
        index = self.sources.index(source)
        if (index + 1) < len(self.sources):
            self.mediaObject.enqueue(self.sources[index + 1])

    def sourceChanged(self, source):
        if source in self.sources:
            self.setWindowTitle(self.structHelper.getFileName(source))
            self.musicTable.selectRow(self.sources.index(source))
        self.timeLcd.display("00:00")

    def cellDoubleClicked(self, row, column):
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        self.mediaObject.setCurrentSource(self.sources[row])
        self.mediaObject.play()

#test suite for mainwindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec_())