#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow


class ExampleWidget(QMainWindow):

    def __init__(self):

        super().__init__()

        self.init_window()
        self.init_buttons()
        self.show()

    def init_window(self) -> None:
        """window の初期設定"""

        self.resize(300, 300)
        self.setWindowTitle('TETRIS')

    def init_buttons(self) -> None:
        button_start = QPushButton("Start", self)
        button_start.move(50, 250)
        button_start.clicked.connect(self.start_game)

        button_end = QPushButton("End", self)
        button_end.move(150, 250)
        button_end.clicked.connect(self.exit_game)

    def start_game(self) -> None:
        self.statusBar().showMessage("Game Start")

    def exit_game(self) -> None:
        self.statusBar().showMessage("Goodbye")
        self.close()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """フィールドの表示処理"""
        pass

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """event handlerの設定 (この名前の関数をオーバーロードすると設定できる)"""

        if event.key() == Qt.Key_Right:
            # TODO: 現在のブロックを右に動かす
            print("Right")
        elif event.key() == Qt.Key_Left:
            # TODO: 現在のブロックを右に動かす
            print("Left")
        elif event.key() == Qt.Key_Up:
            # TODO: ハードドロップ
            print("Up")
        elif event.key() == Qt.Key_Down:
            # TODO: ソフトドロップ
            print("Down")
        elif event.key() == Qt.Key_Space:
            # TODO: ハードドロップ
            print("Space")
        elif event.key() == Qt.Key_X:
            # TODO: 右回転
            print("X")
        elif event.key() == Qt.Key_Z:
            # TODO: 左回転
            print("Z")
        elif event.key() == Qt.Key_Shift:
            # TODO: HOLD
            print("SHIFT")
        elif event.key() == Qt.Key_P:
            # TODO: ポーズする
            print("P")
        elif event.key() == Qt.Key_Escape:
            # アプリ終了
            self.close()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ExampleWidget()
    sys.exit(app.exec_())
