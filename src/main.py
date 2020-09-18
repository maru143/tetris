#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

sys.path.append("src/")
from window import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())
