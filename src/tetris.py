#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import sys
from collections import deque
from typing import Deque, List

from src.mino import Field, DroppingMino, TetroMino, TetroMinoGenerator, \
    TetroMinoColor


class Tetris:
    field: Field
    mino_generator: TetroMinoGenerator
    dropping_mino: DroppingMino
    holding_mino: TetroMino
    next_mino_num: int
    next_minos: Deque[TetroMino]

    def __init__(self):
        self.field = Field()
        self.mino_generator = TetroMinoGenerator()
        self.dropping_mino = DroppingMino(self.mino_generator.gen())
        self.holding_mino = TetroMino.Empty
        self.next_mino_num = 5
        self.next_minos = deque()

        for i in range(self.next_mino_num):
            self.next_minos.append(self.mino_generator.gen())

    def rend_field_color(self) -> List[List[TetroMinoColor]]:
        """returns complete field color for painting"""

        field_color = [[TetroMinoColor.WHITE
                        for i in range(self.field.width)]
                       for j in range(self.field.height)]

        # copy field's color simply
        for i in range(self.field.height):
            for j in range(self.field.width):
                field_color[i][j] = self.field.grid[i][j].color

        size = self.dropping_mino.mino.size()
        shape = self.dropping_mino.rend_mino()

        # show dropping mino ghost
        position = self.dropping_mino.position
        ghost_mino = self.dropping_mino
        while ghost_mino.move_mino(1, 0, self.field):
            pass
        y, x = ghost_mino.position
        self.dropping_mino.position = position
        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                field_color[y + i][x + j] = TetroMinoColor.GRAY

        # show dropping mino
        y, x = self.dropping_mino.position
        color = self.dropping_mino.mino.get_color()
        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                field_color[y + i][x + j] = color

        # stderr output for debugging
        for i in range(self.field.height):
            print(" {:<2}:".format(i), end=" ", file=sys.stderr)
            for j in range(self.field.width):
                print(field_color[i][j].value, end="", file=sys.stderr)
            print(file=sys.stderr)

        return field_color
