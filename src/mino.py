#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List, Dict
import numpy as np
import random


class TetroMinoColor(Enum):
    """defines tetromino colors"""

    WHITE = 0
    YELLOW = 1
    LIGHTBLUE = 2
    PURPLE = 3
    ORANGE = 4
    DARKBLUE = 5
    GREEN = 6
    RED = 7
    GRAY = 8

    def rend_RGB(self) -> int:
        if self == TetroMinoColor.YELLOW:
            return 0xFFFF00
        elif self == TetroMinoColor.LIGHTBLUE:
            return 0x00FFFF
        elif self == TetroMinoColor.PURPLE:
            return 0x880088
        elif self == TetroMinoColor.ORANGE:
            return 0xFFAA00
        elif self == TetroMinoColor.DARKBLUE:
            return 0x0000FF
        elif self == TetroMinoColor.GREEN:
            return 0x00FF00
        elif self == TetroMinoColor.RED:
            return 0xFF0000
        elif self == TetroMinoColor.WHITE:
            return 0xFFFFFF
        else:
            return 0x777777


class TetroMino(Enum):
    """defines tetromino types"""

    Empty = 0
    O = 1
    I = 2
    T = 3
    L = 4
    J = 5
    Z = 6
    S = 7

    def get_shape(self) -> np.ndarray:

        shape: List[List[int]]

        if self == TetroMino.O:
            shape = \
                [[1, 1],
                 [1, 1]]

        elif self == TetroMino.I:
            shape = \
                [[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]

        elif self == TetroMino.T:
            shape = \
                [[0, 1, 0],
                 [1, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.L:
            shape = \
                [[0, 0, 1],
                 [1, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.J:
            shape = \
                [[1, 0, 0],
                 [1, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.Z:
            shape = \
                [[1, 1, 0],
                 [0, 1, 1],
                 [0, 0, 0]]

        elif self == TetroMino.S:
            shape = \
                [[0, 1, 1],
                 [1, 1, 0],
                 [0, 0, 0]]

        else:
            shape = [[0]]

        return np.array(shape, dtype=bool)

    def get_color(self) -> TetroMinoColor:
        if self == TetroMino.O:
            return TetroMinoColor.YELLOW
        elif self == TetroMino.I:
            return TetroMinoColor.LIGHTBLUE
        elif self == TetroMino.T:
            return TetroMinoColor.PURPLE
        elif self == TetroMino.L:
            return TetroMinoColor.ORANGE
        elif self == TetroMino.J:
            return TetroMinoColor.DARKBLUE
        elif self == TetroMino.Z:
            return TetroMinoColor.GREEN
        elif self == TetroMino.S:
            return TetroMinoColor.RED
        else:
            return TetroMinoColor.WHITE

    def size(self) -> int:
        """returns the size of mino"""

        return self.get_shape().shape[0]


class Block:
    filled: bool
    color: TetroMinoColor

    def __init__(self, filled: bool, color: TetroMinoColor):
        self.filled = filled
        self.color = color


class Field:
    height: int = 22
    width: int = 10
    grid: List[List[Block]]

    def __init__(self):
        self.grid = \
            [[Block(False, TetroMinoColor.WHITE)
              for i in range(self.width)]
             for j in range(self.height)]

    # 0 : 0000000000
    # 1 : 0000000000
    # 2 : 0000000000
    # 3 : 0000000000
    # 4 : 0000000000
    # 5 : 0000000000
    # 6 : 0000000000
    # 7 : 0000000000
    # 8 : 0000000000
    # 9 : 0000000000
    # 10: 0000000000
    # 11: 0000000000
    # 12: 0000000000
    # 13: 0000000000
    # 14: 0000000000
    # 15: 1111001111
    # 16: 1111001111
    # 17: 1111001111
    # 18: 1111001111
    # 19: 1111001111
    # 20: 1111001111
    # 21: 1111001111

    def set_default(self):
        # テスト用に作るフィールド
        for i in range(self.height):
            if i < 15:
                continue
            for j in range(self.width):
                if j == 4 or j == 5:
                    continue
                self.grid[i][j].filled = True
                self.grid[i][j].color = TetroMinoColor.DARKBLUE

    def print_field(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].filled:
                    print(1, end="")
                else:
                    print(0, end="")
            print()


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

    def get_rotation_times(self) -> int:
        """returns clockwise rotation times of block"""

        if self == Direction.NORTH:
            return 0
        elif self == Direction.WEST:
            return 1
        elif self == Direction.SOUTH:
            return 2
        else:
            return 3

    def next_dir_clockwise(self):
        """returns next cw-direction"""

        if self == Direction.NORTH:
            return Direction.EAST
        elif self == Direction.EAST:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.WEST
        else:
            return Direction.NORTH

    def next_dir_anticlockwise(self):
        """returns next ccw-direction"""

        if self == Direction.NORTH:
            return Direction.WEST
        elif self == Direction.EAST:
            return Direction.NORTH
        elif self == Direction.SOUTH:
            return Direction.EAST
        else:
            return Direction.SOUTH


class DroppingMino:
    position: (int, int)
    mino: TetroMino
    direction: Direction

    def __init__(self, mino: TetroMino):
        self.mino = mino
        self.direction = Direction.NORTH
        if mino == TetroMino.O:  # O minoだけは真ん中から出すよう調節
            self.position = (0, 4)
        else:
            self.position = (0, 3)

    def rend_mino(self) -> np.ndarray:
        """現在のdirectionに合わせたminoの形を返す"""

        shape = self.mino.get_shape()
        rotation = self.direction.get_rotation_times()
        shape = np.rot90(shape, rotation)
        return shape

    def valid_place(self, field: Field) -> bool:
        """現在のminoがちゃんとした場所にいるかどうかを判定する"""

        size = self.mino.size()
        y, x = self.position
        shape = self.rend_mino()
        for i in range(size):
            for j in range(size):
                if not shape[i][j]:
                    continue
                block_y = y + i
                block_x = x + j
                if block_y < 0 or block_y >= field.height or \
                        block_x < 0 or block_x >= field.width:
                    return False
                if field.grid[block_y][block_x].filled:
                    return False
        return True

    def move_mino(self, i: int, j: int, field: Field) -> bool:
        """
        y方向にi, x方向にjだけminoを動かす
        もしだめだったらもとに戻してfalseを返す
        """

        prev_position = self.position
        y, x = self.position
        self.position = (y + i, x + j)
        if self.valid_place(field):
            return True
        else:
            self.position = prev_position
            return False

    def spin_clockwise(self, field: Field) -> bool:
        """
        minoを時計回りに90度回転
        もしだめだったらもとに戻してfalseを返す
        """

        self.direction = self.direction.next_dir_clockwise()
        if self.valid_place(field):
            return True
        else:
            self.direction = self.direction.next_dir_anticlockwise()
            return False

    def spin_anticlockwise(self, field: Field) -> bool:
        """
        minoを反時計回りに90度回転
        もしだめだったらもとに戻してfalseを返す
        """

        self.direction = self.direction.next_dir_anticlockwise()
        if self.valid_place(field):
            return True
        else:
            self.direction = self.direction.next_dir_clockwise()
            return False


class TetroMinoGenerator:
    """bag systemに従ってminoを生成する"""

    dropped_count: Dict[TetroMino, int]
    loops: int  # バッグが何周目か

    def __init__(self):
        self.dropped_count = {
            TetroMino.O: 0,
            TetroMino.I: 0,
            TetroMino.T: 0,
            TetroMino.L: 0,
            TetroMino.J: 0,
            TetroMino.Z: 0,
            TetroMino.S: 0
        }
        self.loops = 1

    def gen(self) -> TetroMino:
        """returns new mino"""

        candidates = [mino
                      for mino, count in self.dropped_count.items()
                      if count < self.loops
                      ]  # このバッグでまだ出てないものを集める

        if not candidates:
            self.loops += 1
            return self.gen()
        else:
            mino = random.choice(candidates)
            self.dropped_count[mino] += 1
            return mino
