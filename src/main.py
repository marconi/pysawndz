#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from ui.mainwindow import *
from core.player import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Player(Mainwindow())
    sys.exit(app.exec_())