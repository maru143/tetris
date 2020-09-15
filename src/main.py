#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow

from src.tetris import Tetris


class ExampleWidget(QMainWindow):

    timer: QBasicTimer
    tetris: Tetris

    def __init__(self):

        super().__init__()

        self.init_window()
        self.init_tetris()
        self.init_timer()
        # self.init_buttons()
        self.show()

    def init_window(self) -> None:
        self.resize(300, 300)
        self.setWindowTitle('TETRIS')

    def init_tetris(self) -> None:
        self.tetris = Tetris()

    def init_timer(self) -> None:
        self.timer = QBasicTimer()
        self.timer.start(self.tetris.speed, self)

    # def init_buttons(self) -> None:
    #     button_start = QPushButton("Start", self)
    #     button_start.move(50, 250)
    #     button_start.clicked.connect(self.start_game)
    #
    #     button_end = QPushButton("End", self)
    #     button_end.move(150, 250)
    #     button_end.clicked.connect(self.exit_game)

    # def start_game(self) -> None:
    #     self.statusBar().showMessage("Game Start")
    #
    # def exit_game(self) -> None:
    #     self.statusBar().showMessage("Goodbye")
    #     self.close()

    def timerEvent(self, event: QTimerEvent) -> None:
        """config for timer event handler"""

        if event.timerId() == self.timer.timerId():

            if not self.tetris.oneLineDown():
                self.tetris.dropped()

            self.tetris.dump_field()

    # def paintEvent(self, event: QtGui.QPaintEvent) -> None:
    #     """フィールドの表示処理"""

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """config for keyboard event handler"""

        if event.key() == Qt.Key_Right:
            self.tetris.move_right()
        elif event.key() == Qt.Key_Left:
            self.tetris.move_left()
        elif event.key() == Qt.Key_Up:
            self.tetris.hard_drop()
        elif event.key() == Qt.Key_Down:
            self.tetris.move_down()
        elif event.key() == Qt.Key_Space:
            self.tetris.hard_drop()
        elif event.key() == Qt.Key_X:
            self.tetris.spin_clockwise()
        elif event.key() == Qt.Key_Z:
            self.tetris.spin_anticlockwise()
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

        self.tetris.dump_field()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ExampleWidget()
    sys.exit(app.exec_())
