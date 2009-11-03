from os.path import *
from PyQt4.Qt import *

class Playerhelper:
    
    def cmapToPyDict(self, cmap):
        if len(cmap) > 0:
            newDict = {}
            for k, v in cmap.items():
                newDict[str(k)] = str(v[0])
            return newDict
        return {"TITLE":"", "ALBUM":"", "ARTIST":"", "GENRE":""}
    
    def getFileName(self, filePath):
        fileName = QString(basename(str(filePath)))
        return fileName.left(fileName.lastIndexOf("."))