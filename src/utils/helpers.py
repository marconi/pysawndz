#!/usr/bin/env python

from os.path import *
from PyQt4.QtCore import *

class Playerhelper:
    
    def cmapToPyDict(self, cmap):
        if len(cmap) > 0:
            newDict = {}
            for k, v in cmap.items():
                newDict[str(k)] = str(v[0])
            return newDict
        return False
    
    def getFileName(self, filePath):
        fileName = QString(basename(str(filePath)))
        print fileName
        return fileName.left(fileName.lastIndexOf("."))