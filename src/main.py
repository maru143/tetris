#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
from PyQt5.QtGui import QPaintEvent, QKeyEvent, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow

from src.tetris import Tetris


class ExampleWidget(QMainWindow):
    timer: QBasicTimer
    tetris: Tetris
    block_size: int
    offset_x: int
    offset_y: int

    def __init__(self):

        super().__init__()

        self.init_window()
        self.init_painter()
        self.init_tetris()
        self.init_timer()
        # self.init_buttons()
        self.show()

    def init_window(self) -> None:
        self.resize(400, 500)
        self.offset_x = 50
        self.offset_y = 30
        self.setWindowTitle('TETRIS')

    def init_painter(self) -> None:
        self.block_size = 18

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

            self.update()
            # self.tetris.dump_field()

    def paintEvent(self, event: QPaintEvent) -> None:
        """config for painting tetris field"""

        painter = QPainter(self)

        field_color = self.tetris.rend_field_color()
        for y in range(self.tetris.field.height):
            for x in range(self.tetris.field.width):
                if y == 0:
                    continue
                elif y == 1:
                    self.paint_block_below(y, x, field_color[y][x].rend_RGB(),
                                           painter)
                else:
                    self.paint_block(y, x, field_color[y][x].rend_RGB(),
                                     painter)

    def paint_block(self, y: int, x: int, color: int, painter: QPainter):
        """draws block at (y, x)"""

        color = QColor(color)
        pxl_x = x * self.block_size + self.offset_x
        pxl_y = y * self.block_size + self.offset_y

        painter.fillRect(pxl_x + 1, pxl_y + 1,
                         self.block_size, self.block_size,
                         color)

        painter.setPen(color.lighter())
        painter.drawLine(pxl_x, pxl_y,
                         pxl_x, pxl_y + self.block_size - 1)
        painter.drawLine(pxl_x, pxl_y,
                         pxl_x + self.block_size - 1, pxl_y)

        painter.setPen(color.darker())
        painter.drawLine(pxl_x + self.block_size - 1,
                         pxl_y + self.block_size - 1,
                         pxl_x + 1,
                         pxl_y + self.block_size - 1)
        painter.drawLine(pxl_x + self.block_size - 1,
                         pxl_y + self.block_size - 1,
                         pxl_x + self.block_size - 1,
                         pxl_y + 1)

    def paint_block_below(self, y: int, x: int, color: int, painter: QPainter):
        """draws block's foot at (y, x)"""

        color = QColor(color)
        pxl_x = x * self.block_size + self.offset_x
        pxl_y = y * self.block_size + self.offset_y

        painter.fillRect(pxl_x + 1,
                         pxl_y + self.block_size - 4,
                         self.block_size,
                         4,
                         color)

        painter.setPen(color.lighter())
        painter.drawLine(pxl_x, pxl_y + self.block_size - 4,
                         pxl_x, pxl_y + self.block_size - 1)

        painter.setPen(color.darker())
        painter.drawLine(pxl_x + self.block_size - 1,
                         pxl_y + self.block_size - 1,
                         pxl_x + 1,
                         pxl_y + self.block_size - 1)
        painter.drawLine(pxl_x + self.block_size - 1,
                         pxl_y + self.block_size - 1,
                         pxl_x + self.block_size - 1,
                         pxl_y + self.block_size - 4)

    def keyPressEvent(self, event: QKeyEvent) -> None:
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

        self.update()
        # self.tetris.dump_field()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ExampleWidget()
    sys.exit(app.exec_())
