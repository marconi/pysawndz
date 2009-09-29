#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from ui.mainwindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec_())