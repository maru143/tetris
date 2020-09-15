#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
from PyQt5.QtGui import QPaintEvent, QKeyEvent, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel

from tetris import Tetris
from mino import TetroMinoColor


class ExampleWidget(QMainWindow):
    timer: QBasicTimer
    tetris: Tetris

    field_block_size: int
    field_offset_x: int
    field_offset_y: int
    hold_block_size: int
    hold_offset_x: int
    hold_offset_y: int
    next_block_size: int
    next_offset_x: int
    next_offset_y: int

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
        self.setWindowTitle('TETRIS')

    def init_painter(self) -> None:
        self.field_block_size = 18
        self.field_offset_x = 105
        self.field_offset_y = 30
        self.hold_block_size = 15
        self.hold_offset_x = 35
        self.hold_offset_y = 100
        self.next_block_size = 15
        self.next_offset_x = 35
        self.next_offset_y = 80

    def init_tetris(self) -> None:
        self.tetris = Tetris()

        hold_label = QLabel("HOLD", self)
        hold_label.move(40, 70)

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

    def end_game(self) -> None:
        self.timer.stop()
        self.statusBar().showMessage("GAMEOVER")

    def timer_reset(self) -> None:
        self.timer.stop()
        self.timer.start(self.tetris.speed, self)

    def timerEvent(self, event: QTimerEvent) -> None:
        """config for timer event handler"""

        if event.timerId() == self.timer.timerId():

            if not self.tetris.oneLineDown():
                self.tetris.dropped()

            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """config for painting tetris field"""

        if self.tetris.is_game_over:
            self.end_game()

        painter = QPainter(self)

        self.paint_field(painter)
        self.paint_hold(painter)
        self.paint_next(painter)

    def paint_block(self, y: int, x: int,
                    offset_y: int, offset_x: int,
                    block_size: int,
                    color: int, painter: QPainter):
        """draws block at (y, x)"""

        color = QColor(color)
        pxl_x = x * block_size + offset_x
        pxl_y = y * block_size + offset_y

        painter.fillRect(pxl_x + 1, pxl_y + 1,
                         block_size, block_size,
                         color)

        painter.setPen(color.lighter())
        painter.drawLine(pxl_x, pxl_y,
                         pxl_x, pxl_y + block_size - 1)
        painter.drawLine(pxl_x, pxl_y,
                         pxl_x + block_size - 1, pxl_y)

        painter.setPen(color.darker())
        painter.drawLine(pxl_x + block_size - 1,
                         pxl_y + block_size - 1,
                         pxl_x + 1,
                         pxl_y + block_size - 1)
        painter.drawLine(pxl_x + block_size - 1,
                         pxl_y + block_size - 1,
                         pxl_x + block_size - 1,
                         pxl_y + 1)

    def paint_block_below(self, y: int, x: int,
                          offset_y: int, offset_x: int,
                          block_size: int,
                          color: int, painter: QPainter):
        """draws block's foot at (y, x)"""

        color = QColor(color)
        pxl_x = x * block_size + offset_x
        pxl_y = y * block_size + offset_y

        painter.fillRect(pxl_x + 1,
                         pxl_y + block_size - 4,
                         block_size,
                         4,
                         color)

        painter.setPen(color.lighter())
        painter.drawLine(pxl_x, pxl_y + block_size - 4,
                         pxl_x, pxl_y + block_size - 1)

        painter.setPen(color.darker())
        painter.drawLine(pxl_x + block_size - 1,
                         pxl_y + block_size - 1,
                         pxl_x + 1,
                         pxl_y + block_size - 1)
        painter.drawLine(pxl_x + block_size - 1,
                         pxl_y + block_size - 1,
                         pxl_x + block_size - 1,
                         pxl_y + block_size - 4)

    def paint_field(self, painter: QPainter):
        field_color = self.tetris.rend_field_color()
        for y in range(self.tetris.field.height):
            for x in range(self.tetris.field.width):
                if y == 0:
                    continue
                elif y == 1:
                    self.paint_block_below(y, x,
                                           self.field_offset_y,
                                           self.field_offset_x,
                                           self.field_block_size,
                                           field_color[y][x].rend_RGB(),
                                           painter)
                else:
                    self.paint_block(y, x,
                                     self.field_offset_y,
                                     self.field_offset_x,
                                     self.field_block_size,
                                     field_color[y][x].rend_RGB(),
                                     painter)

    def paint_hold(self, paint: QPainter):
        if not self.tetris.holding_mino:
            return

        mino = self.tetris.holding_mino
        color = QColor(mino.get_color().rend_RGB())
        shape = mino.get_shape()
        size = mino.size()

        if self.tetris.hold_just_now:
            color = QColor(TetroMinoColor.GRAY.rend_RGB())

        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                self.paint_block(i, j,
                                 self.hold_offset_y, self.hold_offset_x,
                                 self.hold_block_size,
                                 color, paint)

    def paint_next(self, paint: QPainter):
        pass

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """config for keyboard event handler"""

        if self.tetris.is_game_over:
            return

        if event.key() == Qt.Key_Right:
            self.tetris.move_right()
        elif event.key() == Qt.Key_Left:
            self.tetris.move_left()
        elif event.key() == Qt.Key_Up:
            self.tetris.hard_drop()
            self.timer_reset()
        elif event.key() == Qt.Key_Down:
            self.tetris.move_down()
            self.timer_reset()
        elif event.key() == Qt.Key_Space:
            self.tetris.hard_drop()
            self.timer_reset()
        elif event.key() == Qt.Key_X:
            self.tetris.spin_clockwise()
        elif event.key() == Qt.Key_Z:
            self.tetris.spin_anticlockwise()
        elif event.key() == Qt.Key_Shift:
            hold_success = self.tetris.hold()
            if hold_success:
                self.timer_reset()
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
