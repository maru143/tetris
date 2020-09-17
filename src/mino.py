#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List, Dict
import sys
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
        """struct the default field for testing (see above)"""

        for i in range(self.height):
            if i < 15:
                continue
            for j in range(self.width):
                if j == 4 or j == 5:
                    continue
                self.grid[i][j] = Block(True, TetroMinoColor.DARKBLUE)

    def print_field(self):
        """output the field to stderr"""

        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].filled:
                    print(1, end="", file=sys.stderr)
                else:
                    print(0, end="", file=sys.stderr)
            print(file=sys.stderr)


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

    def get_rotation_times(self) -> int:
        """returns clockwise rotation times of block"""

        return self.value

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

    def __init__(self, mino: TetroMino, field: Field):
        self.mino = mino
        self.direction = Direction.NORTH
        if mino == TetroMino.O:  # arrangement for O mino
            self.position = (2, 4)
        else:
            self.position = (2, 3)

        # if position is not valid move_up up to 2 times
        for i in range(3):
            if self.valid_place(field):
                continue
            y, x = self.position
            self.position = (y - 1, x)

    def rend_mino(self) -> np.ndarray:
        """returns the shape corresponding to current direction"""

        shape = self.mino.get_shape()
        rotation = self.direction.get_rotation_times()
        shape = np.rot90(shape, rotation)
        return shape

    def valid_place(self, field: Field) -> bool:
        """
        judges whether the dropping mino is in field and
        blocks are not overlapping each other
        """

        size = self.mino.size()
        shape = self.rend_mino()
        y, x = self.position
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
        move mino to (y + i, x + j)
        if impossible undo it
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
        change the direction to next (clockwise)
        if impossible undo it
        """

        self.direction = self.direction.next_dir_clockwise()
        if self.valid_place(field):
            return True
        else:
            self.direction = self.direction.next_dir_anticlockwise()
            return False

    def spin_anticlockwise(self, field: Field) -> bool:
        """
        change the direction to next (anticlockwise)
        if impossible undo it
        """

        self.direction = self.direction.next_dir_anticlockwise()
        if self.valid_place(field):
            return True
        else:
            self.direction = self.direction.next_dir_clockwise()
            return False


class TetroMinoGenerator:
    """generates mino following the bag system rule"""

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
